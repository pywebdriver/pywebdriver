from pywebdriver import app, config

def main():
    host = config.get('flask', 'host')
    port = config.getint('flask', 'port')
    debug = config.getboolean('flask', 'debug') 
    app.run(host=host, port=port, debug=debug)

# Run application
if __name__ == '__main__':
    main()
