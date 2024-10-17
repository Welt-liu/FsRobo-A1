# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_test4_dof_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED test4_dof_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(test4_dof_FOUND FALSE)
  elseif(NOT test4_dof_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(test4_dof_FOUND FALSE)
  endif()
  return()
endif()
set(_test4_dof_CONFIG_INCLUDED TRUE)

# output package information
if(NOT test4_dof_FIND_QUIETLY)
  message(STATUS "Found test4_dof: 0.1.0 (${test4_dof_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'test4_dof' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${test4_dof_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(test4_dof_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${test4_dof_DIR}/${_extra}")
endforeach()
