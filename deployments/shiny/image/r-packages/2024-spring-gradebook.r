#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

# This might be used more broadly than just Stat 20.
class_name = "2024 Spring Gradebook"

class_libs = c(
    "DT", "0.32",
    "HMisc", "5.1-1",
    "purrr", "1.0.2",
    "shinyFiles", "0.9.3",
    "shinyTime", "1.0.3",
    "shinyWidgets", "0.8.1",
    "shinydashboard", "0.7.2"
)

class_libs_install_version(class_name, class_libs)

print(paste("Done installing packages for",class_name))
