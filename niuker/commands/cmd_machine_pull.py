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
from niuker.cli import pass_context
from niuker.commands import cmd_pull
from niuker.utils import get_machine_hosts, set_host_environ
from sh import docker
from sh import niuker
from sh import sleep


def pull_images(ctx, hosts, images):
    for host in hosts:
        set_host_environ(host)
        try:
            ctx.log('pulling %s on %s' % (images, host))
            niuker.pull(images)
        except:
            ctx.log('failed pull on %s' % host)


@click.command('machine-pull', short_help='pull images on docker machine env')
@click.argument('images', nargs=-1)
@click.option('--hosts', '-h', multiple=True, metavar='specific_host',
              help='pull images on specific hosts')
@click.option('--exclude', '-e', multiple=True, metavar='exclude_host',
              help='exclude some hosts')
@pass_context
def cli(ctx, images, hosts, exclude):
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
    docker_hosts = get_machine_hosts(hosts, exclude)
    ctx.log('Hosts:\n%s' % '\n'.join(docker_hosts))
    ctx.log('sleep 10s waiting for you')
    sleep(10)
    pull_images(ctx, docker_hosts, images)


__command_name__ = 'machine-pull'
