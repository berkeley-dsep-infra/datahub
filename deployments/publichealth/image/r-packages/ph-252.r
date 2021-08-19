#!/usr/bin/env Rscript
# For https://github.com/berkeley-dsep-infra/datahub/issues/2556
# Fall 2021
print("Installing packages for PH 252")

source("/tmp/class-libs.R")

class_name = "PH 252"

class_libs = c(
  "tableone", "0.13.0"
)

class_libs_install_version(class_name, class_libs)
