# Copyright 2018 TODO

file(GLOB_RECURSE _python_files FOLLOW_SYMLINKS "*.py")
if(_python_files)
  message(STATUS "Added test 'bandit' to check Python code security")
  ament_bandit()
endif()
