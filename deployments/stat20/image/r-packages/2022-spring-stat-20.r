#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "2022 Spring Stat 20"

class_libs = c(
    "swirl", "2.4.5",
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
    "fivethirtyeight", "0.6.1",
    "gapminder", "0.3.0",
    "showtext", "0.9-4"
)

class_libs_install_version(class_name, class_libs)

devtools::install_github("mdbeckman/dcData", ref="56888a6")
devtools::install_github("hadley/emo@3f03b11")
devtools::install_github("andrewpbray/boxofdata@8afd934")

file.symlink("/home/rstudio/shared/stat20/stat20data", "/usr/local/lib/R/site-library/stat20data")

print(paste("Done installing packages for",class_name))
