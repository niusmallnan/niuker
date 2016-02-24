# -*- coding: utf-8 -*-
# Copyright 2016 Neunn, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import click


@click.command('doc', short_help='show docker commonly-used commands')
def cli():
    """docker commonly-used commands"""
    print("""
    1.查看docker信息（version、info）
    # 查看docker版本
    $docker version
    # 显示docker系统的信息
    $docker info

    2.对image的操作（search、pull、images、rmi、history）
    # 检索image
    $docker search image_name
    # 下载image
    $docker pull image_name
    # 列出镜像列表; -a, --all=false Show all images; --no-trunc=false Don't truncate output; -q, --quiet=false Only show numeric IDs
    $docker images
    # 删除一个或者多个镜像; -f, --force=false Force; --no-prune=false Do not delete untagged parents
    $docker rmi image_name
    # 显示一个镜像的历史; --no-trunc=false Don't truncate output; -q, --quiet=false Only show numeric IDs
    $docker history image_name

    3.启动容器（run）
    # 在容器中运行"echo"命令，输出"hello word"
    $docker run image_name echo "hello word"
    # 交互式进入容器中
    $docker run -i -t image_name /bin/bash
    # 在容器中安装新的程序
    $docker run image_name apt-get install -y app_name

    4.查看容器（ps）
    # 列出当前所有正在运行的container
    $docker ps
    # 列出所有的container
    $docker ps -a
    # 列出最近一次启动的container
    $docker ps -l

    5.保存对容器的修改（commit）
    # 保存对容器的修改; -a, --author="" Author; -m, --message="" Commit message 
    $docker commit ID new_image_name

    6.对容器的操作（rm、stop、start、kill、logs、diff、top、cp、restart、attach
    # 删除所有容器
    $docker rm `docker ps -a -q`
    # 删除单个容器; -f, --force=false; -l, --link=false Remove the specified link and not the underlying container; -v, --volumes=false Remove the volumes associated to the container
    $docker rm Name/ID
    # 停止、启动、杀死一个容器
    $docker stop Name/ID
    $docker start Name/ID
    $docker kill Name/ID
    # 从一个容器中取日志; -f, --follow=false Follow log output; -t, --timestamps=false Show timestamps
    $docker logs Name/ID
    # 列出一个容器里面被改变的文件或者目录，list列表会显示出三种事件，A 增加的，D 删除的，C 被改变的
    $docker diff Name/ID
    # 显示一个运行的容器里面的进程信息
    $docker top Name/ID
    # 从容器里面拷贝文件/目录到本地一个路径
    $docker cp Name:/container_path to_path
    $docker cp ID:/container_path to_path
    # 重启一个正在运行的容器; -t, --time=10 Number of seconds to try to stop for before killing the container, Default=10
    $docker restart Name/ID
    # 附加到一个运行的容器上面; --no-stdin=false Do not attach stdin; --sig-proxy=true Proxify all received signal to the process
    $docker attach ID

    7.保存和加载镜像（save、load）
    # 保存镜像到一个tar包; -o, --output="" Write to an file
    $docker save image_name -o file_path
    # 加载一个tar包格式的镜像; -i, --input="" Read from a tar archive file
    $docker load -i file_path
    # 机器a
    $docker save image_name > /home/save.tar
    # 使用scp将save.tar拷到机器b上，然后：
    $docker load < /home/save.tar
    """)
