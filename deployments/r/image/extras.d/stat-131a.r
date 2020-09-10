#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "Stat 131a"
class_libs = c(
    "learnr", "0.10.1"
)

class_libs_install_version(class_name, class_libs)

devtools::install_github('DataComputing/DataComputing', ref='d5cebba', upgrade_dependencies = FALSE)
