#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

# Define the remote server hosts
env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(archive_path):
    """Distribute an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        # Extract important file and folder names
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        release_dir = "/data/web_static/releases/"
        current_dir = "/data/web_static/current"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the release directory if it doesn't exist
        run('mkdir -p {}{}/'.format(release_dir, no_extension))

        # Extract the archive into the release directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, release_dir, no_extension))

        # Remove the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(file_name))

        # Move the contents of the web_static folder to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(release_dir, no_extension))

        # Remove the now-empty web_static folder
        run('rm -rf {}{}/web_static'.format(release_dir, no_extension))

        # Update the symbolic link to the current release
        run('rm -rf {}'.format(current_dir))
        run('ln -s {}{}/ {}'.format(release_dir, no_extension, current_dir))

        return True
    except Exception as e:
        print("Error:", str(e))
        return False
