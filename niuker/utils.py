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
import os

try:
    from sh import docker_machine
except ImportError:
    print('docker-machine needed')


def get_machine_hosts(hosts, exclude):
    if hosts:
        return list(hosts)
    all_hosts = docker_machine.ls('-q').split()
    if not exclude:
        return list(all_hosts)
    return list(set(all_hosts) ^ set(exclude))


def set_host_environ(host):
    for temp in docker_machine.env(host).split():
        if temp.startswith('DOCKER'):
            key =temp.split('=')[0]
            value = temp.split('=')[1].replace('"', '')
            os.environ[key] = value


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.

    """
    for v in vars:
        value = os.environ.get(v)
        if value:
            return value
    return kwargs.get('default', '')
