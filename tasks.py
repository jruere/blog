# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime
from pathlib import Path

from invoke import task
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

import localconf as LOCAL_CONFIG

# Github Pages configuration
#'github_pages_branch': 'gh-pages',
COMMIT_MESSAGE = f"'Publish site on {datetime.date.today().isoformat()}'"

@task
def clean(_):
    """Remove generated files"""
    path = Path(LOCAL_CONFIG.OUTPUT_PATH)
    if path.exists():
        assert path.is_dir()
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=False)


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
        LOCAL_CONFIG.OUTPUT_PATH,
        ('', LOCAL_CONFIG.PORT),
        ComplexHTTPRequestHandler)

    print(f"Serving on port {LOCAL_CONFIG.PORT} ...", file=sys.stderr)
    server.serve_forever()


@task(pre=[build, serve])
def reserve(_):
    """`build`, then `serve`"""


@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s publishconf.py')
