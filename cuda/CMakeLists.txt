add_library(adtrl_cuda_support INTERFACE)
target_include_directories(
  adtrl_cuda_support
  INTERFACE
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
target_compile_features(adtrl_cuda_support INTERFACE cxx_std_17)
target_link_libraries(adtrl_cuda_support INTERFACE CUDA::cudart)

function(adtrl_add_cuda_experiment target source)
  add_executable(${target} ${source})
  target_link_libraries(${target} PRIVATE adtrl_cuda_support)
  set_target_properties(
    ${target}
    PROPERTIES
      CUDA_STANDARD 17
      CUDA_STANDARD_REQUIRED ON
      CUDA_EXTENSIONS OFF
      CUDA_SEPARABLE_COMPILATION OFF
  )

  if(MSVC)
    target_compile_options(${target} PRIVATE $<$<COMPILE_LANGUAGE:CXX>:/W4>)
  else()
    target_compile_options(
      ${target}
      PRIVATE
        $<$<COMPILE_LANGUAGE:CXX>:-Wall;-Wextra;-Wpedantic>
        $<$<COMPILE_LANGUAGE:CUDA>:-Xcompiler=-Wall,-Wextra,-Wpedantic>
    )
  endif()
endfunction()

adtrl_add_cuda_experiment(cuda_vector_add vector_add.cu)
adtrl_add_cuda_experiment(cuda_reduction reduction.cu)
adtrl_add_cuda_experiment(cuda_image_normalize image_normalize.cu)

if(TRT_LAB_BUILD_TESTS)
  add_test(NAME cuda_vector_add_correctness
    COMMAND cuda_vector_add --elements 65537 --iterations 3)
  add_test(NAME cuda_reduction_correctness
    COMMAND cuda_reduction --elements 65537 --iterations 3)
  add_test(NAME cuda_image_normalize_correctness
    COMMAND cuda_image_normalize --width 321 --height 181 --iterations 3)
endif()
