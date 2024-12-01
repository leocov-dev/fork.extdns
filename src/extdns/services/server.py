#!/usr/bin/env python

import os
import time
from collections import defaultdict

import docker
import requests
from loguru import logger


def legacy():
    sleep_timeout = int(os.getenv('SLEEP_TIMEOUT', '300'))

    use_ssh_client = False
    docker_host = os.getenv('DOCKER_HOST', None)
    if docker_host and docker_host.startswith("ssh://"):
        use_ssh_client = True

    client = docker.from_env(use_ssh_client=use_ssh_client)

    while True:
        ip = os.getenv('EXTERNAL_IP', requests.get('https://checkip.amazonaws.com').text.strip())
        logger.info(f'update IP: {ip}')

        records_list = defaultdict(set)

        for c in client.containers.list():
            for label, domain in c.labels.items():
                if label.startswith('extdns.'):
                    provider = label.split('.')[1]
                    records_list[provider].add(domain)

        logger.info(f'extracted domains from docker labels: {records_list}')
        # cf.update(records_list, ip)
        time.sleep(sleep_timeout)
