#!/usr/bin/env r

source("/tmp/class-libs.R")

# install ottr, needs to go first issue #3216, #3263
devtools::install_github('ucbds-infra/ottr', ref='0.1.0', upgrade_dependencies=FALSE, quiet=FALSE)
