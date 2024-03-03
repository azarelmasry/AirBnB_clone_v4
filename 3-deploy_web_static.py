#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['142.44.167.228', '144.217.246.195']

def do_pack():
    """
    Generates a tgz archive of the web_static folder.
    Returns:
        Path to the created archive if successful, None otherwise.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print("Error:", str(e))
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    Args:
        archive_path (str): Path to the archive file to be deployed.
    Returns:
        True if deployment was successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the release directory if it doesn't exist
        run('mkdir -p {}{}/'.format(path, no_ext))

        # Extract the archive into the release directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))

        # Remove the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(file_name))

        # Move the contents of the web_static folder to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))

        # Remove the now-empty web_static folder
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        # Update the symbolic link to the current release
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        return True
    except Exception as e:
        print("Error:", str(e))
        return False

def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
