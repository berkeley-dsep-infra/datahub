#!/usr/bin/env Rscript
# From 
# econ 140, fall 2022 and into the future

print("Installing packages for POL SCI 3")

source("/tmp/class-libs.R")

class_name="POL SCI 3"
class_libs = c(
    "estimatr", "1.0.2"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for POL SCI 3")

