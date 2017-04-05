cmake_minimum_required(VERSION 2.8.3)
project(pathplanning)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  sensor_msgs
  cv_bridge
  image_transport
)
find_package( OpenCV REQUIRED)


################################################
## Declare ROS messages, services and actions ##
################################################


include_directories(
  ${catkin_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS}
)


#############
## Install ##
#############



#############
## Testing ##
#############

add_message_files(DIRECTORY msg
   FILES
   markerpose.msg
 )

add_executable(astarPP src/astarPP.cpp)
target_link_libraries(astarPP ${catkin_LIBRARIES} ${OpenCV_LIBRARIES})
add_dependencies(astarPP beginner_tutorials_generate_messages_cpp) #Og den her...




