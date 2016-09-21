#!/bin/bash

set -e

for REPO in $(echo -n ${REPOS} | sed 's/:/ /g')
do
    if [ ! -f "/opt/svn/${REPO}repo/README.txt" ] || [ `cat "/opt/svn/${REPO}repo/README.txt" | grep "This is a Subversion repository" | wc -l` -ne 1 ]; then
        echo "generate ${REPO}repo."
        svnadmin create --fs-type fsfs /opt/svn/${REPO}repo
        svn mkdir --parents file:///opt/svn/${REPO}repo/${REPO}doc/trunk \
                            file:///opt/svn/${REPO}repo/${REPO}app/trunk \
                            file:///opt/svn/${REPO}repo/${REPO}app/branches \
                            file:///opt/svn/${REPO}repo/${REPO}app/tags \
                            -m "initial create dir hier."
        cp /svn_hooks/* /opt/svn/${REPO}repo/hooks
        chown -R apache:apache /opt/svn
    fi
done

if [ ! -f "/opt/svn/settings/authz" ]; then
    echo "generate authz file."
    mkdir -p /opt/svn/settings
    cat <<EOF > /opt/svn/settings/authz
[groups]
member =

[/]
* = rw
EOF
fi

exec /usr/sbin/httpd -D FOREGROUND
