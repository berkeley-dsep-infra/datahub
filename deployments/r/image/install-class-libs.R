#!/usr/bin/env Rscript

install_class_libs <- function(class_name, class_libs) {
    paste("Installing packages for", class_name)
    for (i in seq(1, length(class_libs), 2)) {
        paste("Installing", class_libs[i], class_libs[i+1])
        devtools::install_github(
            class_libs[i], ref=class_libs[i+1],
            upgrade_dependencies=FALSE, quiet=TRUE
        )
    }
    paste("Done installing packages for", class_name)
}
