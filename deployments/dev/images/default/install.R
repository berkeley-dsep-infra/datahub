#!/usr/bin/env r

# Install devtools so we can install versioned packages
#install.packages("devtools")

source("/tmp/class-libs.R")

# R packages to be installed that aren't from apt
# Combination of informal requests & rocker image suggestions
# Some of these were already in datahub image
cran_packages = c(
  "BiocManager", "1.30.21",
  "IRkernel", "1.3.2",
  "rmarkdown", "2.22",
  "shiny", "1.7.4"
)

class_libs_install_version("Base packages", cran_packages)
