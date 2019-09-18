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
devtools::install_github("thomasp85/patchwork", ref='36b4918777c25393df605a4959a4c9690d2af186', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing fGarch...")
devtools::install_github('cran/fGarch', ref='3042.83.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing SASxport...")
devtools::install_github('cran/SASxport', ref='1.6.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing googlesheets...")
devtools::install_github('cran/googlesheets', ref='0.3.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing googledrive...")
devtools::install_github('cran/googledrive', ref='0.1.3', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing ggrepel...")
devtools::install_github('cran/ggrepel', ref='0.8.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing infer...")
devtools::install_github('cran/infer', ref='0.4.0.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing janitor...")
devtools::install_github('cran/janitor', ref='1.2.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing latex2exp...")
devtools::install_github('cran/latex2exp', ref='0.4.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing cowplot...")
devtools::install_github('cran/cowplot', ref='1.0.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing measurements...")
devtools::install_github('cran/measurements', ref='1.3.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing dagitty...")
devtools::install_github('cran/dagitty', ref='0.2-2', upgrade_dependencies=FALSE, quiet=TRUE)

print("Done installing packages for PHW250F+G")
