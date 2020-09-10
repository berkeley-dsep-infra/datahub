#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "2019 Fall Stat 131a"
class_libs_install_version(class_name, c("BiocManager", "1.30.10"))
BiocManager::install("Biobase", ask = FALSE, update = FALSE)

class_libs = c(
  "alluvial", "0.1-2",
  "latticeExtra", "0.6-29",
  "DAAG", "1.24",
  "faraway", "1.0.7",
  "fdrtool", "1.2.15",
  "gpairs", "1.3.3",
  "gplots", "3.0.3",
  "hexbin", "1.28.1",
  "leaps", "3.1",
  "NMF", "0.22.0",
  "randomForest", "4.6-14",
  "RColorBrewer", "1.1-2",
  "rjson", "0.2.20",
  "rpart.plot", "3.0.8",
  "scatterplot3d", "0.3-41",
  "shape", "1.4.4",
  "sm", "2.2-5.6",
  "pheatmap", "1.0.12"
)
class_libs_install_version(class_name, class_libs)

# 0.3.4; installing in above vector produces an error
install.packages('vioplot', quiet = TRUE)
