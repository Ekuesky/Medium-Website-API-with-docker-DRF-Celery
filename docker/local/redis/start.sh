#!/bin/bash

#Exit immediately if a command exits with a non-zero status.
#set -o errexit
#The return value of a pipeline is the status of the last command to exit with a non-zero status, or zero if no command exited with a non-zero status
#set -o pipefail
#Treat unset variables and parameters as an error when performing parameter expansion.
#set -o nounset

# Add vm.overcommit_memory=1 to /etc/sysctl.conf if not already present
#if ! grep -q "vm.overcommit_memory=1" /etc/sysctl.conf; then
#    echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
#fi
# Apply the sysctl settings
#sysctl -w vm.overcommit_memory=1
#exec "$@"
