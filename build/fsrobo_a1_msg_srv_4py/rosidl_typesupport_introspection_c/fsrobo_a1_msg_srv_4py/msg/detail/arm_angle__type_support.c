// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from fsrobo_a1_msg_srv_4py:msg/ArmAngle.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "fsrobo_a1_msg_srv_4py/msg/detail/arm_angle__rosidl_typesupport_introspection_c.h"
#include "fsrobo_a1_msg_srv_4py/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "fsrobo_a1_msg_srv_4py/msg/detail/arm_angle__functions.h"
#include "fsrobo_a1_msg_srv_4py/msg/detail/arm_angle__struct.h"


// Include directives for member types
// Member `angle`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  fsrobo_a1_msg_srv_4py__msg__ArmAngle__init(message_memory);
}

void ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_fini_function(void * message_memory)
{
  fsrobo_a1_msg_srv_4py__msg__ArmAngle__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_member_array[1] = {
  {
    "angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(fsrobo_a1_msg_srv_4py__msg__ArmAngle, angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_members = {
  "fsrobo_a1_msg_srv_4py__msg",  // message namespace
  "ArmAngle",  // message name
  1,  // number of fields
  sizeof(fsrobo_a1_msg_srv_4py__msg__ArmAngle),
  ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_member_array,  // message members
  ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_init_function,  // function to initialize message memory (memory has to be allocated)
  ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_type_support_handle = {
  0,
  &ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_fsrobo_a1_msg_srv_4py
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, fsrobo_a1_msg_srv_4py, msg, ArmAngle)() {
  if (!ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_type_support_handle.typesupport_identifier) {
    ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ArmAngle__rosidl_typesupport_introspection_c__ArmAngle_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
