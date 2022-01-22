#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "PHW 272a Spring 2021"
class_libs = c(
  "ggmap", "3.0.0",
  "tmap", "3.3-2",
  "rgdal", "1.5-28"
)
class_libs_install_version(class_name, class_libs)
