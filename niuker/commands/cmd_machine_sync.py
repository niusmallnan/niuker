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
from sh import docker
from sh import sleep
from niuker.cli import pass_context
from niuker.utils import get_machine_hosts, set_host_environ


def sync_images(ctx, docker_hosts, image_files):
    for host in docker_hosts:
        set_host_environ(host)
        for f in image_files:
            try:
                ctx.log('loading %s on %s' % (f, host))
                docker.load('-i', f)
            except:
                ctx.log('failed load %s on %s' % (f, host))


@click.command('machine-sync', short_help='sync images to docker machine hosts')
@click.argument('image_files', nargs=-1, type=click.Path(exists=True))
@click.option('--hosts', '-h', multiple=True, metavar='specific_host',
              help='sync images to specific hosts')
@click.option('--exclude', '-e', multiple=True, metavar='exclude_host',
              help='sync images exclude some hosts')
@pass_context
def cli(ctx, image_files, hosts, exclude):
    """sync images to docker machine hosts

    for example:

    \b
        #sync all hosts
        niuker machine-sync ubuntu.tar alpine.tar
    \b
        #sync to specific hosts
        niuker machine-sync ubuntu.tar alpine.tar -h xxxx -h yyyyy
    \b
        #sync exclude some hosts
        niuker machine-sync ubuntu.tar alpine.tar -e xxxx -e yyyyy
    """
    if not image_files:
        return
    if hosts and exclude:
        ctx.log('never use hosts and exclude together')
        return
    docker_hosts = get_machine_hosts(hosts, exclude)
    ctx.log('Hosts:\n%s' % '\n'.join(docker_hosts))
    ctx.log('sleep 10s waiting for you')
    sleep(10)
    sync_images(ctx, docker_hosts, image_files)



__command_name__ = 'machine-sync'

