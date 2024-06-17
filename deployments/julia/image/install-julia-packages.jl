#!/usr/bin/env julia
using Pkg;

Pkg.add.([
    Pkg.PackageSpec(;name="FFTW", version="1.7.1"),
    Pkg.PackageSpec(;name="FastGaussQuadrature", version="1.0.0"),
    Pkg.PackageSpec(;name="ForwardDiff", version="0.10.36"),
    Pkg.PackageSpec(;name="NBInclude", version="2.3.0"),
    Pkg.PackageSpec(;name="Delaunator", version="0.1.1"),
    Pkg.PackageSpec(;name="TriplotRecipes", version="0.1.2"),
    Pkg.PackageSpec(;name="StaticArrays", version="1.6.2"),
    Pkg.PackageSpec(;name="ForwardDiff", version="0.10.35"),
    Pkg.PackageSpec(;name="BenchmarkTools", version="1.3.2"),
    Pkg.PackageSpec(;name="Query", version="1.0.0"),
    Pkg.PackageSpec(;name="VegaLite", version="2.6.0"),
    Pkg.PackageSpec(;name="CSVFiles", version="1.0.1"),
    Pkg.PackageSpec(;name="Distributions", version="0.23.11"),
    Pkg.PackageSpec(;name="DataFrames"),
    Pkg.PackageSpec(;name="Plots", version="1.24.3"),
    Pkg.PackageSpec(;name="Images", version="0.24.1"),
    Pkg.PackageSpec(;name="PyPlot", version="2.10.0"),
    Pkg.PackageSpec(;name="PyCall", version="1.92.5"),
    Pkg.PackageSpec(;name="Roots", version="1.3.11"),
    Pkg.PackageSpec(;name="Polynomials", version="2.0.18"),
    Pkg.PackageSpec(;name="DifferentialEquations", version="7.8.0"),
    Pkg.PackageSpec(;name="Optim", version="1.5.0")
]);

# Precompiling installed packages
Pkg.precompile();
