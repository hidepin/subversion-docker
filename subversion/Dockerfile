FROM centos:centos7

LABEL maintainer "Hidetoshi Imai <hidepin@gmail.com>"

RUN yum clean all && \
    yum -y reinstall glibc-common && \
    yum install -y \
                subversion \
                mod_dav_svn \
                wget

RUN localedef -i ja_JP -f UTF-8 ja_JP.utf8

COPY files/10-subversion.conf /etc/httpd/conf.modules.d
COPY files/docker-entrypoint.sh /
COPY files/usermanager.cgi /var/www/cgi-bin/
COPY files/svn_hooks /svn_hooks

ENV REPOS sample

CMD ["/docker-entrypoint.sh"]
