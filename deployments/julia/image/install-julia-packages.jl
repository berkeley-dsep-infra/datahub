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
    "Plots"
]);
