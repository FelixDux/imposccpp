FILE(GLOB Sources src/*.cpp)
add_library (imposcpy ${Sources})
target_include_directories (imposcpy PUBLIC include)
target_include_directories (imposcpy PUBLIC ../dynamics/include)
target_include_directories (imposcpy PRIVATE ../charts/include)

target_link_libraries (imposcpy PRIVATE dynamics)
target_link_libraries (imposcpy PRIVATE charts)
