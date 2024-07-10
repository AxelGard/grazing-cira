#!/bin/bash

cd "/home/axel/Programs/repositories/grazing-cira/"
mkdir "/etc/grazing-cira"
ln -sf ./run.sh /etc/grazing-cira/run.sh

# systemd stuff 
sudo systemctl link "/home/axel/Programs/repositories/grazing-cira/grazing.service"
sudo systemctl daemon-reload
sudo systemctl enable grazing.service

if [[ $* == *--start* ]]; then 
    sudo systemctl start grazing.service
fi
