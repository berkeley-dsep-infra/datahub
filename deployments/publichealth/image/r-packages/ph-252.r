#!/usr/bin/env Rscript
# For https://github.com/berkeley-dsep-infra/datahub/issues/2556
# For https://github.com/berkeley-dsep-infra/datahub/issues/2524
# For https://github.com/berkeley-dsep-infra/datahub/issues/2748
# For https://github.com/berkeley-dsep-infra/datahub/issues/2788
# Fall 2021
print("Installing packages for PH 252")

source("/tmp/class-libs.R")

class_name = "PH 252"

class_libs = c(
  "foreign", "0.8-81",
  "blm", "2013.2.4.4",
  "geepack", "1.3-2",
  "multcomp", "1.4-17",
  "epitools", "0.5-10.1",
  "rms", "6.2-0",
  "lmtest","0.9-38",
  "car","3.0-10",
  "SurvRegCensCov","1.4",
  "ProfileLikelihood","1.1",
  "biostat3","0.1.5"
)

devtools::install_github('cran/epi', ref='06efd3f', upgrade_dependencies=FALSE, quiet=FALSE)
devtools::install_github('kaz-yos/tableone', ref='7cfcd71', upgrade_dependencies=FALSE, quiet=FALSE)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for PH 252")
