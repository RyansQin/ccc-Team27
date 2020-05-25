#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass instance1.yaml -i inventory/hosts.ini