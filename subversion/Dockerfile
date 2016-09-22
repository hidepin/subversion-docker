FROM centos:7.2.1511
MAINTAINER Hidetoshi Imai <hidepin@gmail.com>

RUN yum clean all && \
    yum -y reinstall glibc-common && \
    yum install -y \
                subversion \
                mod_dav_svn \
                wget

COPY files/10-subversion.conf /etc/httpd/conf.modules.d
COPY files/docker-entrypoint.sh /
COPY files/svn_hooks /svn_hooks

ENV REPOS sample

CMD ["/docker-entrypoint.sh"]
