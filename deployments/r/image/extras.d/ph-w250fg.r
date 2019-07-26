#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PHW250F+G")

print("Installing here...")
devtools::install_github('cran/here', ref='0.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing rlist...")
devtools::install_github('cran/rlist', ref='0.4.6.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing jsonlite...")
devtools::install_github('cran/jsonlite', ref='1.6', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing checkr...")
devtools::install_github('cran/checkr', ref='0.5.0', upgrade_dependencies=FALSE, quiet=TRUE)

# dplyr requires 0.2.1...cran only has 0.2.0
print("Installing assertthat...")
devtools::install_github('hadley/assertthat', ref='v0.2.1', upgrade_dependencies=FALSE, quiet=FALSE)

print("Installing dplyr...")
devtools::install_github('cran/dplyr', ref='0.8.1', upgrade_dependencies=FALSE, quiet=FALSE)

print("Installing ggplot2...")
devtools::install_github('cran/ggplot2', ref='3.1.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing tidyr...")
devtools::install_github('cran/tidyr', ref='0.8.3', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing reticulate...")
devtools::install_github('cran/reticulate', ref='1.13', upgrade_dependencies=FALSE, quiet=TRUE)

print("Done installing packages for PHW250F+G")
