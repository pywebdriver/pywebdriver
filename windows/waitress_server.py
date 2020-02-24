import pywebdriver
from pywebdriver import config as conf
import waitress

def main():
    # waitress configuration
    kwargs = {}
    for option, value  in conf.items('waitress'):
        kwargs[option] = value
    waitress.serve(pywebdriver.app, **kwargs)

# Run application
if __name__ == '__main__':
    main()