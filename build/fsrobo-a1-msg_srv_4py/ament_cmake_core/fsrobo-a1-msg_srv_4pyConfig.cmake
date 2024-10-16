# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_fsrobo-a1-msg_srv_4py_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED fsrobo-a1-msg_srv_4py_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(fsrobo-a1-msg_srv_4py_FOUND FALSE)
  elseif(NOT fsrobo-a1-msg_srv_4py_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(fsrobo-a1-msg_srv_4py_FOUND FALSE)
  endif()
  return()
endif()
set(_fsrobo-a1-msg_srv_4py_CONFIG_INCLUDED TRUE)

# output package information
if(NOT fsrobo-a1-msg_srv_4py_FIND_QUIETLY)
  message(STATUS "Found fsrobo-a1-msg_srv_4py: 0.0.0 (${fsrobo-a1-msg_srv_4py_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'fsrobo-a1-msg_srv_4py' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${fsrobo-a1-msg_srv_4py_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(fsrobo-a1-msg_srv_4py_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${fsrobo-a1-msg_srv_4py_DIR}/${_extra}")
endforeach()