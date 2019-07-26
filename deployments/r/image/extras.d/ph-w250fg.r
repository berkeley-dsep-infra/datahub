#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PHW250F+G")

print("Installing here...")
devtools::install_github('cran/here', ref='d0feb09', upgrade_dependencies=FALSE, quiet=TRUE)

print("Done installing packages for PHW250F+G")
