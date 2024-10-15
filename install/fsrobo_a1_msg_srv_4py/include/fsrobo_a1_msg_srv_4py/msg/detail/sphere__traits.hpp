// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from fsrobo_a1_msg_srv_4py:msg/Sphere.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__TRAITS_HPP_
#define FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__TRAITS_HPP_

#include "fsrobo_a1_msg_srv_4py/msg/detail/sphere__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'center'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fsrobo_a1_msg_srv_4py::msg::Sphere>()
{
  return "fsrobo_a1_msg_srv_4py::msg::Sphere";
}

template<>
inline const char * name<fsrobo_a1_msg_srv_4py::msg::Sphere>()
{
  return "fsrobo_a1_msg_srv_4py/msg/Sphere";
}

template<>
struct has_fixed_size<fsrobo_a1_msg_srv_4py::msg::Sphere>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value> {};

template<>
struct has_bounded_size<fsrobo_a1_msg_srv_4py::msg::Sphere>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value> {};

template<>
struct is_message<fsrobo_a1_msg_srv_4py::msg::Sphere>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__TRAITS_HPP_
