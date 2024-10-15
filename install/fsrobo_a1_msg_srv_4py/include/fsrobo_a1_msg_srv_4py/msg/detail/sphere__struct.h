// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from fsrobo_a1_msg_srv_4py:msg/Sphere.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__STRUCT_H_
#define FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'center'
#include "geometry_msgs/msg/detail/point__struct.h"

// Struct defined in msg/Sphere in the package fsrobo_a1_msg_srv_4py.
typedef struct fsrobo_a1_msg_srv_4py__msg__Sphere
{
  geometry_msgs__msg__Point center;
  double radius;
} fsrobo_a1_msg_srv_4py__msg__Sphere;

// Struct for a sequence of fsrobo_a1_msg_srv_4py__msg__Sphere.
typedef struct fsrobo_a1_msg_srv_4py__msg__Sphere__Sequence
{
  fsrobo_a1_msg_srv_4py__msg__Sphere * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} fsrobo_a1_msg_srv_4py__msg__Sphere__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__DETAIL__SPHERE__STRUCT_H_
