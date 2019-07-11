#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/814

devtools::install_github('cran/stargazer', ref='5.2.2', upgrade_dependencies=FALSE)
devtools::install_github('cran/lm.beta', ref='1.5-1', upgrade_dependencies=FALSE)
devtools::install_github('cran/multcomp', ref='1.4-8', upgrade_dependencies=FALSE)
devtools::install_github('cran/lfe', ref='2.8-2', upgrade_dependencies=FALSE)