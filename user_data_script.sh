#!/bin/bash
yum install httpd -y
systemctl enable httpd
systemctl start httpd