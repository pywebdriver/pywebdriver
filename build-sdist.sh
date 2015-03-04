sudo rm -rf dist
python setup.py sdist
cd dist
tar xvzf *.tar.gz
cd pywebdriver*
sudo pip uninstall pywebdriver
sudo python setup.py install
