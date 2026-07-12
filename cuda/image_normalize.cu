#include "adtrl/cuda_support.hpp"

#include <cuda_runtime.h>

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr std::size_t kChannels = 3;
constexpr int kThreadsPerBlock = 256;
constexpr int kMaximumBlocks = 4096;
constexpr std::array<float, kChannels> kMean{0.485F, 0.456F, 0.406F};
constexpr std::array<float, kChannels> kStandardDeviation{0.229F, 0.224F, 0.225F};

struct Options {
  std::size_t width{1280};
  std::size_t height{720};
  int iterations{100};
};

void print_usage(const char* executable) {
  std::cout << "Usage: " << executable
            << " [--width N] [--height N] [--iterations N]\n";
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
    if (argument == "--width") {
      options.width = adtrl::cuda::parse_positive_size(argv[++index], "--width");
    } else if (argument == "--height") {
      options.height = adtrl::cuda::parse_positive_size(argv[++index], "--height");
    } else if (argument == "--iterations") {
      options.iterations = adtrl::cuda::parse_positive_int(argv[++index], "--iterations");
    } else {
      throw std::invalid_argument("unknown option: " + argument);
    }
  }
  return options;
}

__global__ void normalize_rgb_u8_hwc_to_f32_chw_kernel(const std::uint8_t* input,
                                                        float* output,
                                                        const std::size_t pixel_count,
                                                        const std::size_t value_count,
                                                        const float mean_red,
                                                        const float mean_green,
                                                        const float mean_blue,
                                                        const float inv_std_red,
                                                        const float inv_std_green,
                                                        const float inv_std_blue) {
  const std::size_t start = static_cast<std::size_t>(blockIdx.x) * blockDim.x + threadIdx.x;
  const std::size_t stride = static_cast<std::size_t>(blockDim.x) * gridDim.x;

  for (std::size_t input_index = start; input_index < value_count; input_index += stride) {
    const std::size_t pixel = input_index / kChannels;
    const std::size_t channel = input_index % kChannels;
    const float scaled = static_cast<float>(input[input_index]) / 255.0F;

    float mean = mean_blue;
    float inverse_standard_deviation = inv_std_blue;
    if (channel == 0U) {
      mean = mean_red;
      inverse_standard_deviation = inv_std_red;
    } else if (channel == 1U) {
      mean = mean_green;
      inverse_standard_deviation = inv_std_green;
    }

    output[channel * pixel_count + pixel] = (scaled - mean) * inverse_standard_deviation;
  }
}

int block_count_for(const std::size_t values) {
  const std::size_t required = (values + kThreadsPerBlock - 1U) / kThreadsPerBlock;
  return static_cast<int>(std::min<std::size_t>(required, kMaximumBlocks));
}

}  // namespace

int main(const int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const std::size_t pixels =
        adtrl::cuda::checked_product(options.width, options.height, "image pixel");
    const std::size_t values = adtrl::cuda::checked_product(pixels, kChannels, "image value");
    adtrl::cuda::print_device_banner();

    std::vector<std::uint8_t> input(values);
    std::vector<float> expected(values);
    std::vector<float> actual(values);

    for (std::size_t pixel = 0; pixel < pixels; ++pixel) {
      for (std::size_t channel = 0; channel < kChannels; ++channel) {
        const std::size_t input_index = pixel * kChannels + channel;
        input[input_index] = static_cast<std::uint8_t>((pixel * 17U + channel * 53U) % 256U);
        const float scaled = static_cast<float>(input[input_index]) / 255.0F;
        expected[channel * pixels + pixel] =
            (scaled - kMean[channel]) / kStandardDeviation[channel];
      }
    }

    adtrl::cuda::Stream stream;
    adtrl::cuda::DeviceBuffer<std::uint8_t> device_input(values);
    adtrl::cuda::DeviceBuffer<float> device_output(values);
    device_input.copy_from_host_async(input.data(), input.size(), stream.get());
    stream.synchronize();

    const int blocks = block_count_for(values);
    const auto launch = [&] {
      normalize_rgb_u8_hwc_to_f32_chw_kernel<<<blocks, kThreadsPerBlock, 0, stream.get()>>>(
          device_input.get(),
          device_output.get(),
          pixels,
          values,
          kMean[0],
          kMean[1],
          kMean[2],
          1.0F / kStandardDeviation[0],
          1.0F / kStandardDeviation[1],
          1.0F / kStandardDeviation[2]);
      ADTRL_CUDA_CHECK(cudaGetLastError());
    };

    launch();
    stream.synchronize();
    const float average_kernel_ms =
        adtrl::cuda::benchmark_kernel_ms(options.iterations, stream.get(), launch);

    device_output.copy_to_host_async(actual.data(), actual.size(), stream.get());
    stream.synchronize();

    const adtrl::cuda::ValidationResult validation =
        adtrl::cuda::validate_near(expected, actual, 2.0e-6, 2.0e-6);

    std::cout << "experiment=image_normalize input_layout=HWC output_layout=CHW width="
              << options.width << " height=" << options.height << " channels=" << kChannels
              << " iterations=" << options.iterations << '\n';
    std::cout << "operation=uint8_to_float_scale_imagenet_normalize blocks=" << blocks
              << " threads_per_block=" << kThreadsPerBlock << '\n';
    std::cout << "timing_scope=kernel_only cuda_event_average_ms=" << average_kernel_ms << '\n';
    adtrl::cuda::print_validation(validation);
    return validation.passed ? EXIT_SUCCESS : EXIT_FAILURE;
  } catch (const std::exception& error) {
    std::cerr << "image_normalize failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
