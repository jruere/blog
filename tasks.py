# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime

from invoke import task
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

CONFIG = {
    # Local path configuration (can be absolute or relative to tasks.py)
    'deploy_path': 'docs',
    # Github Pages configuration
    #'github_pages_branch': 'gh-pages',
    'commit_message': "'Publish site on {}'".format(datetime.date.today().isoformat()),
    # Port for `serve`
    'port': 8000,
}

@task
def clean(_):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])

@task
def build(c):
    """Build local version of site"""
    c.run('pelican -s localconf.py')

@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run('pelican -d -s localconf.py')

@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    c.run('pelican -r -s localconf.py')

@task
def serve(_):
    """Serve site at http://localhost:8000/"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG['deploy_path'],
        ('', CONFIG['port']),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {port} ...\n'.format(**CONFIG))
    server.serve_forever()

@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)

@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s publishconf.py')
