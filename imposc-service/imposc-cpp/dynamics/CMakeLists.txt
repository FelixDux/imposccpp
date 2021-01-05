FILE(GLOB Sources src/*.cpp)
add_library (dynamics ${Sources})
target_include_directories (dynamics PUBLIC include/)
# # Enable the thread library
# set(THREADS_PREFER_PTHREAD_FLAG ON)
# set(CMAKE_FIND_LIBRARY_SUFFIXES ${CMAKE_STATIC_LIBRARY_SUFFIX})
# find_package(Threads REQUIRED)
# target_link_libraries(dynamics PRIVATE Threads::Threads)
