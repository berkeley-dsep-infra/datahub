# Disable sqlite things since we use nfs

# history manager -- we don't really use it
c.Historymanager.enabled = False

# nbformat signing. from nbformat/tests/test_sign.py
from nbformat import sign
store = sign.MemorySignatureStore()
c.NotebookNotary.store_factory = lambda: store
