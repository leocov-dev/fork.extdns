import enum
import os
from dataclasses import dataclass
from typing import Mapping

import docker


class DnsType(enum.StrEnum):
    A='A'
    CNAME='CNAME'

@dataclass
class DnsRecord:
    type: DnsType
    name: str
    target: str
    ttl: int

@dataclass
class DnsLabel:
    record: DnsRecord

DnsConfig = Mapping[str, DnsLabel]

def get_container_dns_labels() -> DnsConfig:

    config = {}

    return config


__docker_client: docker.DockerClient | None = None
def get_docker_client() -> docker.DockerClient:
    global __docker_client
    if __docker_client is None:

        __docker_client = docker.from_env(use_ssh_client=_use_ssh_client())
    return __docker_client

def _use_ssh_client() -> bool:

    host = os.getenv('DOCKER_HOST', None)
    if not host:
        raise Exception('DOCKER_HOST not set')

    return host.startswith('ssh://')

