#!/usr/bin/env r


# Install devtools so we can install versioned packages
install.packages("devtools")

class_libs_install_version <- function(class_name, class_libs) {
    print(paste("Installing packages for", class_name))
    for (i in seq(1, length(class_libs), 2)) {
        print(paste("Installing", class_libs[i], class_libs[i+1]))
        devtools::install_version(
            class_libs[i], version = class_libs[i+1],
            quiet=TRUE
        )
    }
    print(paste("Done installing packages for", class_name))
}


# R packages to be installed that aren't from apt
cran_packages = c(
  "BH", "1.72.0-3",
  "AER", "1.2-9",
  "assertthat", "0.2.1",
  "base64enc", "0.1-3",
  "bindrcpp", "0.2.2",
  "broom", "0.7.3",
  "checkr", "0.5.0",
  "clipr", "0.7.1",
  "crosstalk", "1.1.0.1",
  "crayon", "1.3.4",
  "curl", "4.3",
  "data.table", "1.13.6",
  "DBI", "1.1.0",
  "digest", "0.6.27",
  "dplyr", "1.0.2",
  "e1071", "1.7-4",
  "evaluate", "0.14",
  "forcats", "0.5.0",
  "ggplot2", "3.3.3",
  "glue", "1.4.2",
  "haven", "2.3.1",
  "here", "1.0.1",
  "highr", "0.8",
  "hms", "0.5.3",
  "htmlwidgets", "1.5.3",
  "httpuv", "1.5.4",
  "httr", "1.4.2",
  "ivpack", "1.2",
  "jsonlite", "1.7.2",
  "knitr", "1.30",
  "leaflet", "2.0.3",
  "lubridate", "1.7.9.2",
  "mapproj", "1.2.7",
  "maptools", "1.0-2",
  "markdown", "1.1",
  "Matrix", "1.3-0",
  "matrixStats", "0.57.0",
  "memoise", "1.1.0",
  "modelr", "0.1.8",
  "nlme", "3.1-151",
  "openssl", "1.4.3",
  "pander", "0.6.3",
  "pbdZMQ", "0.3-4",
  "pillar", "1.4.7",
  "png", "0.1-7",
  "praise", "1.0.0",
  "proto", "1.0.0",
  "pryr", "0.1.4",
  "IRkernel", "1.1.1",
  "rapportools", "1.0",
  "raster", "3.4-5",
  "RColorBrewer", "1.1-2",
  "Rcpp", "1.0.5",
  "RCurl", "1.98-1.2",
  "readr", "1.4.0",
  "readxl", "1.3.1",
  "rematch", "1.0.1",
  "repr", "1.1.0",
  "reprex", "0.3.0",
  "reshape", "0.8.8",
  "reticulate", "1.18",
  "rjson", "0.2.20",
  "rlang", "0.4.10",
  "rlist", "0.4.6.1",
  "rmarkdown", "2.6",
  "rpart", "4.1-15",
  "rprojroot", "2.0.2",
  "selectr", "0.4-2",
  "shiny", "1.5.0",
  "sp", "1.4-4",
  "spatstat", "1.64-1",
  "spatstat.data", "1.7-0",
  "spdep", "1.1-5",
  "stargazer", "5.2.2",
  "stringi", "1.5.3",
  "stringr", "1.4.0",
  "summarytools", "0.9.8",
  "testthat", "3.0.1",
  "tibble", "3.0.4",
  "tidyr", "1.1.2",
  "tidyverse", "1.3.0",
  "tinytex", "0.28",
  "utf8", "1.1.4",
  "uuid", "0.1-4",
  "viridis", "0.5.1",
  "withr", "2.3.0",
  "xfun", "0.19",
  "xml2", "1.3.2",
  "yaml", "2.2.1"
  ## "lfe", "???" # https://github.com/sgaure/lfe/issues/41
)

class_libs_install_version("Base packages", cran_packages)
