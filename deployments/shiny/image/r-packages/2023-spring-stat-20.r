#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

# This might be used more broadly than just Stat 20.
class_name = "2023 Spring Stat 20"

class_libs = c(
    "DT", "0.26"
)

class_libs_install_version(class_name, class_libs)

print(paste("Done installing packages for",class_name))
