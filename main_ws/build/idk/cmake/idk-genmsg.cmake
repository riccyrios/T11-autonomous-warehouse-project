# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "idk: 1 messages, 0 services")

set(MSG_I_FLAGS "-Iidk:/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(idk_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg" NAME_WE)
add_custom_target(_idk_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "idk" "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(idk
  "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/idk
)

### Generating Services

### Generating Module File
_generate_module_cpp(idk
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/idk
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(idk_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(idk_generate_messages idk_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg" NAME_WE)
add_dependencies(idk_generate_messages_cpp _idk_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(idk_gencpp)
add_dependencies(idk_gencpp idk_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS idk_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(idk
  "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/idk
)

### Generating Services

### Generating Module File
_generate_module_eus(idk
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/idk
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(idk_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(idk_generate_messages idk_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg" NAME_WE)
add_dependencies(idk_generate_messages_eus _idk_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(idk_geneus)
add_dependencies(idk_geneus idk_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS idk_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(idk
  "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/idk
)

### Generating Services

### Generating Module File
_generate_module_lisp(idk
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/idk
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(idk_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(idk_generate_messages idk_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg" NAME_WE)
add_dependencies(idk_generate_messages_lisp _idk_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(idk_genlisp)
add_dependencies(idk_genlisp idk_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS idk_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(idk
  "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/idk
)

### Generating Services

### Generating Module File
_generate_module_nodejs(idk
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/idk
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(idk_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(idk_generate_messages idk_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg" NAME_WE)
add_dependencies(idk_generate_messages_nodejs _idk_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(idk_gennodejs)
add_dependencies(idk_gennodejs idk_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS idk_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(idk
  "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/idk
)

### Generating Services

### Generating Module File
_generate_module_py(idk
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/idk
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(idk_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(idk_generate_messages idk_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/git/T11_multi_warehouse/main_ws/src/idk/msg/Tour.msg" NAME_WE)
add_dependencies(idk_generate_messages_py _idk_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(idk_genpy)
add_dependencies(idk_genpy idk_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS idk_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/idk)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/idk
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(idk_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/idk)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/idk
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(idk_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/idk)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/idk
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(idk_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/idk)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/idk
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(idk_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/idk)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/idk\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/idk
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(idk_generate_messages_py std_msgs_generate_messages_py)
endif()
