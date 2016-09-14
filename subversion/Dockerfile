FROM centos:7.2.1511
MAINTAINER Hidetoshi Imai <hidepin@gmail.com>

RUN yum install -y \
                subversion \
                mod_dav_svn

COPY files/10-subversion.conf /etc/httpd/conf.modules.d
COPY files/docker-entrypoint.sh /

ENV LANG=C
ENV REPOS=sample

CMD ["/docker-entrypoint.sh"]
