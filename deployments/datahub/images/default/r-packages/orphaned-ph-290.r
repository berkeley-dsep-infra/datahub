#!/usr/bin/env Rscript

# This file should be removed at the end of 2021 Fall
# PH courses have moved to the publichealth hub

# For https://github.com/berkeley-dsep-infra/datahub/issues/1921
print("Installing packages for PH 290W")

source("/tmp/class-libs.R")

class_name = "PH 290W"

class_libs = c(
  "kableExtra", "1.3.1",
  "plotly", "4.9.2.2",
  "ggthemes", "4.2.0",
  "formattable", "0.2.1"
)

class_libs_install_version(class_name, class_libs)
