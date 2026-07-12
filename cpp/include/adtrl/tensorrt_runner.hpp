#pragma once

#include <cuda_runtime_api.h>

#include <cstddef>
#include <cstdint>
#include <string>
#include <string_view>
#include <vector>

namespace adtrl::tensorrt {

enum class TensorDirection { kInput, kOutput };

enum class ElementType { kFloat32, kFloat16, kInt8, kInt32, kBool, kUnknown };

struct TensorSpec {
  std::string name;
  TensorDirection direction{TensorDirection::kInput};
  ElementType element_type{ElementType::kUnknown};
  std::vector<std::int64_t> shape;
  bool has_dynamic_dimension{false};
};

struct DeviceTensorView {
  std::string_view name;
  void* device_address{nullptr};
  std::size_t bytes{0};
};

// Contract for the future tested TensorRT adapter.
//
// This repository intentionally exposes no concrete runner yet. A concrete
// implementation must define ownership for IRuntime/ICudaEngine/
// IExecutionContext, validate dynamic shapes and buffer sizes, and document
// which TensorRT version and GPU it was tested on before it can claim working
// inference.
class ITensorRTRunner {
 public:
  virtual ~ITensorRTRunner() = default;

  ITensorRTRunner(const ITensorRTRunner&) = delete;
  ITensorRTRunner& operator=(const ITensorRTRunner&) = delete;
  ITensorRTRunner(ITensorRTRunner&&) = delete;
  ITensorRTRunner& operator=(ITensorRTRunner&&) = delete;

  virtual void load_serialized_engine(const std::string& engine_path) = 0;
  [[nodiscard]] virtual const std::vector<TensorSpec>& tensors() const noexcept = 0;
  virtual void set_input_shape(std::string_view tensor_name,
                               const std::vector<std::int64_t>& shape) = 0;
  virtual void bind_device_tensor(const DeviceTensorView& tensor) = 0;
  [[nodiscard]] virtual bool enqueue(cudaStream_t stream) = 0;

 protected:
  ITensorRTRunner() = default;
};

}  // namespace adtrl::tensorrt
