#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/3757
# econ 140, fall 2022 and into the future

print("Installing packages for ECON 140")

source("/tmp/class-libs.R")

class_name="ECON 140"
class_libs = c(
    "ipumsr", "0.5.0"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for ECON 140")

