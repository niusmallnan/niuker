#! /bin/sh
#
# get_rancher_images.sh
# Copyright (C) 2016 niusmallnan <zhangzb@neunn.com>
#
# Distributed under terms of the MIT license.
#
# crontab: 0 17 * * * cd /opt/ && sh get_rancher_images.sh && /usr/local/bin/niuker pull $(cat images.txt) > /tmp/sync_mirror_history.log
#
set -e

if [ -f "$(dirname $0)/images.txt" ]; then
    rm -f $(dirname $0)/images.txt
fi

if [ -d "$(dirname $0)/catalog-dockerfiles" ]; then
    cd $(dirname $0)/catalog-dockerfiles
    git pull origin master
else
    git clone https://github.com/rancher/catalog-dockerfiles.git
    cd $(dirname $0)/catalog-dockerfiles
fi

git grep "image:" | grep yml | awk -F ' ' '{print $3}' > _images.txt
sed -i 's/"//g' _images.txt
sort _images.txt | uniq > $(dirname $0)/../images.txt && rm -f _images.txt
