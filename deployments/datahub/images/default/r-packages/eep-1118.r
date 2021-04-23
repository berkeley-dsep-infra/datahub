#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/1103
# eep 1118, fall 2019/spring 2020

print("Installing packages for EEP 1118")

source("/tmp/class-libs.R")

class_name="EEP 1118"
class_libs = c(
    "car", "3.0-10"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for EEP 1118")

