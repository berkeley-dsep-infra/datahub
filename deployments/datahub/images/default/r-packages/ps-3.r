#!/usr/bin/env Rscript
# For https://github.com/berkeley-dsep-infra/datahub/issues/2579
# Fall 2021 - Spring 2022

print("Installing packages for PS 3")

source("/tmp/class-libs.R")

class_name = "PS 3"

class_libs = c(
  "estimatr", "0.30.2"
)

class_libs_install_version(class_name, class_libs)
