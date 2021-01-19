#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "2021 Spring Stat 20"
class_libs = c(
  "swirl", "2.4.5"
)
class_libs_install_version(class_name, class_libs)

devtools::install_github("mdbeckman/dcData", ref="56888a6")
