#!/bin/bash

# systemd stuff 
sudo apt-get install systemd
sudo systemctl link "/home/axel/Programs/repositories/grazing-cira/grazing.service"
sudo systemctl daemon-reload
sudo systemctl enable grazing.service

if [[ $* == *--start* ]]; then 
    sudo systemctl start grazing.service
    sleep(2)
    sudo systemctl status grazing.service
fi
echo "Done"
