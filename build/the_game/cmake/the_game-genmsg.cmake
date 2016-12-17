# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "the_game: 2 messages, 0 services")

set(MSG_I_FLAGS "-Ithe_game:/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg;-Isensor_msgs:/opt/ros/indigo/share/sensor_msgs/cmake/../msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/indigo/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(the_game_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg" NAME_WE)
add_custom_target(_the_game_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "the_game" "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg" ""
)

get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg" NAME_WE)
add_custom_target(_the_game_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "the_game" "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg" "geometry_msgs/Vector3"
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(the_game
  "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/the_game
)
_generate_msg_cpp(the_game
  "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/the_game
)

### Generating Services

### Generating Module File
_generate_module_cpp(the_game
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/the_game
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(the_game_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(the_game_generate_messages the_game_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg" NAME_WE)
add_dependencies(the_game_generate_messages_cpp _the_game_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg" NAME_WE)
add_dependencies(the_game_generate_messages_cpp _the_game_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(the_game_gencpp)
add_dependencies(the_game_gencpp the_game_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS the_game_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(the_game
  "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/the_game
)
_generate_msg_lisp(the_game
  "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/the_game
)

### Generating Services

### Generating Module File
_generate_module_lisp(the_game
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/the_game
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(the_game_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(the_game_generate_messages the_game_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg" NAME_WE)
add_dependencies(the_game_generate_messages_lisp _the_game_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg" NAME_WE)
add_dependencies(the_game_generate_messages_lisp _the_game_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(the_game_genlisp)
add_dependencies(the_game_genlisp the_game_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS the_game_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(the_game
  "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/the_game
)
_generate_msg_py(the_game
  "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Vector3.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/the_game
)

### Generating Services

### Generating Module File
_generate_module_py(the_game
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/the_game
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(the_game_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(the_game_generate_messages the_game_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Vector2.msg" NAME_WE)
add_dependencies(the_game_generate_messages_py _the_game_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/cc/ee106a/fa16/class/ee106a-act/ros_workspaces/ee106a-patrol-game/src/the_game/msg/Update.msg" NAME_WE)
add_dependencies(the_game_generate_messages_py _the_game_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(the_game_genpy)
add_dependencies(the_game_genpy the_game_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS the_game_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/the_game)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/the_game
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(the_game_generate_messages_cpp sensor_msgs_generate_messages_cpp)
add_dependencies(the_game_generate_messages_cpp std_msgs_generate_messages_cpp)
add_dependencies(the_game_generate_messages_cpp geometry_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/the_game)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/the_game
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(the_game_generate_messages_lisp sensor_msgs_generate_messages_lisp)
add_dependencies(the_game_generate_messages_lisp std_msgs_generate_messages_lisp)
add_dependencies(the_game_generate_messages_lisp geometry_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/the_game)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/the_game\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/the_game
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(the_game_generate_messages_py sensor_msgs_generate_messages_py)
add_dependencies(the_game_generate_messages_py std_msgs_generate_messages_py)
add_dependencies(the_game_generate_messages_py geometry_msgs_generate_messages_py)
