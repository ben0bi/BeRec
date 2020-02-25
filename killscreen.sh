#!/bin/bash

echo "Killing the root screen named $1"
sudo screen -X -S $1 kill
echo "DONE"

