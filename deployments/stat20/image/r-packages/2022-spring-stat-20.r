#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "2022 Spring Stat 20"

class_libs = c(
    "fivethirtyeight", "0.6.2",
    "gapminder", "0.3.0",
    "googlesheets4", "1.0.0",
    "infer", "1.0.0",
    "janitor", "2.1.0",
    "openintro", "2.2.0",
    "pagedown", "0.16",
    "palmerpenguins", "0.1.0",
    "patchwork", "1.1.1",
    "patchwork", "1.1.1",
    "showtext", "0.9-4",
    "swirl", "2.4.5",
    "tidycensus", "1.1",
    "tidymodels", "0.1.4",
    "tigris", "1.5",
    "unvotes", "0.3.0",
    "xaringanthemer", "0.4.1"
)

class_libs_install_version(class_name, class_libs)

devtools::install_github("mdbeckman/dcData", ref="56888a6")
devtools::install_github("hadley/emo@3f03b11")
devtools::install_github("andrewpbray/boxofdata@8afd934")

file.symlink("/opt/shared/stat20/stat20data", "/usr/local/lib/R/site-library/stat20data")

print(paste("Done installing packages for",class_name))
