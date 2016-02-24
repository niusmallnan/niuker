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
from __future__ import print_function

import click
from niuker.cli import pass_context
from sh import docker

@click.group()
def cli():
    """clean docker containers or images"""
    pass


@cli.command()
@click.option('--force', '-f', is_flag=True, help='force remove containers')
@click.option('--all', '-a', is_flag=True, help='remove all the containers')
@pass_context
def containers(ctx, force, all):
    """clean docker containers which not running"""
    all_containers = docker.ps('-a', '-q').stdout.split()
    if all:
        removed_containers = all_containers
    else:
        running_containers = docker.ps('-q').stdout.split()
        removed_containers = set(all_containers) ^ set(running_containers)
    for cid in removed_containers:
        ctx.log('docker removing container %s' % cid)
        if force:
            print(docker.rm('-f', cid))
        else:
            print(docker.rm(cid))

    ctx.log('list all containers')
    print(docker.ps('-a'))


@cli.command()
@click.option('--force', '-f', is_flag=True, help='force remove images')
@click.option('--all', '-a', is_flag=True, help='remove all the images')
@pass_context
def images(ctx, force, all):
    """clean docker images which has no tag"""
    if all:
        ctx.log('clean all images')
        removed_images = docker.images('-q')
    else:
        ctx.log('clean images only no tag')
        removed_images = docker.images("--filter='dangling=true'", '-q')
    for img_id in removed_images.split():
        ctx.log('docker removing image %s' % img_id)
        if force:
            print(docker.rmi('-f', img_id))
        else:
            print(docker.rmi(img_id))

    ctx.log('list all images')
    print(docker.images())
