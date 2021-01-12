#!/usr/bin/env Rscript

source("/tmp/class-libs.R")

class_name = "2019 Fall Stat 131a"
BiocManager::install('Biobase')
class_libs = c(
  "alluvial", "0.1-2",
  "latticeExtra", "0.6-29",
  "DAAG", "1.24",
  "faraway", "1.0.7",
  "fdrtool", "1.2.16",
  "gpairs", "1.3.3",
  "gplots", "3.1.1",
  "hexbin", "1.28.1",
  "leaps", "3.1",
  "NMF", "0.23.0",
  "randomForest", "4.6-14",
  "rpart.plot", "3.0.9",
  "scatterplot3d", "0.3-41",
  "shape", "1.4.5",
  "sm", "2.2-5.6",
  "pheatmap", "1.0.12",
  "vioplot", "0.3.5"
)
class_libs_install_version(class_name, class_libs)
