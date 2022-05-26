#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/3403
print("Installing packages for ottr")

source("/tmp/class-libs.R")

class_name = "ottr"

class_libs = c(
  "ottr", "1.1.4"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for ottr")
