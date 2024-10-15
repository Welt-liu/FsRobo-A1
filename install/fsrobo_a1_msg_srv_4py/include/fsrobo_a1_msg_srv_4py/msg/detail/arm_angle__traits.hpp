// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from fsrobo_a1_msg_srv_4py:msg/ArmAngle.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__TRAITS_HPP_
#define FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__TRAITS_HPP_

#include "fsrobo_a1_msg_srv_4py/msg/detail/arm_angle__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fsrobo_a1_msg_srv_4py::msg::ArmAngle>()
{
  return "fsrobo_a1_msg_srv_4py::msg::ArmAngle";
}

template<>
inline const char * name<fsrobo_a1_msg_srv_4py::msg::ArmAngle>()
{
  return "fsrobo_a1_msg_srv_4py/msg/ArmAngle";
}

template<>
struct has_fixed_size<fsrobo_a1_msg_srv_4py::msg::ArmAngle>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<fsrobo_a1_msg_srv_4py::msg::ArmAngle>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<fsrobo_a1_msg_srv_4py::msg::ArmAngle>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__TRAITS_HPP_
