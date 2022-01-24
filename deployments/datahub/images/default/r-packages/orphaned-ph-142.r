#!/usr/bin/env Rscript

# This file should be removed at the end of 2021 Fall
# PH courses have moved to the publichealth hub

                                        # From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PH142")

source("/tmp/class-libs.R")

class_name = "PH142"

class_libs = c(
  "fGarch", "3042.83.2",
  "SASxport", "1.7.0",
  "googlesheets", "0.3.0",
  "googledrive", "1.0.1",
  "ggrepel", "0.9.0",
  "janitor", "2.1.0",
  "latex2exp", "0.4.0",
  "measurements", "1.4.0",
  "dagitty", "0.3-0",
  "cowplot", "1.1.1",
  "patchwork", "1.1.1",
  "tigris", "1.0",
  "googlesheets4", "0.2.0"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for PH142")
