#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass instance4.yaml -i inventory/hosts.ini