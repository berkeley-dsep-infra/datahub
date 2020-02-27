#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/814
#      https://github.com/berkeley-dsep-infra/datahub/issues/897

source("/tmp/class-libs.R")

class_name = "IA C188"
class_libs = c(
    "rdd", "0.57",
    "stargazer", "5.2.2",
    "lm.beta", "1.5-1",
    "multcomp", "1.4-8",
    "lfe", "2.8-2"
)

class_libs_install_version(class_name, class_libs)

