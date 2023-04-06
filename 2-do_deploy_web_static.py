#!/usr/bin/python3
"""a script to send an archive file to a remote server
and decompress it"""

from fabric.api import run, env, put
import os.path

env.hosts = ['54.144.221.234', '100.26.154.245']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'


def do_deploy(archive_path):
    """a function to deploy code and decompress it"""

    # Check if the archive file exists and is not a directory
    if not os.path.isfile(archive_path) or os.path.isdir(archive_path):
        return False

    try:
        remote_path = "/data/web_static/releases/"
        sym_link = "/data/web_static/current"

        # Upload the archive file to the remote server
        put(archive_path, "/tmp/")

        # Extract the files from the archive to a new release directory
        run("sudo mkdir -p {}{}".format(remote_path, os.path.basename(
            archive_path).replace(".tgz", "").replace(".tar.gz", "")))
        run("sudo tar -xzf /tmp/{} -C {}{}/".format(os.path.basename(
            archive_path), remote_path, os.path.basename(
                archive_path).replace(".tgz", "").replace(".tar.gz", "")))

        # Remove the archive file from the remote server
        run("sudo rm /tmp/{}".format(os.path.basename(archive_path)))

        # Update the symbolic link to point to the new release
        run("sudo rm -rf {}".format(sym_link))
        run("sudo ln -s {} {}".format(remote_path, sym_link))

        return True
    except Exception as e:
        return False
