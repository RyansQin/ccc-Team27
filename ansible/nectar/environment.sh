#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass environment.yaml -i inventory/hosts.ini