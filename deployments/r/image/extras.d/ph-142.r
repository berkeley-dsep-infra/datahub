#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/881
print("Installing packages for PH142")

print("Installing fGarch...")
devtools::install_github('cran/fGarch', ref='3042.83.1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing SASxport...")
devtools::install_github('cran/SASxport', ref='1.6.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing googlesheets...")
devtools::install_github('cran/googlesheets', ref='0.3.0', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing googledrive...")
devtools::install_github('cran/googledrive', ref='0.1.3', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing patchwork...")
devtools::install_github('thomasp85/patchwork', ref='36b4918', upgrade_dependencies=FALSE, quiet=TRUE)

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

print("Installing tigris...")
devtools::install_github('walkerke/tigris', ref='78d1e44ccc1f561342078c0e79d0415fa4396389', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing googlesheets4")
devtools::install_github("tidyverse/googlesheets4", ref='9348a37511c45257f2aceadf76674a601740e708', upgrade_dependencies=FALSE, quiet=TRUE)

print("Done installing packages for PH142")
