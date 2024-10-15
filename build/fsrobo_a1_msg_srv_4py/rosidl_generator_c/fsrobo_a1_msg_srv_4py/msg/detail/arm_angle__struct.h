// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from fsrobo_a1_msg_srv_4py:msg/ArmAngle.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__STRUCT_H_
#define FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'angle'
#include "rosidl_runtime_c/primitives_sequence.h"

// Struct defined in msg/ArmAngle in the package fsrobo_a1_msg_srv_4py.
typedef struct fsrobo_a1_msg_srv_4py__msg__ArmAngle
{
  rosidl_runtime_c__float__Sequence angle;
} fsrobo_a1_msg_srv_4py__msg__ArmAngle;

// Struct for a sequence of fsrobo_a1_msg_srv_4py__msg__ArmAngle.
typedef struct fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence
{
  fsrobo_a1_msg_srv_4py__msg__ArmAngle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__ARM_ANGLE__STRUCT_H_
