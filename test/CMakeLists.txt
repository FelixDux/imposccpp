include_directories ( ${IMPOSC_SOURCE_DIR}/test/catch
	${IMPOSC_SOURCE_DIR}/charts/include
	${IMPOSC_SOURCE_DIR}/dynamics/include
                     )
add_executable (Test test.cpp)
target_include_directories (Test PUBLIC catch/)
target_link_libraries (Test dynamics charts)
add_test (NAME MyTest COMMAND Test)
