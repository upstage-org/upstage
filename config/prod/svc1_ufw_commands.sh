#!/bin/bash

# currently dev and prod share this server
ufw allow 22
ufw enable
ufw allow 'Nginx Full'
ufw allow 1884
ufw allow 9002
ufw allow from 10.116.0.6 to any port 5432;
ufw allow from 10.116.0.3 to any port 5432;
ufw allow from 10.116.0.3 to any port 27018;
ufw allow from 10.116.0.6 to any port 27018;
