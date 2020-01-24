FROM buildpack-deps:bionic-scm

# Set up common env variables
ENV TZ=America/Los_Angeles									    \
    LC_ALL=en_US.UTF-8             								    \
    LANG=en_US.UTF-8               								    \
    LANGUAGE=en_US.UTF-8           								    \
    CONDA_PREFIX=/opt/conda        								    \
    DEBIAN_FRONTEND=noninteractive 								    \
    JUPYTER_USER=jovyan

ENV PATH=${CONDA_PREFIX}/bin:$PATH								    \
    HOME_DIR=/home/${JUPYTER_USER}

#    Basic configuration steps
#
#    Set up timezone
RUN  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone			    &&  \
#    locale setup
     echo "${LC_ALL} UTF-8" > /etc/locale.gen 							    &&  \
#
#    Set up default user
     adduser --disabled-password --gecos "Default Jupyter user" ${JUPYTER_USER}			    &&  \
#
#    Make sure default user has access to conda directory
     install -d -o ${JUPYTER_USER} -g ${JUPYTER_USER} ${CONDA_PREFIX}
     
#    Install basic dependencies e.g. for Python
RUN  apt-get -qq update && apt-get --yes -qq upgrade							    &&  \
     apt-get --yes -qq install   	  	    	 						    \
     bzip2											    \
     gcc 											    \
     libevent-dev 										    \
     libffi-dev 										    \
     libzmq3-dev 										    \
     locales 											    \
     lsb-release 										    \
     tar 											    \
     tzdata								         		    \
     vim

#    nbconvert prefers having a TeX distribution available, this is the easiest way
#    to install on Ubuntu. pandoc can be installed via conda
#RUN  apt-get --yes -qq install									    \
#     texlive-xetex										    \
#     texlive-fonts-recommended 									    \
#     texlive-generic-recommended 								    \
#
#    Have this available for students to export PDFs, since JupyterLab doesn't support
#    loading NBConvert (bundler) extensions via UI yet, so nbpdfexport won't work
#     wkhtmltopdf										   
#
#    curl, ca-certificates, wget, git should all be installed in
#    bionic-scm and parent bionic-curl images, so no need to install again here


#    Use newly installed tzdata for configuring timezone
RUN  dpkg-reconfigure --frontend noninteractive tzdata						    &&  \
#
#    Use newly installed locales/locale-gen to configure locals
     locale-gen											    &&  \
#
#    Prevent bibtex from interrupting nbconvert
     update-alternatives --install /usr/bin/bibtex bibtex /bin/true 200


#    Leave root
WORKDIR ${HOME_DIR}
USER ${JUPYTER_USER}

#    Package specifications for Conda
COPY environment.yml /tmp/

#    Install Miniconda and conda packages
RUN  curl -s -o miniconda3.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh &&  \
     bash miniconda3.sh -f -b -p ${CONDA_PREFIX}  						    &&  \
     conda config --add channels conda-forge  							    &&  \
     conda config --set changeps1 no         							    &&  \
     conda env update --name base --file /tmp/environment.yml				   	    &&  \
     conda clean --all --yes -f

#    Install extra JupyterLab Extension dependencies
RUN  jupyter labextension install								    \
     @jupyter-widgets/jupyterlab-manager  							    \
     @jupyterlab/plotly-extension  								    \
     jupyter-matplotlib  									    \
     plotlywidget
     
COPY ipython_config.py ${CONDA_PREFIX}/etc/ipython/
COPY jupyter_notebook_config.py ${CONDA_PREFIX}/etc/jupyter/
     
EXPOSE 8888
