FILE(GLOB Sources src/*.cpp)
add_library (dynamics ${Sources})
target_include_directories (dynamics PUBLIC include/)
