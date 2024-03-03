#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir

def do_pack():
    """
    Generates a tgz archive of the web_static folder.
    Returns:
        Path to the created archive if successful, None otherwise.
    """
    try:
        # Get the current date and time as a string
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the 'versions' directory if it doesn't exist
        if not isdir("versions"):
            local("mkdir -p versions")

        # Define the file name for the archive
        file_name = "versions/web_static_{}.tgz".format(date)

        # Create the tar.gz archive
        local("tar -cvzf {} web_static".format(file_name))

        return file_name
    except Exception as e:
        print("Error:", str(e))
        return None

if __name__ == "__main__":
    result = do_pack()
    if result:
        print("Web static packed: {}".format(result))
    else:
        print("Packaging failed.")
