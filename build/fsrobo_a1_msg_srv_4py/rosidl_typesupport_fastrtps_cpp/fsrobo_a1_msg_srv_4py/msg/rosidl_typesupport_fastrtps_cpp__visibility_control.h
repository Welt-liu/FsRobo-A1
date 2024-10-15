// generated from
// rosidl_typesupport_fastrtps_cpp/resource/rosidl_typesupport_fastrtps_cpp__visibility_control.h.in
// generated code does not contain a copyright notice

#ifndef FSROBO_A1_MSG_SRV_4PY__MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP__VISIBILITY_CONTROL_H_
#define FSROBO_A1_MSG_SRV_4PY__MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP__VISIBILITY_CONTROL_H_

#if __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_fsrobo_a1_msg_srv_4py __attribute__ ((dllexport))
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_fsrobo_a1_msg_srv_4py __attribute__ ((dllimport))
  #else
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_fsrobo_a1_msg_srv_4py __declspec(dllexport)
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_fsrobo_a1_msg_srv_4py __declspec(dllimport)
  #endif
  #ifdef ROSIDL_TYPESUPPORT_FASTRTPS_CPP_BUILDING_DLL_fsrobo_a1_msg_srv_4py
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_fsrobo_a1_msg_srv_4py ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_fsrobo_a1_msg_srv_4py
  #else
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_fsrobo_a1_msg_srv_4py ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_fsrobo_a1_msg_srv_4py
  #endif
#else
  #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_fsrobo_a1_msg_srv_4py __attribute__ ((visibility("default")))
  #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_IMPORT_fsrobo_a1_msg_srv_4py
  #if __GNUC__ >= 4
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_fsrobo_a1_msg_srv_4py __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_fsrobo_a1_msg_srv_4py
  #endif
#endif

#if __cplusplus
}
#endif

#endif  // FSROBO_A1_MSG_SRV_4PY__MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP__VISIBILITY_CONTROL_H_
