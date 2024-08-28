#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "2023 Fall Stat 20"

class_libs = c(
    "fivethirtyeight", "0.6.2",
    "gapminder", "0.3.0",
    "janitor", "2.2.0",
    "openintro", "2.4.0",
    "pagedown", "0.16",
    "palmerpenguins", "0.1.1",
    "patchwork", "1.1.2",
    "showtext", "0.9-4",
    "swirl", "2.4.5",
    "tidycensus", "1.1",
    "tidymodels", "0.1.4",
    "tigris", "1.5",
    "unvotes", "0.3.0",
    "xaringanthemer", "0.4.1",
    "rmarkdown", "2.22",
    "plotly", "4.10.1",
    "reshape2", "1.4.4",
    "kableExtra", "1.3.4",
    "infer", "1.0.4",
    "countdown", "0.4.0",
    "ggrepel", "0.9.3",
    "ggthemes", "4.2.4",
    "latex2exp", "0.9.6",
    "markdown", "1.7",
    "downlit", "0.4.3",
    "xml2", "1.3.4",
    "gt", "0.9.0",
    "quarto", "1.2",
    "fs", "1.6.3",
    "rsample", "1.2.1"
)

class_libs_install_version(class_name, class_libs)

devtools::install_github("mdbeckman/dcData", ref="56888a6")
devtools::install_github("hadley/emo@3f03b11")
devtools::install_github("andrewpbray/boxofdata@8afd934")
devtools::install_github("tidymodels/infer@2806a69")
devtools::install_github("stat20/stat20data@11b4377")

# file.symlink("/opt/shared/stat20/stat20data", "/usr/local/lib/R/site-library/stat20data")

print(paste("Done installing packages for",class_name))
