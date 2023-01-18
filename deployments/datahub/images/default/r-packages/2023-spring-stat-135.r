#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "Stat 135 Spring 2023"
class_libs = c(
  "mosaicData", "0.20.3"
)
class_libs_install_version(class_name, class_libs)
