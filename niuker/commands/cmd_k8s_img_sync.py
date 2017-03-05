from __future__ import print_function

import click
from sh import docker
from niuker.cli import pass_context


DEFAULT_REGISTRY = 'registry.cn-hangzhou.aliyuncs.com'
DEFAULR_NAMESPACE = "rancher-cn"


@click.command('k8s-img-sync', short_help='sync rancher k8s images')
@click.option('--image-file', '-f', type=click.File('r'))
@pass_context
def cli(ctx, image_file):
    """sync images to docker machine hosts

    for example:

    \b
        #sync k8s images
        niuker k8s-img-sync -f <image_file>
    """
    if not image_file:
        return
    for pull_image in image_file.readlines(image_file):
        if len(pull_image) == 0:
            continue
        docker.pull(pull_image)
        push_image = '%s/%s/%s' % (DEFAULT_REGISTRY,
                                  DEFAULR_NAMESPACE,
                                  pull_image.split('/')[-1])
        docker.tag(pull_image, push_image)
        docker.push(push_image)


__command_name__ = 'k8s-img-sync'
