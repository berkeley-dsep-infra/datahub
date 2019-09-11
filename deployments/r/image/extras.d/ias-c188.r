#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/814
#      https://github.com/berkeley-dsep-infra/datahub/issues/897

source("/tmp/class-libs.R")

class_name = "IA C188"
class_libs = c(
    "cran/rdd", "0.57",
    "cran/stargazer", "5.2.2",
    "cran/lm.beta", "1.5-1",
    "cran/multcomp", "1.4-8",
    "cran/lfe", "2.8-2"
)

class_libs_install_github(class_name, class_libs)

