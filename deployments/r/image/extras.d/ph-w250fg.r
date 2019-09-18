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
devtools::install_github('hadley/assertthat', ref='v0.2.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing dplyr...")
devtools::install_github('cran/dplyr', ref='0.8.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing ggplot2...")
devtools::install_github('cran/ggplot2', ref='3.1.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing tidyr...")
devtools::install_github('cran/tidyr', ref='0.8.3', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing reticulate...")
devtools::install_github('cran/reticulate', ref='1.13', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing patchwork")
devtools::install_github("thomasp85/patchwork", upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing fGarch...")
devtools::install_github('cran/fGarch', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing SASxport...")
devtools::install_github('cran/SASxport', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing googlesheets...")
devtools::install_github('cran/googlesheets', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing googledrive...")
devtools::install_github('cran/googledrive', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing ggrepel...")
devtools::install_github('cran/ggrepel', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing infer...")
devtools::install_github('cran/infer', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing janitor...")
devtools::install_github('cran/janitor', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing latex2exp...")
devtools::install_github('cran/latex2exp', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing cowplot...")
devtools::install_github('cran/cowplot', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing measurements...")
devtools::install_github('cran/measurements', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing dagitty...")
devtools::install_github('cran/dagitty', upgrade_dependencies=FALSE, quiet=TRUE)

print("Done installing packages for PHW250F+G")
