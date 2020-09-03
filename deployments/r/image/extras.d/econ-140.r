#!/usr/bin/env Rscript

print("Installing packages for Econ 140")

source("/tmp/class-libs.R")

class_name = "Econ 140"

print("Installing ottr...")
devtools::install_github('ucbds-infra/ottr', ref='0.0.1.b1', upgrade='never', quiet=FALSE)

print("Done installing packages for Econ 140")
