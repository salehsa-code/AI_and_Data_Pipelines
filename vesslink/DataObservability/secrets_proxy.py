user        = '<user>'
password    = '<password>'
proxies     = {
            'https': f'http://{user}:{password}@web.prod.proxy.cargill.com:4300',
            'http': f'http://{user}:{password}@eweb.prod.proxy.cargill.com:4300'
          }
