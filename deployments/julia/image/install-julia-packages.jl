#!/usr/bin/env julia
using Pkg;

# FIXME: Specify versions here :'(
Pkg.add.([
    "PyPlot",
    "PyCall",
    "Roots",
    "Polynomials",
    "DifferentialEquations",
    "Triangle",
    "Optim",
    "Images",
    "Plots",
    "Mimi"
]);


# Add support for various MIMI models
Pkg.Registry.add(RegistrySpec(url = "https://github.com/mimiframework/MimiRegistry.git"))

Pkg.add.([
    "MimiFUND"
])
# Precompiling installed packages
Pkg.precompile()
