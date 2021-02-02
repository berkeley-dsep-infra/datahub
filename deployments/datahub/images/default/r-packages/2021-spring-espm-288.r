#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "ESPM 288 Spring 2021"
class_libs = c(
  "rjags", "4-10"
)
class_libs_install_version(class_name, class_libs)
