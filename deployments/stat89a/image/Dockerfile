FROM buildpack-deps:bionic-scm

# Set up common env variables
ENV TZ=America/Los_Angeles									    \
    LC_ALL=en_US.UTF-8             								    \
    LANG=en_US.UTF-8               								    \
    LANGUAGE=en_US.UTF-8           								    \
    CONDA_PREFIX=/opt/conda        								    \
    DEBIAN_FRONTEND=noninteractive 

ENV PATH=${CONDA_PREFIX}/bin:$PATH

#    Basic configuration steps
#
#    Set up timezone
RUN  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone			    &&  \
#    locale setup
     echo "${LC_ALL} UTF-8" > /etc/locale.gen 							    &&  \
#
#    Set up default user
     adduser --disabled-password --gecos "Default Jupyter user" jupyterian			    &&  \
#    It took me WAY too long to realize that jovyan was Jovian with the i replaced with
#    a y, like Jupyter is to Jupiter. This username seems more straightforward
#
#    Make sure default user has access to conda directory
     install -d -o jupyterian -g jupyterian ${CONDA_PREFIX}					    &&  \
#
#    Install basic dependencies e.g. for Python
     apt-get update && apt-get --yes upgrade							    &&  \
#
#    --no-install-recommends flag decreases size of image
     apt-get --yes install --no-install-recommends						    \
     bzip2											    \
     gcc 											    \
     libevent-dev 										    \
     libffi-dev 										    \
     libzmq3-dev 										    \
     locales 											    \
     lsb-release 										    \
     tar 											    \
     tzdata								         		    \
     vim								  			    \
#
#    nbconvert prefers having a TeX distribution available, this is the easiest way
#    to install on Ubuntu. pandoc can be installed via conda
     texlive-xetex										    \
     texlive-fonts-recommended 									    \
     texlive-generic-recommended 								    \
#
#    Have this available for students to export PDFs, since JupyterLab doesn't support
#    loading NBConvert (bundler) extensions via UI yet, so nbpdfexport won't work
     wkhtmltopdf										    &&  \
#
#    curl, ca-certificates, wget, git should all be installed in
#    bionic-scm and parent bionic-curl images, so no need to install again here
#
#    Prevent image from becoming too bloated, as much as possible anyway
     apt-get clean --yes									    &&  \
     rm -rf /var/lib/apt/lists/*						 		    &&  \
     rm -rf /tmp/*										    &&  \
#
#    Use newly installed tzdata for configuring timezone
     dpkg-reconfigure --frontend noninteractive tzdata						    &&  \
#
#    Use newly installed locales/locale-gen to configure locals
     locale-gen											    &&  \
#    Prevent bibtex from interrupting nbconvert
     update-alternatives --install /usr/bin/bibtex bibtex /bin/true 200

#    Leave root
WORKDIR /home/jupyterian
USER jupyterian

#    Install Miniconda
#
RUN  curl -s -o miniconda3.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh &&  \
     bash miniconda3.sh -f -b -p ${CONDA_PREFIX}  						    &&  \
     echo "python 3.7.*" >> /opt/conda/conda-meta/pinned  					    &&  \
     conda config --add channels conda-forge  							    &&  \
     conda config --set changeps1 no         							    &&  \
     conda install --yes 	  								    \
     ipympl  	   										    \
     ipywidgets											    \
     jupyterhub  										    \
     jupyterlab  										    \
     matplotlib  										    \
     nodejs  											    \
     numpy   											    \
     pandas  											    \
     pandoc  											    \
     plotly  											    \
     psutil											    \
     scipy  											    \
     setuptools 										    \
     statsmodels										    &&  \
     conda clean --all --yes  									    &&  \
     rm -rf ${CONDA_PREFIX}/pkgs/*								    &&  \
#
#    Install dependencies we can't get from conda-forge
     pip install --no-cache-dir									    \
     nbgitpuller  										    \
     jassign  											    \
     nbresuse  											    \
     okpy  &&  											    \
#
#    Install extra JupyterLab Extension dependencies
     jupyter labextension install								    \
     @jupyter-widgets/jupyterlab-manager  							    \
     @jupyterlab/plotly-extension  								    \
     jupyter-matplotlib  									    \
     plotlywidget  										    &&  \
     rm -rf /tmp/*
     
ADD ipython_config.py ${CONDA_PREFIX}/etc/ipython/
ADD jupyter_notebook_config.py ${CONDA_PREFIX}/etc/jupyter/
     
EXPOSE 8888
