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

NEUNN_REGISTRY = 'index.neunn.com'
ALAUDA_REGISTRY = 'index.alauda.cn'

def parse_alauda_image(image, private_registry):
    if image.find('/') > 0:
        pulled_image = '%s/%s' % (private_registry, image)
    else:
        pulled_image = '%s/library/%s' % (private_registry, image)
    return pulled_image

def parse_neunn_image(image, private_registry):
    pass


def parse_image(image, private_registry):
    if private_registry == ALAUDA_REGISTRY:
        return parse_alauda_image(image, private_registry)
    return image


@click.command('pull', short_help='pull images from private registry')
@click.argument('images', nargs=-1)
@click.option('--private_registry', envvar='NIUKER_PRIVATE_REGISTRY',
              metavar='private_registry',
              help='set the private registry domain')
@pass_context
def cli(ctx, images, private_registry):
    """pull images from private registry

    images could be a list param
    """
    ctx.log('pull %s from %s' % (images, private_registry))
    for image in images:
        image = parse_image(image, private_registry)
        ctx.log('RUN: docker pull %s' % image)
        docker.pull(image)
        if private_registry:
            new_image = image.replace(private_registry, '')[1:]
            docker.tag(image, new_image)
            docker.rmi(image)

    print(docker.images())
