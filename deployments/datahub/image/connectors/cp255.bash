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

# urbanism templates fails on osmnet
# https://circleci.com/gh/berkeley-dsep-infra/datahub/88
exit 0

git clone https://github.com/udst/urbansim_templates.git
cd urbansim_templates && python setup.py develop
cd ~ && rm -rf urbansim_templates

# GSI asked for specific versions of these
pip install folium==0.6.0
pip install gdal==2.2.4
pip install geojson==2.4.0
pip install geoviews==1.4.3
pip install holoviews==1.10.7
pip install ipyleaflet==0.9.0
pip install OSMnx==0.8.1
pip install pandana==0.3.0
pip install plotly==1.39.4
pip install shapely==1.6.4
pip install TwitterAPI==2.5.4
pip install urbanaccess==0.1.0
pip install urbansim==3.1.1
