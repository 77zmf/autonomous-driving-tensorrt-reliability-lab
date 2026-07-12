add_library(adtrl_cpp_support INTERFACE)
target_include_directories(adtrl_cpp_support INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_compile_features(adtrl_cpp_support INTERFACE cxx_std_17)

if(TRT_LAB_BUILD_TESTS)
  add_executable(cpp_unique_resource_test tests/unique_resource_test.cpp)
  target_link_libraries(cpp_unique_resource_test PRIVATE adtrl_cpp_support)
  add_test(NAME cpp_unique_resource COMMAND cpp_unique_resource_test)

  if(MSVC)
    target_compile_options(cpp_unique_resource_test PRIVATE /W4)
  else()
    target_compile_options(cpp_unique_resource_test PRIVATE -Wall -Wextra -Wpedantic -Werror)
  endif()
endif()

if(ADTRL_TENSORRT_AVAILABLE)
  add_library(adtrl_tensorrt_runner INTERFACE)
  target_link_libraries(adtrl_tensorrt_runner INTERFACE adtrl_cpp_support)
  target_compile_definitions(adtrl_tensorrt_runner INTERFACE ADTRL_HAS_TENSORRT=1)
  target_link_libraries(
    adtrl_tensorrt_runner
    INTERFACE
      TensorRT::nvinfer
      CUDA::cudart
  )

  # This probe proves that the discovered headers and shared library agree. It is
  # deliberately not presented as a working inference implementation.
  add_executable(tensorrt_sdk_probe src/tensorrt_sdk_probe.cpp)
  target_link_libraries(tensorrt_sdk_probe PRIVATE adtrl_tensorrt_runner)

  if(MSVC)
    target_compile_options(tensorrt_sdk_probe PRIVATE /W4)
  else()
    target_compile_options(tensorrt_sdk_probe PRIVATE -Wall -Wextra -Wpedantic)
  endif()
endif()
