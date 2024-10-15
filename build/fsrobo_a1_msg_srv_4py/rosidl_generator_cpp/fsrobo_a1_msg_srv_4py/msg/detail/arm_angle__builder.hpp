// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from fsrobo_a1_msg_srv_4py:msg/ArmAngle.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__BUILDER_HPP_
#define FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__BUILDER_HPP_

#include "fsrobo_a1_msg_srv_4py/msg/detail/arm_angle__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace fsrobo_a1_msg_srv_4py
{

namespace msg
{

namespace builder
{

class Init_ArmAngle_angle
{
public:
  Init_ArmAngle_angle()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::fsrobo_a1_msg_srv_4py::msg::ArmAngle angle(::fsrobo_a1_msg_srv_4py::msg::ArmAngle::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::fsrobo_a1_msg_srv_4py::msg::ArmAngle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::fsrobo_a1_msg_srv_4py::msg::ArmAngle>()
{
  return fsrobo_a1_msg_srv_4py::msg::builder::Init_ArmAngle_angle();
}

}  // namespace fsrobo_a1_msg_srv_4py

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__BUILDER_HPP_
