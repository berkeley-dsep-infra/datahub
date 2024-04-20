#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/1103 && https://github.com/berkeley-dsep-infra/datahub/issues/4203
# eep 1118, Spring 2023

print("Installing packages for EEP 1118")

source("/tmp/class-libs.R")

class_name="EEP 1118"
class_libs = c(
    "car", "3.0-10",
    "mfx", "1.2-2",
    "psych", "2.2.9",
    "pacman", "0.5.1"
)

class_libs_install_version(class_name, class_libs)

print("Done installing packages for EEP 1118")
