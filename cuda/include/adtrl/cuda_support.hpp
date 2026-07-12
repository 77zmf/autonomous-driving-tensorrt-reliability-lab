#pragma once

#include <cuda_runtime_api.h>

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace adtrl::cuda {

class CudaError final : public std::runtime_error {
 public:
  explicit CudaError(const std::string& message) : std::runtime_error(message) {}
};

inline void check(const cudaError_t status, const char* expression, const char* file, const int line) {
  if (status == cudaSuccess) {
    return;
  }

  std::ostringstream message;
  message << file << ':' << line << ": CUDA call `" << expression << "` failed: "
          << cudaGetErrorName(status) << " (" << cudaGetErrorString(status) << ')';
  throw CudaError(message.str());
}

#define ADTRL_CUDA_CHECK(expression) \
  ::adtrl::cuda::check((expression), #expression, __FILE__, __LINE__)

class Stream final {
 public:
  Stream() { ADTRL_CUDA_CHECK(cudaStreamCreateWithFlags(&stream_, cudaStreamNonBlocking)); }

  ~Stream() {
    if (stream_ != nullptr) {
      (void)cudaStreamDestroy(stream_);
    }
  }

  Stream(const Stream&) = delete;
  Stream& operator=(const Stream&) = delete;

  Stream(Stream&& other) noexcept : stream_(std::exchange(other.stream_, nullptr)) {}

  Stream& operator=(Stream&& other) noexcept {
    if (this != &other) {
      if (stream_ != nullptr) {
        (void)cudaStreamDestroy(stream_);
      }
      stream_ = std::exchange(other.stream_, nullptr);
    }
    return *this;
  }

  [[nodiscard]] cudaStream_t get() const noexcept { return stream_; }

  void synchronize() const { ADTRL_CUDA_CHECK(cudaStreamSynchronize(stream_)); }

 private:
  cudaStream_t stream_{nullptr};
};

class Event final {
 public:
  Event() { ADTRL_CUDA_CHECK(cudaEventCreateWithFlags(&event_, cudaEventDefault)); }

  ~Event() {
    if (event_ != nullptr) {
      (void)cudaEventDestroy(event_);
    }
  }

  Event(const Event&) = delete;
  Event& operator=(const Event&) = delete;

  Event(Event&& other) noexcept : event_(std::exchange(other.event_, nullptr)) {}

  Event& operator=(Event&& other) noexcept {
    if (this != &other) {
      if (event_ != nullptr) {
        (void)cudaEventDestroy(event_);
      }
      event_ = std::exchange(other.event_, nullptr);
    }
    return *this;
  }

  void record(const cudaStream_t stream) const { ADTRL_CUDA_CHECK(cudaEventRecord(event_, stream)); }

  void synchronize() const { ADTRL_CUDA_CHECK(cudaEventSynchronize(event_)); }

  [[nodiscard]] float elapsed_ms_since(const Event& start) const {
    float elapsed_ms = 0.0F;
    ADTRL_CUDA_CHECK(cudaEventElapsedTime(&elapsed_ms, start.event_, event_));
    return elapsed_ms;
  }

 private:
  cudaEvent_t event_{nullptr};
};

template <typename T>
class DeviceBuffer final {
 public:
  explicit DeviceBuffer(const std::size_t count) : count_(count) {
    if (count_ == 0) {
      throw std::invalid_argument("DeviceBuffer size must be greater than zero");
    }
    if (count_ > std::numeric_limits<std::size_t>::max() / sizeof(T)) {
      throw std::overflow_error("DeviceBuffer allocation size overflow");
    }
    ADTRL_CUDA_CHECK(cudaMalloc(reinterpret_cast<void**>(&data_), bytes()));
  }

  ~DeviceBuffer() {
    if (data_ != nullptr) {
      (void)cudaFree(data_);
    }
  }

  DeviceBuffer(const DeviceBuffer&) = delete;
  DeviceBuffer& operator=(const DeviceBuffer&) = delete;

  DeviceBuffer(DeviceBuffer&& other) noexcept
      : data_(std::exchange(other.data_, nullptr)), count_(std::exchange(other.count_, 0)) {}

  DeviceBuffer& operator=(DeviceBuffer&& other) noexcept {
    if (this != &other) {
      if (data_ != nullptr) {
        (void)cudaFree(data_);
      }
      data_ = std::exchange(other.data_, nullptr);
      count_ = std::exchange(other.count_, 0);
    }
    return *this;
  }

  [[nodiscard]] T* get() noexcept { return data_; }
  [[nodiscard]] const T* get() const noexcept { return data_; }
  [[nodiscard]] std::size_t size() const noexcept { return count_; }
  [[nodiscard]] std::size_t bytes() const noexcept { return count_ * sizeof(T); }

  void copy_from_host_async(const T* source, const std::size_t count, const cudaStream_t stream) {
    validate_copy(count);
    ADTRL_CUDA_CHECK(cudaMemcpyAsync(data_, source, count * sizeof(T), cudaMemcpyHostToDevice, stream));
  }

  void copy_to_host_async(T* destination, const std::size_t count, const cudaStream_t stream) const {
    validate_copy(count);
    ADTRL_CUDA_CHECK(cudaMemcpyAsync(destination, data_, count * sizeof(T), cudaMemcpyDeviceToHost, stream));
  }

 private:
  void validate_copy(const std::size_t count) const {
    if (count > count_) {
      throw std::out_of_range("DeviceBuffer copy exceeds allocation");
    }
  }

  T* data_{nullptr};
  std::size_t count_{0};
};

template <typename Launch>
float benchmark_kernel_ms(const int iterations, const cudaStream_t stream, Launch&& launch) {
  if (iterations <= 0) {
    throw std::invalid_argument("iterations must be greater than zero");
  }

  Event start;
  Event stop;
  start.record(stream);
  for (int iteration = 0; iteration < iterations; ++iteration) {
    launch();
  }
  stop.record(stream);
  stop.synchronize();
  return stop.elapsed_ms_since(start) / static_cast<float>(iterations);
}

struct ValidationResult {
  bool passed{true};
  std::size_t first_failure{0};
  float expected_at_failure{0.0F};
  float actual_at_failure{0.0F};
  double max_absolute_error{0.0};
  double max_relative_error{0.0};
};

inline ValidationResult validate_near(const std::vector<float>& expected,
                                      const std::vector<float>& actual,
                                      const double absolute_tolerance,
                                      const double relative_tolerance) {
  if (expected.size() != actual.size()) {
    throw std::invalid_argument("validation vectors have different sizes");
  }

  ValidationResult result;
  for (std::size_t index = 0; index < expected.size(); ++index) {
    const double expected_value = static_cast<double>(expected[index]);
    const double actual_value = static_cast<double>(actual[index]);
    const double absolute_error = std::abs(expected_value - actual_value);
    const double relative_error = absolute_error / std::max(std::abs(expected_value), 1.0e-12);

    result.max_absolute_error = std::max(result.max_absolute_error, absolute_error);
    result.max_relative_error = std::max(result.max_relative_error, relative_error);

    const double allowed_error = absolute_tolerance + relative_tolerance * std::abs(expected_value);
    if ((!std::isfinite(actual_value) || absolute_error > allowed_error) && result.passed) {
      result.passed = false;
      result.first_failure = index;
      result.expected_at_failure = expected[index];
      result.actual_at_failure = actual[index];
    }
  }
  return result;
}

inline void print_validation(const ValidationResult& result) {
  std::cout << "correctness=" << (result.passed ? "PASS" : "FAIL")
            << " max_abs_error=" << std::scientific << result.max_absolute_error
            << " max_rel_error=" << result.max_relative_error << std::defaultfloat << '\n';
  if (!result.passed) {
    std::cerr << "first_failure_index=" << result.first_failure
              << " expected=" << result.expected_at_failure
              << " actual=" << result.actual_at_failure << '\n';
  }
}

inline std::size_t parse_positive_size(const char* text, const char* option_name) {
  try {
    std::size_t consumed = 0;
    const std::string value{text};
    const auto parsed = std::stoull(value, &consumed, 10);
    if (consumed != value.size() || parsed == 0 ||
        parsed > std::numeric_limits<std::size_t>::max()) {
      throw std::invalid_argument("out of range");
    }
    return static_cast<std::size_t>(parsed);
  } catch (const std::exception&) {
    throw std::invalid_argument(std::string(option_name) + " requires a positive integer");
  }
}

inline int parse_positive_int(const char* text, const char* option_name) {
  const std::size_t parsed = parse_positive_size(text, option_name);
  if (parsed > static_cast<std::size_t>(std::numeric_limits<int>::max())) {
    throw std::invalid_argument(std::string(option_name) + " exceeds int range");
  }
  return static_cast<int>(parsed);
}

inline std::size_t checked_product(const std::size_t left,
                                   const std::size_t right,
                                   const char* description) {
  if (left != 0 && right > std::numeric_limits<std::size_t>::max() / left) {
    throw std::overflow_error(std::string(description) + " size overflow");
  }
  return left * right;
}

inline void print_device_banner() {
  int device = 0;
  ADTRL_CUDA_CHECK(cudaGetDevice(&device));
  cudaDeviceProp properties{};
  ADTRL_CUDA_CHECK(cudaGetDeviceProperties(&properties, device));
  std::cout << "device=\"" << properties.name << "\" compute_capability=" << properties.major << '.'
            << properties.minor << '\n';
}

}  // namespace adtrl::cuda
