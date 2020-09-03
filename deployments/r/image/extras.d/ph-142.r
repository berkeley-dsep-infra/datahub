#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PH142")

source("/tmp/class-libs.R")

class_name = "PH142"

class_libs = c(
    "fGarch", "3042.83.1",
    "SASxport", "1.6.0",
    "googlesheets", "0.3.0",
    "googledrive", "0.1.3",
    "ggrepel", "0.8.1",
    "infer", "0.4.0.1",
    "janitor", "1.2.0",
    "latex2exp", "0.4.0",
    "measurements", "1.3.0",
    "dagitty", "0.2-2"
)

class_libs_install_version(class_name, class_libs)

# not found in CRAN
print("Installing rlang...")
devtools::install_github('cran/rlang', ref='0.4.6', upgrade='never', quiet=FALSE)

print("Installing tigris...")
devtools::install_github('walkerke/tigris', ref='3d50076', upgrade='never')

print("Installing cowplot...")
devtools::install_github('cran/cowplot', ref='1.0.0', upgrade='never')

# print("Installing patchwork...")
devtools::install_github('thomasp85/patchwork', ref='36b4918', upgrade='never')

print("Installing googlesheets4")
devtools::install_github("tidyverse/googlesheets4", ref='9348a37511c45257f2aceadf76674a601740e708', upgrade='never', quiet=TRUE)

print("Done installing packages for PH142")
