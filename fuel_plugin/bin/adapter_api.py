#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright 2013 Mirantis, Inc.
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
import logging
import signal
import pecan
from gevent import pywsgi

from fuel_plugin.ostf_adapter import cli_config
from fuel_plugin.ostf_adapter import nailgun_hooks
from fuel_plugin.ostf_adapter import logger
from fuel_plugin.ostf_adapter.wsgi import app
from fuel_plugin.ostf_adapter.nose_plugin.nose_discovery import discovery
from fuel_plugin.utils.utils import clean_db, cache_data
from fuel_plugin.ostf_adapter.storage import engine


def main():

    cli_args = cli_config.parse_cli()

    config = {
        'server': {
            'host': cli_args.host,
            'port': cli_args.port
        },
        'dbpath': cli_args.dbpath,
        'debug': cli_args.debug,
        'debug_tests': cli_args.debug_tests,
        'nailgun': {
            'host': cli_args.nailgun_host,
            'port': cli_args.nailgun_port
        }
    }

    logger.setup(log_file=cli_args.log_file)

    log = logging.getLogger(__name__)

    root = app.setup_app(config=config)

    if getattr(cli_args, 'after_init_hook'):
        return nailgun_hooks.after_initialization_environment_hook()

    #performing cleaning of expired data (if any) in db
    clean_db()

    #discover testsets and their tests
    CORE_PATH = pecan.conf.debug_tests if \
        pecan.conf.get('debug_tests') else 'fuel_health'

    discovery(path=CORE_PATH, session=engine.get_session())

    #cache needed data from test repository
    cache_data()

    host, port = pecan.conf.server.host, pecan.conf.server.port
    srv = pywsgi.WSGIServer((host, int(port)), root)

    log.info('Starting server in PID %s', os.getpid())
    log.info("serving on http://%s:%s", host, port)

    try:
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
