cmake_minimum_required(VERSION 3.9)
project(MAERI_Mapper)

set(CMAKE_CXX_STANDARD 11)
link_libraries(gflags)

add_executable(MAERI_Mapper
    DNNModel.h
    MAERIModel.h
    MAERIModel.cpp
    Analyzer.cpp
    Analyzer.h
        MAERIModel.cpp
    RSNetwork.h
    RSNetwork.cpp
    DSNetwork.h
    DSNetwork.cpp
    MSNetwork.h
    MSNetwork.cpp
    VNAT.h
    VNAT.cpp
        main.cpp define.h
    DNNModel.cpp
    MappingStrategy.h
    utility.h
    utility.cpp
    MappingStrategy.cpp SDMemory.cpp SDMemory.h)
