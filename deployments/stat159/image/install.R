#!/usr/bin/env r

# Install devtools so we can install versioned packages
install.packages("devtools")

# Install IRKernel
# The kernelspec will be installed after conda is setup in the Dockerfile
install.packages('IRkernel', version='1.1.1')

# Packages for the class
install.packages('gtools', version='3.8.2')