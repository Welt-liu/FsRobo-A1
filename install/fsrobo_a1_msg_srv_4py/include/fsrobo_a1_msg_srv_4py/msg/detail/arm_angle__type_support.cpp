// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from fsrobo_a1_msg_srv_4py:msg/ArmAngle.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "fsrobo_a1_msg_srv_4py/msg/detail/arm_angle__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace fsrobo_a1_msg_srv_4py
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ArmAngle_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) fsrobo_a1_msg_srv_4py::msg::ArmAngle(_init);
}

void ArmAngle_fini_function(void * message_memory)
{
  auto typed_message = static_cast<fsrobo_a1_msg_srv_4py::msg::ArmAngle *>(message_memory);
  typed_message->~ArmAngle();
}

size_t size_function__ArmAngle__angle(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ArmAngle__angle(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__ArmAngle__angle(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void resize_function__ArmAngle__angle(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ArmAngle_message_member_array[1] = {
  {
    "angle",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(fsrobo_a1_msg_srv_4py::msg::ArmAngle, angle),  // bytes offset in struct
    nullptr,  // default value
    size_function__ArmAngle__angle,  // size() function pointer
    get_const_function__ArmAngle__angle,  // get_const(index) function pointer
    get_function__ArmAngle__angle,  // get(index) function pointer
    resize_function__ArmAngle__angle  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ArmAngle_message_members = {
  "fsrobo_a1_msg_srv_4py::msg",  // message namespace
  "ArmAngle",  // message name
  1,  // number of fields
  sizeof(fsrobo_a1_msg_srv_4py::msg::ArmAngle),
  ArmAngle_message_member_array,  // message members
  ArmAngle_init_function,  // function to initialize message memory (memory has to be allocated)
  ArmAngle_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ArmAngle_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ArmAngle_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace fsrobo_a1_msg_srv_4py


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<fsrobo_a1_msg_srv_4py::msg::ArmAngle>()
{
  return &::fsrobo_a1_msg_srv_4py::msg::rosidl_typesupport_introspection_cpp::ArmAngle_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, fsrobo_a1_msg_srv_4py, msg, ArmAngle)() {
  return &::fsrobo_a1_msg_srv_4py::msg::rosidl_typesupport_introspection_cpp::ArmAngle_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
