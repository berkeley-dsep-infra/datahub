#!/usr/bin/env Rscript
# For https://github.com/berkeley-dsep-infra/datahub/issues/2556
# Fall 2021
print("Installing packages for PH 252")

source("/tmp/class-libs.R")

class_name = "PH 252"
devtools::install_github('kaz-yos/tableone', ref='7cfcd71')
