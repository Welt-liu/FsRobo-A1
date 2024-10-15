// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from fsrobo_a1_msg_srv_4py:srv/AddThreeInts.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__SRV__DETAIL__ADD_THREE_INTS__TRAITS_HPP_
#define FSROBO_A1_MSG_SRV_4PY__SRV__DETAIL__ADD_THREE_INTS__TRAITS_HPP_

#include "fsrobo_a1_msg_srv_4py/srv/detail/add_three_ints__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>()
{
  return "fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request";
}

template<>
inline const char * name<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>()
{
  return "fsrobo_a1_msg_srv_4py/srv/AddThreeInts_Request";
}

template<>
struct has_fixed_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>()
{
  return "fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response";
}

template<>
inline const char * name<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>()
{
  return "fsrobo_a1_msg_srv_4py/srv/AddThreeInts_Response";
}

template<>
struct has_fixed_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fsrobo_a1_msg_srv_4py::srv::AddThreeInts>()
{
  return "fsrobo_a1_msg_srv_4py::srv::AddThreeInts";
}

template<>
inline const char * name<fsrobo_a1_msg_srv_4py::srv::AddThreeInts>()
{
  return "fsrobo_a1_msg_srv_4py/srv/AddThreeInts";
}

template<>
struct has_fixed_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts>
  : std::integral_constant<
    bool,
    has_fixed_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>::value &&
    has_fixed_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>::value
  >
{
};

template<>
struct has_bounded_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts>
  : std::integral_constant<
    bool,
    has_bounded_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>::value &&
    has_bounded_size<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>::value
  >
{
};

template<>
struct is_service<fsrobo_a1_msg_srv_4py::srv::AddThreeInts>
  : std::true_type
{
};

template<>
struct is_service_request<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>
  : std::true_type
{
};

template<>
struct is_service_response<fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // FSROBO_A1_MSG_SRV_4PY__SRV__DETAIL__ADD_THREE_INTS__TRAITS_HPP_
