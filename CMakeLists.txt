cmake_minimum_required(VERSION 3.24)

project(
  autonomous_driving_tensorrt_reliability_lab
  VERSION 0.1.0
  DESCRIPTION "Reproducible CUDA and TensorRT reliability experiments"
  LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(TRT_LAB_ENABLE_CUDA "Build CUDA experiments when a CUDA compiler is available" ON)
option(TRT_LAB_ENABLE_TENSORRT "Build the TensorRT interface probe when the SDK is available" ON)
option(TRT_LAB_BUILD_TESTS "Register available correctness checks with CTest" OFF)

if(TRT_LAB_BUILD_TESTS)
  include(CTest)
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

set(ADTRL_CUDA_AVAILABLE OFF)
set(ADTRL_TENSORRT_AVAILABLE OFF)

if(TRT_LAB_ENABLE_CUDA)
  include(CheckLanguage)
  check_language(CUDA)

  if(CMAKE_CUDA_COMPILER)
    enable_language(CUDA)
    find_package(CUDAToolkit REQUIRED)

    set(CMAKE_CUDA_STANDARD 17)
    set(CMAKE_CUDA_STANDARD_REQUIRED ON)
    set(CMAKE_CUDA_EXTENSIONS OFF)
    set(ADTRL_CUDA_AVAILABLE ON)

    add_subdirectory(cuda)
  else()
    message(STATUS "CUDA compiler not found; CUDA experiments are skipped.")
  endif()
else()
  message(STATUS "CUDA experiments disabled by TRT_LAB_ENABLE_CUDA=OFF.")
endif()

if(TRT_LAB_ENABLE_TENSORRT)
  if(ADTRL_CUDA_AVAILABLE)
    find_package(TensorRT QUIET)
    if(TensorRT_FOUND)
      message(STATUS "TensorRT ${TensorRT_VERSION} found; enabling SDK probe and runner interface.")
      set(ADTRL_TENSORRT_AVAILABLE ON)
    else()
      message(STATUS "TensorRT SDK not found; TensorRT targets are skipped.")
    endif()
  else()
    message(STATUS "TensorRT targets require CUDA and are skipped.")
  endif()
endif()

add_subdirectory(cpp)
