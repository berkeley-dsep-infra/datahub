#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PHW250F+G")

source("/tmp/class-libs.R")

class_name = "PHW250F+G"

class_libs = c(
    "assertthat", "0.2.1",
    "here", "0.1",
    "rlist", "0.4.6.1",
    "jsonlite", "1.6.1",
    "checkr", "0.5.0",
    "dplyr", "1.0.0",
    "tidyr", "1.1.0",
    "reticulate", "1.16"
)

# "ggplot2", "3.1.0",
# ggplot was removed from cran
# https://cran.microsoft.com/snapshot/2020-05-30/src/contrib/Archive/ggplot/

class_libs_install_version(class_name, class_libs)
