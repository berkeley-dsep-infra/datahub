#!/usr/bin/env Rscript
# From https://github.com/berkeley-dsep-infra/datahub/issues/3403

print("Installing packages for ottr")
devtools::install_version("ottr", version = "1.1.4", repos = "https://cran.r-project.org", upgrade = "never", quiet = FALSE)
print("Done installing packages for ottr")
