#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/1103
# eep 1118, fall 2019/spring 2020

print("Installing packages for EEP 1118")

print("Installing car...")
devtools::install_github('cran/car', ref='3.0-2', upgrade_dependencies=FALSE, quiet=TRUE)

print("Done installing packages for EEP 1118")

