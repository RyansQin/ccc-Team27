#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass instance23.yaml -i inventory/hosts.ini