cmake_minimum_required(VERSION 3.0.0)

project(exif_header_checker VERSION 0.1.0)

SET(Boost_USE_STATIC_LIBS ON)

find_package(Boost COMPONENTS log program_options REQUIRED)


include_directories( ${Boost_INCLUDE_DIRS} )
include_directories(cpp_exiftool/inc)
include_directories(cpp_exiftool/src)
include_directories(src)
include_directories(include)

add_executable(exif_header_checker 
    src/main.cpp
    include/Table.h
    src/Table.cpp
    cpp_exiftool/inc/ExifTool.h
    cpp_exiftool/src/ExifTool.cpp
    cpp_exiftool/src/ExifToolPipe.cpp
    cpp_exiftool/src/TagInfo.cpp
    )

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)

target_link_libraries (exif_header_checker ${Boost_LIBRARIES})


