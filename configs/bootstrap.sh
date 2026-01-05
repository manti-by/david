#!/bin/bash
# NGINX setup
sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -s /home/ubuntu/david/configs/nginx.conf /etc/nginx/sites-enabled/default
sudo systemctl restart nginx.service

# Web app services
sudo ln -s /home/ubuntu/david/configs/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl enable gunicorn.service
sudo systemctl start gunicorn.service

# Background worker
sudo ln -s /home/ubuntu/david/configs/worker.service /etc/systemd/system/worker.service
sudo systemctl enable worker.service
sudo systemctl start worker.service

# Scheduled tasks
sudo ln -s /home/ubuntu/david/configs/scheduler.service /etc/systemd/system/scheduler.service
sudo systemctl enable scheduler.service
sudo systemctl start scheduler.service
