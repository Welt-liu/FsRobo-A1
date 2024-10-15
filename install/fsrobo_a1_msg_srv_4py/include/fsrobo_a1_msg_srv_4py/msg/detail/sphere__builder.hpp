// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from fsrobo_a1_msg_srv_4py:msg/Sphere.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__BUILDER_HPP_
#define FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__BUILDER_HPP_

#include "fsrobo_a1_msg_srv_4py/msg/detail/sphere__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace fsrobo_a1_msg_srv_4py
{

namespace msg
{

namespace builder
{

class Init_Sphere_radius
{
public:
  explicit Init_Sphere_radius(::fsrobo_a1_msg_srv_4py::msg::Sphere & msg)
  : msg_(msg)
  {}
  ::fsrobo_a1_msg_srv_4py::msg::Sphere radius(::fsrobo_a1_msg_srv_4py::msg::Sphere::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return std::move(msg_);
  }

private:
  ::fsrobo_a1_msg_srv_4py::msg::Sphere msg_;
};

class Init_Sphere_center
{
public:
  Init_Sphere_center()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Sphere_radius center(::fsrobo_a1_msg_srv_4py::msg::Sphere::_center_type arg)
  {
    msg_.center = std::move(arg);
    return Init_Sphere_radius(msg_);
  }

private:
  ::fsrobo_a1_msg_srv_4py::msg::Sphere msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::fsrobo_a1_msg_srv_4py::msg::Sphere>()
{
  return fsrobo_a1_msg_srv_4py::msg::builder::Init_Sphere_center();
}

}  // namespace fsrobo_a1_msg_srv_4py

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__BUILDER_HPP_
