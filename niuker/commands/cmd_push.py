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


@click.command('push', short_help='push images to private registry')
@click.argument('images', nargs=-1)
@click.option('--private_registry', envvar='NIUKER_PRIVATE_REGISTRY',
              metavar='private_registry',
              help='set the private registry domain')
@pass_context
def cli(ctx, images, private_registry):
    """push images to private registry

    images could be a list param
    """
    ctx.log('push %s to %s' % (images, private_registry))
    if not private_registry:
        return
    for image in images:
        new_image = '%s/%s' % (private_registry, image)
        docker.tag(image, new_image)
        ctx.log('RUN: docker push %s' % new_image)
        print(docker.push(new_image))
        docker.rmi(new_image)
