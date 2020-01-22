#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PHW250F+G")

source("/tmp/class-libs.R")

# dplyr requires 0.2.1...cran only has 0.2.0
print("Installing assertthat...")
devtools::install_github('hadley/assertthat', ref='v0.2.1', upgrade_dependencies=FALSE, quiet=TRUE)

class_name = "PHW250F+G"

class_libs = c(
    "here", "0.1",
    "rlist", "0.4.6.1",
    "jsonlite", "1.6",
    "checkr", "0.5.0",
    "dplyr", "0.8.1",
    "ggplot2", "3.1.0",
    "tidyr", "0.8.3",
)

# 1.13 isn't found in cran?
print("Installing reticulate...")
devtools::install_github('cran/reticulate', ref='1.13', upgrade_dependencies=FALSE, quiet=TRUE)

class_libs_install_version(class_name, class_libs)
