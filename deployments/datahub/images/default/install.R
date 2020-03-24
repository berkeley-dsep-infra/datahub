# R packages to be installed that aren't from apt

#devtools::install_github('cran/knitr', ref = '7cfb9ac', upgrade_dependencies = FALSE)
devtools::install_version('knitr', '1.21', upgrade_dependencies = FALSE)

#devtools::install_github('cran/leaflet', ref = 'e0019db', upgrade_dependencies = FALSE)
devtools::install_version('leaflet', '2.0.1', upgrade_dependencies = FALSE)

#devtools::install_github('cran/spatstat.data', ref = '2e6fa70', upgrade_dependencies = FALSE)
devtools::install_version('spatstat.data', '1.3-1', upgrade_dependencies = FALSE)

# github ref is version 0.2-3
devtools::install_github('cran/classint', ref = '9bc40fc', upgrade_dependencies = FALSE)

#devtools::install_github('cran/ggmap', ref = '24118b4', upgrade_dependencies = FALSE)
devtools::install_version('ggmap', '2.6.1', upgrade_dependencies = FALSE)

#devtools::install_github('cran/rgdal', ref = '8ae242d', upgrade_dependencies = FALSE)
devtools::install_version('rgdal', '1.3-2', upgrade_dependencies = FALSE)

#devtools::install_github('cran/xfun', ref = '10a9629', upgrade_dependencies = FALSE)
devtools::install_version('xfun', '0.2', upgrade_dependencies = FALSE)

#devtools::install_github('cran/tinytex', ref = 'a350d5c', upgrade_dependencies = FALSE)
devtools::install_version('tinytex', '0.5', upgrade_dependencies = FALSE)

#devtools::install_github('cran/rmarkdown', ref = '9e5496f', upgrade_dependencies = FALSE)
devtools::install_version('rmarkdown', '1.9', upgrade_dependencies = FALSE)

#devtools::install_github('cran/selectr', ref = '7c8ee27', upgrade_dependencies = FALSE)
devtools::install_version('selectr', '0.4-1', upgrade_dependencies = FALSE)

#devtools::install_github('cran/modelr', ref = 'f4e2b61', upgrade_dependencies = FALSE)
devtools::install_version('modelr', '0.1.2', upgrade_dependencies = FALSE)

#devtools::install_github('cran/reprex', ref = '25a43c4', upgrade_dependencies = FALSE)
devtools::install_version('reprex', '0.1.1', upgrade_dependencies = FALSE)

# github ref is version 0.3.2
devtools::install_github('hadley/revest', ref = '15f265b', upgrade_dependencies = FALSE)

# github ref is version 1.66.0-1
devtools::install_github('cran/bh', ref = 'bb41077', upgrade_dependencies = FALSE)
#devtools::install_version('BH', '1.72.0-3')

#devtools::install_github('cran/clipr', ref = 'b95bcb1', upgrade_dependencies = FALSE)
devtools::install_version('clipr', '0.4.1', upgrade_dependencies = FALSE)

#devtools::install_github('cran/tidyverse', ref = 'bd9ff0b', upgrade_dependencies = FALSE)
devtools::install_version('tidyverse', '1.2.1', upgrade_dependencies = FALSE)

#devtools::install_github('cran/pander', ref = '06d1de8', upgrade_dependencies = FALSE)
devtools::install_version('pander', '0.6.3')

#devtools::install_github('cran/pryr', ref = '69edc8d', upgrade_dependencies = FALSE)
devtools::install_version('pryr', '0.1.3', upgrade_dependencies = FALSE)

#devtools::install_github('cran/rapportools', ref = '6da2f4a', upgrade_dependencies = FALSE)
devtools::install_version('rapportools', '1.0')

#devtools::install_github('cran/summarytools', ref = '8eeb20a', upgrade_dependencies = FALSE)
devtools::install_version('summarytools', '0.8.8', upgrade_dependencies = FALSE)

#devtools::install_github('cran/stargazer', ref = '736d303', upgrade_dependencies = FALSE)
devtools::install_version('stargazer', '5.2.2')

#devtools::install_github('cran/ivpack', ref = 'cc70b77', upgrade_dependencies = FALSE)
devtools::install_version('ivpack', '1.2')

# github ref is version 0.8.1
devtools::install_github('cran/dplyr', ref = 'e6ed42a', upgrade_dependencies = FALSE)
# needs newer bh, but produces compiler error with newer bh
#devtools::install_version('dplyr', '0.8.1', upgrade_dependencies = FALSE)

# github ref is version 0.8.15
devtools::install_github('cran/irkernel', ref = '238b691', upgrade_dependencies = FALSE)

devtools::install_version('here', '0.1')

devtools::install_version('checkr', '0.5.0')

devtools::install_version('reticulate', '1.13', upgrade_dependencies=FALSE)

# for EEP118, 2019-11 issue 1154
devtools::install_version('lfe', '2.8-2', upgrade_dependencies=FALSE)
