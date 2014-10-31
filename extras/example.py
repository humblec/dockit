import docker
import sys

# part of https://github.com/humblec/dockit.git
# make sure docker module is availble , if not do
# pip install docker-py

DOCK_SOCK = "unix://var/run/docker.sock"
DOCK_VERSION = "1.9"



if __name__ == "__main__":
# Program to Connect to docker deamon and talk

    try:
        conn = docker.Client(base_url=DOCK_SOCK, version=DOCK_VERSION, timeout=30)
        if conn:
            print "Successfully Connected to the docker deamon \n "
            print "Available methods with connection object %s \n" %(dir(conn))
            print "Retrieve docker information \n"
            print conn.info()
        else:
            print "Connection Failed "
    except Exception as e:
            print e
            sys.exit(1)


