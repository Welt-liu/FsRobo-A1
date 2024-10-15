// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from fsrobo_a1_msg_srv_4py:srv/AddThreeInts.idl
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__SRV__DETAIL__ADD_THREE_INTS__BUILDER_HPP_
#define FSROBO_A1_MSG_SRV_4PY__SRV__DETAIL__ADD_THREE_INTS__BUILDER_HPP_

#include "fsrobo_a1_msg_srv_4py/srv/detail/add_three_ints__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace fsrobo_a1_msg_srv_4py
{

namespace srv
{

namespace builder
{

class Init_AddThreeInts_Request_c
{
public:
  explicit Init_AddThreeInts_Request_c(::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request & msg)
  : msg_(msg)
  {}
  ::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request c(::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request::_c_type arg)
  {
    msg_.c = std::move(arg);
    return std::move(msg_);
  }

private:
  ::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request msg_;
};

class Init_AddThreeInts_Request_b
{
public:
  explicit Init_AddThreeInts_Request_b(::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request & msg)
  : msg_(msg)
  {}
  Init_AddThreeInts_Request_c b(::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request::_b_type arg)
  {
    msg_.b = std::move(arg);
    return Init_AddThreeInts_Request_c(msg_);
  }

private:
  ::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request msg_;
};

class Init_AddThreeInts_Request_a
{
public:
  Init_AddThreeInts_Request_a()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AddThreeInts_Request_b a(::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request::_a_type arg)
  {
    msg_.a = std::move(arg);
    return Init_AddThreeInts_Request_b(msg_);
  }

private:
  ::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Request>()
{
  return fsrobo_a1_msg_srv_4py::srv::builder::Init_AddThreeInts_Request_a();
}

}  // namespace fsrobo_a1_msg_srv_4py


namespace fsrobo_a1_msg_srv_4py
{

namespace srv
{

namespace builder
{

class Init_AddThreeInts_Response_sum
{
public:
  Init_AddThreeInts_Response_sum()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response sum(::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response::_sum_type arg)
  {
    msg_.sum = std::move(arg);
    return std::move(msg_);
  }

private:
  ::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::fsrobo_a1_msg_srv_4py::srv::AddThreeInts_Response>()
{
  return fsrobo_a1_msg_srv_4py::srv::builder::Init_AddThreeInts_Response_sum();
}

}  // namespace fsrobo_a1_msg_srv_4py

#endif  // FSROBO_A1_MSG_SRV_4PY__SRV__DETAIL__ADD_THREE_INTS__BUILDER_HPP_
