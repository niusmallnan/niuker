# 王海龙修改了Readme
# 再次修改


==================================
Docker & Rancher 命令行辅助工具
==================================
Support docker engine v1.10+

安装
============================
# install setuptools first. for example.

   $ easy_install setuptools

# git clone this repo

   $ git clone xxxx/niuker.git

# install this tool

   $ cd niuker && python setup.py develop

pull from neunn or alauda
============================
# switch to the alauda/neunn registry

   $ source tools/alauda-rc.sh

       or

   $ source tools/neunn-rc.sh

# make some tests

   $ niuker pull nginx alpine ubuntu

push images to neunn
============================
# switch to the neunn registry

   $ source tools/neunn-rc.sh

# push all local images

   $ niuker push -a

# push images list

   $ niuker push ubuntu nginx:1.4.3

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


docker-machine
============================
# docker-machine pull images

    $ niuker machine-pull --help

# docker-machine sync images

    $ niuker machine-sync --help


新手教学
============================
# see the cmd help

    $ niuker doc

