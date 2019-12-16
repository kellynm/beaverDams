for /F %i in ('dir /b *.las') do pdal translate --writers.las.minor_version=2 %i %i_versioned.las



