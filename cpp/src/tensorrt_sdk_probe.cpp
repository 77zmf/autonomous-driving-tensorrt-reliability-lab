#include "adtrl/tensorrt_runner.hpp"

#include <NvInferRuntime.h>
#include <NvInferVersion.h>
#include <cuda_runtime_api.h>

#include <cstdlib>
#include <iostream>

int main() {
  const int linked_version = nvinfer1::getInferLibVersion();
  std::cout << "TensorRT headers=" << NV_TENSORRT_MAJOR << '.' << NV_TENSORRT_MINOR << '.'
            << NV_TENSORRT_PATCH << '.' << NV_TENSORRT_BUILD << '\n';
  std::cout << "TensorRT linked_library_encoded_version=" << linked_version << '\n';
  std::cout << "CUDA runtime headers=" << CUDART_VERSION << '\n';
  std::cout << "runner_status=interface_only concrete_implementation=not_yet_validated\n";
  return linked_version > 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
