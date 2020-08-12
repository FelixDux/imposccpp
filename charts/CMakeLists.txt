FILE(GLOB Sources src/*.cpp)
add_library (charts ${Sources})
target_include_directories (charts PUBLIC include)
target_include_directories (charts PRIVATE ../dynamics/include)
