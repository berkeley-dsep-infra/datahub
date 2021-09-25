#!/usr/bin/env r

# Install devtools, so we can install versioned packages
install.packages("devtools")

# Install a bunch of R packages
# This doesn't do any dependency resolution or anything,
# so refer to `installed.packages()` for authoritative list
cran_packages <- c(
  "tidyverse", "1.3.0",
  "adegenet", "2.1.3",
  "pegas", "0.14",
  "phytools", "0.7-70",
  "ape","5.4-1",
  "seqinr","4.2-4",
  "hierfstat","0.5-7",
  "poppr","2.8.6",
  "PopGenome","2.7.5", 
  "detectRUNS","0.9.6", 
  "pwr","1.3" ,
  "plotly","4.9.3",
  "mixtools","1.2.0",
  "mclust","5.4.7"
)

for (i in seq(1, length(cran_packages), 2)) {
  devtools::install_version(
    cran_packages[i],
    version = cran_packages[i + 1]
  )
}

## Bioconductor packages
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("EBSeq")
BiocManager::install("Rhtslib")
BiocManager::install("dada2")
BiocManager::install("phyloseq")
BiocManager::install("Biostrings")
BiocManager::install("cummeRbund")
