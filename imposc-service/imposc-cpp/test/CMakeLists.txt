include_directories ( ${IMPOSC_SOURCE_DIR}/test/catch
	${IMPOSC_SOURCE_DIR}/charts/include
	${IMPOSC_SOURCE_DIR}/dynamics/include
	${IMPOSC_SOURCE_DIR}/imposcpy/include
                     )

# Enable the thread library
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable (Test test.cpp test_dynamics.cpp)
target_include_directories (Test PUBLIC catch/)
target_link_libraries (Test dynamics charts imposcpy Threads::Threads)

add_test (NAME MyTest COMMAND Test)
