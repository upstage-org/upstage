#!/bin/bash

# currently dev and prod share this server
ufw allow 22
ufw enable
ufw allow 'Nginx Full'
