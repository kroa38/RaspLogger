#!/bin/bash
echo "Package update ..............................................................."
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y install $(cat pkglist.txt)
echo "Python package install........................................................"
pip install -r requirements.txt & process_id=$!


