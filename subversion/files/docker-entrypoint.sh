#!/bin/bash

set -e

if [ ! -e /opt/svn/samplerepo/format ]; then
    svnadmin create --fs-type fsfs /opt/svn/samplerepo
    chown -R apache:apache /opt/svn
fi

if [ ! -d /opt/svn/samplerepo/settings ]; then
    mkdir -p /opt/svn/settings
fi

exec /usr/sbin/httpd -D FOREGROUND
