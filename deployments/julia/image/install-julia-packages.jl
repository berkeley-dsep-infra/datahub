#!/usr/bin/env julia
using Pkg;

# Add support for various MIMI models
Pkg.Registry.add(RegistrySpec(url = "https://github.com/mimiframework/MimiRegistry.git"));

Pkg.add.([
    Pkg.PackageSpec(;name="MimiFUND", version="3.13.0"),
    Pkg.PackageSpec(;name="MimiIWG", version="1.1.0"),
    Pkg.PackageSpec(;name="MimiDICE2010", version="1.0.1"),
    Pkg.PackageSpec(;name="MimiDICE2013", version="1.0.2"),
    Pkg.PackageSpec(;name="MimiPAGE2009", version="3.1.0"),
    Pkg.PackageSpec(;name="MimiRICE2010", version="3.0.3"),
    Pkg.PackageSpec(;name="Query", version="1.0.0"),
    Pkg.PackageSpec(;name="VegaLite", version="2.6.0"),
    Pkg.PackageSpec(;name="CSVFiles", version="1.0.1"),
    Pkg.PackageSpec(;name="Distributions", version="0.25.68"),
    Pkg.PackageSpec(;name="DataFrames", version="1.3.4"),
    Pkg.PackageSpec(;name="Plots", version="1.24.3"),
    Pkg.PackageSpec(;name="Images", version="0.24.1"),
    Pkg.PackageSpec(;name="PyPlot", version="2.10.0"),
    Pkg.PackageSpec(;name="PyCall", version="1.92.5"),
    Pkg.PackageSpec(;name="Roots", version="2.0.2"),
    Pkg.PackageSpec(;name="Polynomials", version="3.2"),
    Pkg.PackageSpec(;name="DifferentialEquations", version="7.2.0"),
    Pkg.PackageSpec(;name="Mimi", version="1.4.0"),
    Pkg.PackageSpec(;name="Optim", version="1.5.0")
]);

# Precompiling installed packages
Pkg.precompile();
