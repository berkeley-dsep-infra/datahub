c.ServerProxy.servers = {
  'http-server': {
    'command': ['python3', '-m', 'http.server', '{port}'],
    'absolute_url': False,
    'launcher_entry': {
      'title': "HTTP Server"
    }
  }
}


# Use memory for notebook notary file to workaround corrupted files on nfs
# https://www.sqlite.org/inmemorydb.html
# https://github.com/jupyter/jupyter/issues/174
# https://github.com/ipython/ipython/issues/9163
c.NotebookNotary.db_file = ":memory:"