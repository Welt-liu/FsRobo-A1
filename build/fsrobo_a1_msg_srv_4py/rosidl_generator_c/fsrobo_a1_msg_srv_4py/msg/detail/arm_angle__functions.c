// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from fsrobo_a1_msg_srv_4py:msg/ArmAngle.idl
// generated code does not contain a copyright notice
#include "fsrobo_a1_msg_srv_4py/msg/detail/arm_angle__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `angle`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
fsrobo_a1_msg_srv_4py__msg__ArmAngle__init(fsrobo_a1_msg_srv_4py__msg__ArmAngle * msg)
{
  if (!msg) {
    return false;
  }
  // angle
  if (!rosidl_runtime_c__float__Sequence__init(&msg->angle, 0)) {
    fsrobo_a1_msg_srv_4py__msg__ArmAngle__fini(msg);
    return false;
  }
  return true;
}

void
fsrobo_a1_msg_srv_4py__msg__ArmAngle__fini(fsrobo_a1_msg_srv_4py__msg__ArmAngle * msg)
{
  if (!msg) {
    return;
  }
  // angle
  rosidl_runtime_c__float__Sequence__fini(&msg->angle);
}

bool
fsrobo_a1_msg_srv_4py__msg__ArmAngle__are_equal(const fsrobo_a1_msg_srv_4py__msg__ArmAngle * lhs, const fsrobo_a1_msg_srv_4py__msg__ArmAngle * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // angle
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->angle), &(rhs->angle)))
  {
    return false;
  }
  return true;
}

bool
fsrobo_a1_msg_srv_4py__msg__ArmAngle__copy(
  const fsrobo_a1_msg_srv_4py__msg__ArmAngle * input,
  fsrobo_a1_msg_srv_4py__msg__ArmAngle * output)
{
  if (!input || !output) {
    return false;
  }
  // angle
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->angle), &(output->angle)))
  {
    return false;
  }
  return true;
}

fsrobo_a1_msg_srv_4py__msg__ArmAngle *
fsrobo_a1_msg_srv_4py__msg__ArmAngle__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  fsrobo_a1_msg_srv_4py__msg__ArmAngle * msg = (fsrobo_a1_msg_srv_4py__msg__ArmAngle *)allocator.allocate(sizeof(fsrobo_a1_msg_srv_4py__msg__ArmAngle), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(fsrobo_a1_msg_srv_4py__msg__ArmAngle));
  bool success = fsrobo_a1_msg_srv_4py__msg__ArmAngle__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
fsrobo_a1_msg_srv_4py__msg__ArmAngle__destroy(fsrobo_a1_msg_srv_4py__msg__ArmAngle * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    fsrobo_a1_msg_srv_4py__msg__ArmAngle__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__init(fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  fsrobo_a1_msg_srv_4py__msg__ArmAngle * data = NULL;

  if (size) {
    data = (fsrobo_a1_msg_srv_4py__msg__ArmAngle *)allocator.zero_allocate(size, sizeof(fsrobo_a1_msg_srv_4py__msg__ArmAngle), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = fsrobo_a1_msg_srv_4py__msg__ArmAngle__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        fsrobo_a1_msg_srv_4py__msg__ArmAngle__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__fini(fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      fsrobo_a1_msg_srv_4py__msg__ArmAngle__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence *
fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * array = (fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence *)allocator.allocate(sizeof(fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__destroy(fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__are_equal(const fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * lhs, const fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!fsrobo_a1_msg_srv_4py__msg__ArmAngle__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence__copy(
  const fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * input,
  fsrobo_a1_msg_srv_4py__msg__ArmAngle__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(fsrobo_a1_msg_srv_4py__msg__ArmAngle);
    fsrobo_a1_msg_srv_4py__msg__ArmAngle * data =
      (fsrobo_a1_msg_srv_4py__msg__ArmAngle *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!fsrobo_a1_msg_srv_4py__msg__ArmAngle__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          fsrobo_a1_msg_srv_4py__msg__ArmAngle__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!fsrobo_a1_msg_srv_4py__msg__ArmAngle__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
