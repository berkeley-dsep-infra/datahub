#!/usr/bin/env R

# Function to install Quarto
install_quarto <- function() {
  print("Installing Quarto")
  system("wget https://quarto.org/download/latest/quarto-linux-amd64.deb")
  system("sudo apt-get install -y ./quarto-linux-amd64.deb")
  system("rm ./quarto-linux-amd64.deb")
  print("Quarto installation complete")
}

# Function to install R packages with specific versions
class_libs_install_version <- function(class_name, class_libs) {
  print(paste("Installing packages for", class_name))
  for (i in seq(1, length(class_libs), 2)) {
    installed_packages <- rownames(installed.packages())
    package_name = class_libs[i]
    version = class_libs[i+1]
    # Only install packages if they haven't already been installed!
    # devtools doesn't do that by default
    if (!package_name %in% installed_packages) {
      print(paste("Installing", package_name, version))
      devtools::install_version(package_name, version, quiet=TRUE)
    } else {
      # FIXME: This ignores version incompatibilities :'(
      print(paste("Not installing", package_name, " as it is already installed"))
    }
  }
  print(paste("Done installing packages for", class_name))
}

# Install Quarto
install_quarto()

# R packages to be installed that aren't from apt
# Combination of informal requests & rocker image suggestions
# Some of these were already in datahub image
cran_packages = c(
  "BiocManager", "1.30.21",
  "IRkernel", "1.3.2",
  "rmarkdown", "2.22",
  "shiny", "1.7.4"
)

class_libs_install_version("Base packages", cran_packages)