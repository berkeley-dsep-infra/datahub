############################
# Install packages for IB134L
############################

#LOCAL_BIN=${REPO_DIR}/.local/bin
#mkdir -p ${LOCAL_BIN}
#
## mitoZ installation
#
#wget https://raw.githubusercontent.com/linzhi2013/MitoZ/master/version_2.4-alpha/release_MitoZ_v2.4-alpha.tar.bz2 -O ${REPO_DIR}/release_MitoZ_v2.4-alpha.tar.bz2
#pushd ${REPO_DIR}
#tar -jxvf release_MitoZ_v2.4-alpha.tar.bz2
#rm release_MitoZ_v2.4-alpha.tar.bz2
#cd release_MitoZ_v2.4-alpha
#wget https://raw.githubusercontent.com/linzhi2013/MitoZ/master/version_2.4-alpha/mitozEnv.yaml
#cd ..
#
### create mitoZ env
#conda env create -n mitozEnv -f release_MitoZ_v2.4-alpha/mitozEnv.yaml # worked after reinstallation of conda
#
### patch ncbiquery.py
#cp patches/ncbiquery.py /srv/conda/envs/mitozEnv/lib/python3.6/site-packages/ete3/ncbi_taxonomy/ncbiquery.py
#
### download annotations
##source activate mitozEnv
##python3 mitozEnv_config.py
##source deactivate


###


