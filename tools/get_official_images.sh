#! /bin/sh
#
# get_official_images.sh
# Copyright (C) 2016 niusmallnan <zhangzb@neunn.com>
#
# Distributed under terms of the MIT license.
#
set -e

if [ -f "$(dirname $0)/official.txt" ]; then
    rm -f $(dirname $0)/official.txt
fi

if [ -d "$(dirname $0)/official-images" ]; then
    cd $(dirname $0)/official-images
    git pull origin master
else
    git clone https://github.com/docker-library/official-images.git
    cd $(dirname $0)/official-images
fi

if [ ! -f "/usr/local/bin/bashbrew" ]; then
    cp bashbrew/bashbrew.sh /usr/local/bin/bashbrew && chmod +x /usr/local/bin/bashbrew
fi

bashbrew list --library=`pwd`/library --all > $(dirname $0)/../official.txt

