# Find the NVIDIA TensorRT runtime SDK.
#
# Hints:
#   TensorRT_ROOT (CMake variable or environment variable)
#   TENSORRT_ROOT (environment variable)
#
# Result variables:
#   TensorRT_FOUND
#   TensorRT_VERSION
#   TensorRT_INCLUDE_DIR
#   TensorRT_NVINFER_LIBRARY
#
# Imported target:
#   TensorRT::nvinfer

set(_TensorRT_HINTS
  "${TensorRT_ROOT}"
  "$ENV{TensorRT_ROOT}"
  "$ENV{TENSORRT_ROOT}"
)

find_path(
  TensorRT_INCLUDE_DIR
  NAMES NvInfer.h NvInferVersion.h
  HINTS ${_TensorRT_HINTS}
  PATH_SUFFIXES include include/x86_64-linux-gnu
)

find_library(
  TensorRT_NVINFER_LIBRARY
  NAMES nvinfer
  HINTS ${_TensorRT_HINTS}
  PATH_SUFFIXES lib lib64 lib/x86_64-linux-gnu
)

if(TensorRT_INCLUDE_DIR AND EXISTS "${TensorRT_INCLUDE_DIR}/NvInferVersion.h")
  file(STRINGS "${TensorRT_INCLUDE_DIR}/NvInferVersion.h" _TensorRT_VERSION_LINES
    REGEX "^#define NV_TENSORRT_(MAJOR|MINOR|PATCH|BUILD) [0-9]+")

  foreach(_component MAJOR MINOR PATCH BUILD)
    string(REGEX MATCH
      "#define NV_TENSORRT_${_component} ([0-9]+)"
      _match
      "${_TensorRT_VERSION_LINES}")
    if(CMAKE_MATCH_1)
      set(_TensorRT_VERSION_${_component} "${CMAKE_MATCH_1}")
    else()
      set(_TensorRT_VERSION_${_component} 0)
    endif()
  endforeach()

  set(TensorRT_VERSION
    "${_TensorRT_VERSION_MAJOR}.${_TensorRT_VERSION_MINOR}.${_TensorRT_VERSION_PATCH}.${_TensorRT_VERSION_BUILD}")
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
  TensorRT
  REQUIRED_VARS TensorRT_INCLUDE_DIR TensorRT_NVINFER_LIBRARY
  VERSION_VAR TensorRT_VERSION
)

if(TensorRT_FOUND AND NOT TARGET TensorRT::nvinfer)
  add_library(TensorRT::nvinfer UNKNOWN IMPORTED)
  set_target_properties(
    TensorRT::nvinfer
    PROPERTIES
      IMPORTED_LOCATION "${TensorRT_NVINFER_LIBRARY}"
      INTERFACE_INCLUDE_DIRECTORIES "${TensorRT_INCLUDE_DIR}"
  )
endif()

mark_as_advanced(TensorRT_INCLUDE_DIR TensorRT_NVINFER_LIBRARY)
