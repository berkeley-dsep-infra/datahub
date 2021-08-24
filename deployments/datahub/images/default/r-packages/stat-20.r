#!/usr/bin/env Rscript
print("Installing packages for stat-20")

source("/tmp/class-libs.R")

class_name = "stat-20"

class_libs = c(
    "tidycensus", "1.0",
    "openintro", "2.0.0",
    "infer", "1.0.0",
    "patchwork", "1.1.1",
    "tigris", "1.0",
    "googlesheets4", "0.2.0"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for stat-20")