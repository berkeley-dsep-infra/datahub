c.ServerProxy.servers = {
  'http-server': {
    'command': ['python3', '-m', 'http.server', '{port}'],
    'absolute_url': False,
    'launcher_entry': {
      'title': "HTTP Server"
    }
  }
}
