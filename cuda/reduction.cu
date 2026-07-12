#include "adtrl/cuda_support.hpp"

#include <cuda_runtime.h>

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int kThreadsPerBlock = 256;
constexpr int kValuesPerThread = 2;
constexpr int kMaximumBlocks = 4096;

struct Options {
  std::size_t elements{1U << 20U};
  int iterations{100};
};

void print_usage(const char* executable) {
  std::cout << "Usage: " << executable << " [--elements N] [--iterations N]\n";
}

Options parse_options(const int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument{argv[index]};
    if (argument == "--help" || argument == "-h") {
      print_usage(argv[0]);
      std::exit(EXIT_SUCCESS);
    }
    if (index + 1 >= argc) {
      throw std::invalid_argument("missing value for " + argument);
    }
    if (argument == "--elements") {
      options.elements = adtrl::cuda::parse_positive_size(argv[++index], "--elements");
    } else if (argument == "--iterations") {
      options.iterations = adtrl::cuda::parse_positive_int(argv[++index], "--iterations");
    } else {
      throw std::invalid_argument("unknown option: " + argument);
    }
  }
  return options;
}

__global__ void reduce_sum_kernel(const float* input, float* output, const std::size_t count) {
  extern __shared__ float partial_sums[];

  const unsigned int thread = threadIdx.x;
  std::size_t index =
      static_cast<std::size_t>(blockIdx.x) * blockDim.x * kValuesPerThread + thread;
  const std::size_t stride =
      static_cast<std::size_t>(gridDim.x) * blockDim.x * kValuesPerThread;

  float local_sum = 0.0F;
  while (index < count) {
    local_sum += input[index];
    const std::size_t paired_index = index + blockDim.x;
    if (paired_index < count) {
      local_sum += input[paired_index];
    }
    index += stride;
  }

  partial_sums[thread] = local_sum;
  __syncthreads();

  for (unsigned int offset = blockDim.x / 2U; offset > 0U; offset >>= 1U) {
    if (thread < offset) {
      partial_sums[thread] += partial_sums[thread + offset];
    }
    __syncthreads();
  }

  if (thread == 0U) {
    output[blockIdx.x] = partial_sums[0];
  }
}

std::size_t block_count_for(const std::size_t elements) {
  constexpr std::size_t values_per_block = kThreadsPerBlock * kValuesPerThread;
  const std::size_t required = (elements + values_per_block - 1U) / values_per_block;
  return std::min<std::size_t>(required, kMaximumBlocks);
}

const float* launch_reduction(const float* input,
                              float* scratch_a,
                              float* scratch_b,
                              std::size_t count,
                              const cudaStream_t stream) {
  const float* current_input = input;
  float* current_output = scratch_a;
  bool output_is_a = true;

  do {
    const std::size_t blocks = block_count_for(count);
    reduce_sum_kernel<<<static_cast<unsigned int>(blocks),
                        kThreadsPerBlock,
                        kThreadsPerBlock * sizeof(float),
                        stream>>>(current_input, current_output, count);
    ADTRL_CUDA_CHECK(cudaGetLastError());

    count = blocks;
    current_input = current_output;
    output_is_a = !output_is_a;
    current_output = output_is_a ? scratch_a : scratch_b;
  } while (count > 1U);

  return current_input;
}

}  // namespace

int main(const int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    adtrl::cuda::print_device_banner();

    std::vector<float> input(options.elements);
    for (std::size_t index = 0; index < options.elements; ++index) {
      input[index] = static_cast<float>((index % 29U) + 1U) / 29.0F;
    }
    const double expected = std::accumulate(input.begin(), input.end(), 0.0);

    const std::size_t scratch_elements = std::max<std::size_t>(1U, block_count_for(options.elements));
    adtrl::cuda::Stream stream;
    adtrl::cuda::DeviceBuffer<float> device_input(options.elements);
    adtrl::cuda::DeviceBuffer<float> scratch_a(scratch_elements);
    adtrl::cuda::DeviceBuffer<float> scratch_b(scratch_elements);
    device_input.copy_from_host_async(input.data(), input.size(), stream.get());
    stream.synchronize();

    const float* result_pointer = nullptr;
    const auto launch = [&] {
      result_pointer = launch_reduction(
          device_input.get(), scratch_a.get(), scratch_b.get(), options.elements, stream.get());
    };

    launch();
    stream.synchronize();
    const float average_kernel_ms =
        adtrl::cuda::benchmark_kernel_ms(options.iterations, stream.get(), launch);

    float actual = 0.0F;
    ADTRL_CUDA_CHECK(cudaMemcpyAsync(
        &actual, result_pointer, sizeof(actual), cudaMemcpyDeviceToHost, stream.get()));
    stream.synchronize();

    const double absolute_error = std::abs(expected - static_cast<double>(actual));
    const double relative_error = absolute_error / std::max(std::abs(expected), 1.0e-12);
    const double allowed_error = 1.0e-3 + 2.0e-5 * std::abs(expected);
    const bool passed = std::isfinite(actual) && absolute_error <= allowed_error;

    std::cout << "experiment=reduction elements=" << options.elements
              << " iterations=" << options.iterations
              << " threads_per_block=" << kThreadsPerBlock << '\n';
    std::cout << "timing_scope=all_reduction_kernels cuda_event_average_ms="
              << average_kernel_ms << '\n';
    std::cout << "correctness=" << (passed ? "PASS" : "FAIL") << " expected=" << expected
              << " actual=" << actual << " abs_error=" << absolute_error
              << " rel_error=" << relative_error << '\n';
    return passed ? EXIT_SUCCESS : EXIT_FAILURE;
  } catch (const std::exception& error) {
    std::cerr << "reduction failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
