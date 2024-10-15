// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from fsrobo_a1_msg_srv_4py:msg/ArmAngle.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__STRUCT_HPP_
#define FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__fsrobo_a1_msg_srv_4py__msg__ArmAngle __attribute__((deprecated))
#else
# define DEPRECATED__fsrobo_a1_msg_srv_4py__msg__ArmAngle __declspec(deprecated)
#endif

namespace fsrobo_a1_msg_srv_4py
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ArmAngle_
{
  using Type = ArmAngle_<ContainerAllocator>;

  explicit ArmAngle_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit ArmAngle_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _angle_type =
    std::vector<float, typename ContainerAllocator::template rebind<float>::other>;
  _angle_type angle;

  // setters for named parameter idiom
  Type & set__angle(
    const std::vector<float, typename ContainerAllocator::template rebind<float>::other> & _arg)
  {
    this->angle = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator> *;
  using ConstRawPtr =
    const fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__fsrobo_a1_msg_srv_4py__msg__ArmAngle
    std::shared_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__fsrobo_a1_msg_srv_4py__msg__ArmAngle
    std::shared_ptr<fsrobo_a1_msg_srv_4py::msg::ArmAngle_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ArmAngle_ & other) const
  {
    if (this->angle != other.angle) {
      return false;
    }
    return true;
  }
  bool operator!=(const ArmAngle_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ArmAngle_

// alias to use template instance with default allocator
using ArmAngle =
  fsrobo_a1_msg_srv_4py::msg::ArmAngle_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace fsrobo_a1_msg_srv_4py

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__STRUCT_HPP_
