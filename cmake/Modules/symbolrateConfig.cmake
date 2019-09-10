INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SYMBOLRATE symbolrate)

FIND_PATH(
    SYMBOLRATE_INCLUDE_DIRS
    NAMES symbolrate/api.h
    HINTS $ENV{SYMBOLRATE_DIR}/include
        ${PC_SYMBOLRATE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SYMBOLRATE_LIBRARIES
    NAMES gnuradio-symbolrate
    HINTS $ENV{SYMBOLRATE_DIR}/lib
        ${PC_SYMBOLRATE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/symbolrateTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SYMBOLRATE DEFAULT_MSG SYMBOLRATE_LIBRARIES SYMBOLRATE_INCLUDE_DIRS)
MARK_AS_ADVANCED(SYMBOLRATE_LIBRARIES SYMBOLRATE_INCLUDE_DIRS)
