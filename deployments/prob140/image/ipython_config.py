# Disable history manager, we don't really use it
# and by default it puts an sqlite file on NFS, which is not something we wanna do
c.Historymanager.enabled = False

# Use memory for notebook notary file to workaround corrupted files on nfs
# https://www.sqlite.org/inmemorydb.html
# https://github.com/jupyter/jupyter/issues/174
# https://github.com/ipython/ipython/issues/9163
c.NotebookNotary.db_file = ":memory:"
