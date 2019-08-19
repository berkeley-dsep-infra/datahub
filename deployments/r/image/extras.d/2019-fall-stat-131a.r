#!/usr/bin/env Rscript

source("/tmp/install-class-libs.R")

class_name = "2019 Fall Stat 131a"
class_libs = c(
  "cran/alluvial", "0.1-2",
  "cran/DAAG", "1.22",
  "cran/faraway", "1.0.7",
  "cran/fdrtool", "1.2.15",
  "cran/gpairs", "1.2",
  "cran/gplots", "3.0.1.1",
  "cran/hexbin", "1.27.3",
  "cran/leaps", "2.9",
  "cran/NMF", "0.21.0",
  "cran/randomForest", "4.6-12",
  "cran/RColorBrewer", "1.1-2",
  "cran/rjson", "0.2.20",
  "cran/rpart.plot", "3.0.7",
  "cran/scatterplot3d", "0.3-41",
  "cran/shape", "1.4.4",
  "cran/sm", "2.2-5.6",
  "cran/vioplot", "0.3.2"
)
install_class_libs(class_name, class_libs)
