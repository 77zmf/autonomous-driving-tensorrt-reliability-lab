#pragma once

#include <type_traits>
#include <utility>

namespace adtrl {

// Minimal move-only ownership for handles whose cleanup is expressed by a
// callable. The explicit ownership bit avoids assuming that every resource
// type uses nullptr, zero, or another universal invalid sentinel.
template <typename Resource, typename Deleter>
class UniqueResource final {
 public:
  static_assert(std::is_nothrow_move_constructible<Resource>::value,
                "Resource must be nothrow move constructible");
  static_assert(std::is_nothrow_move_assignable<Resource>::value,
                "Resource must be nothrow move assignable");
  static_assert(std::is_nothrow_move_constructible<Deleter>::value,
                "Deleter must be nothrow move constructible");
  static_assert(std::is_nothrow_move_assignable<Deleter>::value,
                "Deleter must be nothrow move assignable");
  static_assert(std::is_nothrow_invocable<Deleter&, Resource&>::value,
                "Deleter must be noexcept when invoked with the resource");

  UniqueResource(Resource resource, Deleter deleter)
      : resource_(std::move(resource)), deleter_(std::move(deleter)), owns_(true) {}

  ~UniqueResource() noexcept { reset(); }

  UniqueResource(const UniqueResource&) = delete;
  UniqueResource& operator=(const UniqueResource&) = delete;

  UniqueResource(UniqueResource&& other) noexcept
      : resource_(std::move(other.resource_)),
        deleter_(std::move(other.deleter_)),
        owns_(std::exchange(other.owns_, false)) {}

  UniqueResource& operator=(UniqueResource&& other) noexcept {
    if (this != &other) {
      reset();
      resource_ = std::move(other.resource_);
      deleter_ = std::move(other.deleter_);
      owns_ = std::exchange(other.owns_, false);
    }
    return *this;
  }

  [[nodiscard]] Resource& get() noexcept { return resource_; }
  [[nodiscard]] const Resource& get() const noexcept { return resource_; }
  [[nodiscard]] explicit operator bool() const noexcept { return owns_; }

  Resource release() noexcept {
    owns_ = false;
    return std::move(resource_);
  }

  void reset() noexcept {
    if (owns_) {
      deleter_(resource_);
      owns_ = false;
    }
  }

 private:
  Resource resource_;
  Deleter deleter_;
  bool owns_{false};
};

template <typename Resource, typename Deleter>
UniqueResource<Resource, Deleter> make_unique_resource(Resource resource, Deleter deleter) {
  return UniqueResource<Resource, Deleter>(std::move(resource), std::move(deleter));
}

}  // namespace adtrl
