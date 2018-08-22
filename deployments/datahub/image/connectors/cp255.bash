#!/bin/bash
set -euo pipefail

# this is to work around hubploy #1
function safe_pip_install {
	pip install $1 > /tmp/safe_pip.$$ 2>&1 && \
		true || ( echo FAIL ; cat /tmp/safe_pip.$$ ; false )
}

# GSI asked to always install latest version from source
git clone https://github.com/UDST/choicemodels
cd ~/choicemodels && python setup.py install
cd ~ && rm -rf choicemodels

git clone https://github.com/bokeh/datashader
cd ~/datashader && pip install -e .
cd ~ && rm -rf datashader

git clone https://github.com/udst/urbansim_templates.git
cd urbansim_templates && python setup.py develop
cd ~ && rm -rf urbansim_templates

# GSI asked for specific versions of these
safe_pip_install folium==0.6.0
safe_pip_install gdal==2.2.4
safe_pip_install geojson==2.4.0
safe_pip_install geoviews==1.4.3
safe_pip_install holoviews==1.10.7
safe_pip_install ipyleaflet==0.9.0
safe_pip_install OSMnx==0.8.1
safe_pip_install pandana==0.3.0
safe_pip_install plotly==1.39.4
safe_pip_install shapely==1.6.4
safe_pip_install TwitterAPI==2.5.4
safe_pip_install urbanaccess==0.1.0
safe_pip_install urbansim==3.1.1
