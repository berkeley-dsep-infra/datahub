#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/814
print("Installing packages for IA C188")

print("Installing stargazer...")
devtools::install_github('cran/stargazer', ref='5.2.2', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing lm.beta...")
devtools::install_github('cran/lm.beta', ref='1.5-1', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing multcomp...")
devtools::install_github('cran/multcomp', ref='1.4-8', upgrade_dependencies=FALSE, quiet=TRUE)

print("Installing lfe...")
devtools::install_github('cran/lfe', ref='2.8-2', upgrade_dependencies=FALSE, quiet=TRUE)

print("Done installing packages for IA C188")