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
import sh
import os
from niuker.cli import pass_context
from niuker.commands import cmd_pull
from sh import docker
from sh import niuker
from sh import sleep
try:
    from sh import docker_machine
except ImportError:
    print('docker-machine needed')


def get_machine_hosts():
    return docker_machine.ls('-q').split()


def set_environ(host):
    for temp in docker_machine.env(host).split():
        if temp.startswith('DOCKER'):
            key =temp.split('=')[0]
            value = temp.split('=')[1].replace('"', '')
            os.environ[key] = value


def pull_image(ctx, hosts, images, private_registry):
    for host in hosts:
        set_environ(host)
        ctx.log('pull %s on %s' % (images, host))
        try:
            niuker.pull(images)
        except:
            ctx.log('failed pull on %s' % host)


@click.command('machine-pull', short_help='pull images on docker machine env')
@click.argument('images', nargs=-1)
@click.option('--hosts', '-h', multiple=True, metavar='specific_host',
              help='pull images on specific hosts')
@click.option('--exclude', '-e', multiple=True, metavar='exclude_host',
              help='exclude some hosts')
@click.option('--private_registry', envvar='NIUKER_PRIVATE_REGISTRY',
              metavar='private_registry',
              help='set the private registry domain')
@pass_context
def cli(ctx, images, hosts, exclude, private_registry):
    """pull images on docker machine env

    for example:

    \b
        #default pull on all hosts
        niuker machine-pull ubuntu alpine
    \b
        #pull on specific hosts
        niuker machine-pull ubuntu alpine -h xxxx -h yyyyy
    \b
        #pull exclude some hosts
        niuker machine-pull ubuntu alpine -e xxxx -e yyyyy
    """
    if not images:
        return
    if hosts and exclude:
        ctx.log('never use hosts and exclude together')
        return
    elif hosts:
        docker_hosts = hosts
    elif exclude:
        all_hosts = get_machine_hosts()
        docker_hosts = set(all_hosts) ^ set(exclude)
    else:
        docker_hosts = get_machine_hosts()
    ctx.log('Hosts:\n%s' % '\n'.join(list(docker_hosts)))
    ctx.log('sleep 10s waiting for you')
    sleep(10)
    pull_image(ctx, docker_hosts, images, private_registry)


__command_name__ = 'machine-pull'
