#include "adtrl/unique_resource.hpp"

#include <cstdlib>
#include <iostream>
#include <utility>

namespace {

struct CountingDeleter {
  int* calls;
  int* last_resource;

  void operator()(const int resource) const noexcept {
    ++(*calls);
    *last_resource = resource;
  }
};

bool expect(const bool condition, const char* message) {
  if (!condition) {
    std::cerr << "FAIL: " << message << '\n';
  }
  return condition;
}

}  // namespace

int main() {
  int delete_calls = 0;
  int last_deleted = 0;
  CountingDeleter deleter{&delete_calls, &last_deleted};

  {
    auto first = adtrl::make_unique_resource(7, deleter);
    if (!expect(static_cast<bool>(first), "new resource should be owned")) {
      return EXIT_FAILURE;
    }

    auto second = std::move(first);
    if (!expect(!static_cast<bool>(first), "moved-from resource should not be owned") ||
        !expect(static_cast<bool>(second), "moved-to resource should be owned")) {
      return EXIT_FAILURE;
    }

    second.reset();
    second.reset();
    if (!expect(delete_calls == 1, "reset should delete exactly once") ||
        !expect(last_deleted == 7, "deleter should receive the owned handle")) {
      return EXIT_FAILURE;
    }
  }

  {
    auto released_owner = adtrl::make_unique_resource(11, deleter);
    const int released = released_owner.release();
    if (!expect(released == 11, "release should return the handle") ||
        !expect(!static_cast<bool>(released_owner), "released handle should not remain owned") ||
        !expect(delete_calls == 1, "released handle must not be deleted by the wrapper")) {
      return EXIT_FAILURE;
    }
  }

  {
    auto left = adtrl::make_unique_resource(13, deleter);
    auto right = adtrl::make_unique_resource(17, deleter);
    right = std::move(left);
    if (!expect(delete_calls == 2, "move assignment should clean the previous target") ||
        !expect(last_deleted == 17, "move assignment should delete the replaced handle")) {
      return EXIT_FAILURE;
    }
  }

  if (!expect(delete_calls == 3, "final owned handle should be deleted at scope exit") ||
      !expect(last_deleted == 13, "scope-exit deleter should receive the moved handle")) {
    return EXIT_FAILURE;
  }

  std::cout << "unique_resource correctness=PASS delete_calls=" << delete_calls << '\n';
  return EXIT_SUCCESS;
}
