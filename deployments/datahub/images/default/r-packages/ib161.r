#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "IB161"
class_libs = c(
  "pegas", "0.14"
)
class_libs_install_version(class_name, class_libs)
