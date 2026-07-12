.PHONY: check test-python configure-cpu build-cpu test-cpu clean

BUILD_DIR ?= build/cpu
PYTHON ?= python3

test-python:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

configure-cpu:
	cmake -S . -B $(BUILD_DIR) \
		-DTRT_LAB_ENABLE_CUDA=OFF \
		-DTRT_LAB_ENABLE_TENSORRT=OFF \
		-DTRT_LAB_BUILD_TESTS=ON

build-cpu: configure-cpu
	cmake --build $(BUILD_DIR)

test-cpu: build-cpu
	ctest --test-dir $(BUILD_DIR) --output-on-failure

check: test-python test-cpu
	bash -n scripts/check_environment.sh scripts/run_cpu_checks.sh
	$(PYTHON) -m compileall -q src tests scripts
	$(PYTHON) scripts/capture_environment.py >/dev/null

clean:
	cmake -E remove_directory build
