#!/usr/bin/env Rscript
print("Installing packages for stat-20")

source("/tmp/class-libs.R")

class_name = "stat-20"

class_libs = c(
    "tidycensus", "1.0",
    "openintro", "2.2.0",
    "infer", "1.0.0",
    "patchwork", "1.1.1",
    "tigris", "1.0",
    "googlesheets4", "0.2.0",
    "xaringanthemer", "0.4.0",
    "palmerpenguins", "0.1.0",
    "unvotes", "0.3.0",
    "janitor", "2.1.0",
    "patchwork", "1.1.1",
    "fivethirtyeight", "0.6.1"
)

class_libs_install_version(class_name, class_libs)

devtools::install_github("hadley/emo@3f03b11")
devtools::install_github("stat-20/stat20data@ab3685a")

print("Done installing packages for stat-20")