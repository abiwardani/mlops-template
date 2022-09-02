#!/usr/bin/env bash

if [[ ! -f /var/log/auth.log ]]
then
    touch /var/log/auth.log
fi

service ssh start

tail -f /var/log/auth.log