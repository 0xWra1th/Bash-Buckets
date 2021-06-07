#!/bin/bash

# Required programs: apt, hostnamectl, grep, mpstat, awk, free, df
# The @'s allow for easier string manipulation before templating in django

# 1) Get upgradable packages
apt list --upgradable
echo "@"

# 2) Get kernel version
hostnamectl | grep Kernel
echo "@"

# 3) System load (CPU) (mpstat will need to be install)
mpstat 1 1 | awk '$12 ~ /[0-9.]+/ { print 100 - $12"%" }'
echo "@"

# 4) Get free memory
free | grep Mem | awk '{print $4/$2 * 100.0"%"}'
echo "@"

# 5) Get free disk space
df / | awk '$4 ~/[0-9.]+/ { print $4/1024/1024" GB"}'
echo "@"