==================================
Docker & Rancher 命令行辅助工具
==================================


安装
============================
#install setuptools first

#git clone this repo
$ cd niuker && python setup.py develop

pull from alauda
============================
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
#clean untag images
$ niuker clean images
#clean all images
$ niuker clean images -a -f

新手教学
============================
$ niuker doc

