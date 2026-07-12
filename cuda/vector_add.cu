#include "adtrl/cuda_support.hpp"

#include <cuda_runtime.h>

#include <algorithm>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int kThreadsPerBlock = 256;
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

__global__ void vector_add_kernel(const float* left,
                                  const float* right,
                                  float* output,
                                  const std::size_t count) {
  const std::size_t start = static_cast<std::size_t>(blockIdx.x) * blockDim.x + threadIdx.x;
  const std::size_t stride = static_cast<std::size_t>(blockDim.x) * gridDim.x;
  for (std::size_t index = start; index < count; index += stride) {
    output[index] = left[index] + right[index];
  }
}

int block_count_for(const std::size_t elements) {
  const std::size_t required = (elements + kThreadsPerBlock - 1U) / kThreadsPerBlock;
  return static_cast<int>(std::min<std::size_t>(required, kMaximumBlocks));
}

}  // namespace

int main(const int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    adtrl::cuda::print_device_banner();

    std::vector<float> left(options.elements);
    std::vector<float> right(options.elements);
    std::vector<float> expected(options.elements);
    std::vector<float> actual(options.elements);

    for (std::size_t index = 0; index < options.elements; ++index) {
      left[index] = static_cast<float>(static_cast<int>(index % 251U) - 125) * 0.03125F;
      right[index] = static_cast<float>(static_cast<int>(index % 113U) - 56) * 0.0625F;
      expected[index] = left[index] + right[index];
    }

    adtrl::cuda::Stream stream;
    adtrl::cuda::DeviceBuffer<float> device_left(options.elements);
    adtrl::cuda::DeviceBuffer<float> device_right(options.elements);
    adtrl::cuda::DeviceBuffer<float> device_output(options.elements);

    device_left.copy_from_host_async(left.data(), left.size(), stream.get());
    device_right.copy_from_host_async(right.data(), right.size(), stream.get());
    stream.synchronize();

    const int blocks = block_count_for(options.elements);
    const auto launch = [&] {
      vector_add_kernel<<<blocks, kThreadsPerBlock, 0, stream.get()>>>(
          device_left.get(), device_right.get(), device_output.get(), options.elements);
      ADTRL_CUDA_CHECK(cudaGetLastError());
    };

    launch();
    stream.synchronize();
    const float average_kernel_ms =
        adtrl::cuda::benchmark_kernel_ms(options.iterations, stream.get(), launch);

    device_output.copy_to_host_async(actual.data(), actual.size(), stream.get());
    stream.synchronize();

    const adtrl::cuda::ValidationResult validation =
        adtrl::cuda::validate_near(expected, actual, 1.0e-6, 1.0e-6);

    std::cout << "experiment=vector_add elements=" << options.elements
              << " iterations=" << options.iterations << " blocks=" << blocks
              << " threads_per_block=" << kThreadsPerBlock << '\n';
    std::cout << "timing_scope=kernel_only cuda_event_average_ms=" << average_kernel_ms << '\n';
    adtrl::cuda::print_validation(validation);
    return validation.passed ? EXIT_SUCCESS : EXIT_FAILURE;
  } catch (const std::exception& error) {
    std::cerr << "vector_add failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
