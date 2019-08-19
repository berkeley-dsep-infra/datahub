#!/usr/bin/env Rscript

class_libs_install_github <- function(class_name, class_libs) {
    print(paste("Installing packages for", class_name))
    for (i in seq(1, length(class_libs), 2)) {
        print(paste("Installing", class_libs[i], class_libs[i+1]))
        devtools::install_github(
            class_libs[i], ref=class_libs[i+1],
            upgrade_dependencies=FALSE, quiet=TRUE
        )
    }
    paste("Done installing packages for", class_name)
}

class_libs_install_version <- function(class_name, class_libs) {
    print(paste("Installing packages for", class_name))
    for (i in seq(1, length(class_libs), 2)) {
        print(paste("Installing", class_libs[i], class_libs[i+1]))
        devtools::install_version(
            class_libs[i], version = class_libs[i+1],
            dependencies=TRUE, quiet=TRUE
        )
    }
    print(paste("Done installing packages for", class_name))
}
