==================================
Docker & Rancher 命令行辅助工具
==================================


安装
============================
# install setuptools first. for example.

        $ easy_install setuptools

# git clone this repo

        $ git clone xxxx/niuker.git

# install this tool

        $ cd niuker && python setup.py develop

pull from alauda
============================
# switch to the alauda registry

        $ source tools/alauda-rc.sh

# make some tests

        $ niuker pull nginx alpine nginx

clean containers
============================
#clean stoped containers

        $ niuker clean containers

#clean all containers

        $ niuker clean containers -a -f

clean images
============================
# clean untag images

        $ niuker clean images

# clean all images

        $ niuker clean images -a -f

新手教学
============================
# see the cmd help

        $ niuker doc

