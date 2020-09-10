#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PH142")

source("/tmp/class-libs.R")

class_name = "PH142"

class_libs = c(
    "fGarch", "3042.83.2",
    "SASxport", "1.7.0",
    "googlesheets", "0.3.0",
    "googledrive", "1.0.1",
    "ggrepel", "0.8.2",
    "infer", "0.5.1",
    "janitor", "2.0.1",
    "latex2exp", "0.4.0",
    "measurements", "1.4.0",
    "dagitty", "0.2-2",
    "rlang", "0.4.6",
    "cowplot", "1.0.0",
    "patchwork", "1.0.0",
    "tigris", "0.9.4",
    "googlesheets4", "0.2.0"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for PH142")
