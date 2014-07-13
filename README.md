dockit
======

Dockit is an application to make your life better wrt managing docker actions (ex: run , pull, build, create, start ...etc) and to also help massive deployment of containers. 

This is also glued with gluster  (-g option of this binary) wrt huge gluster deployment. When in gluster action mode, it can be used to start any number of containers using the bricks exported ( configuration read from the config file) from host system. The gluster volume is created automatically ( volume name can be given as user input)  from the exported bricks . 

All you need to do is, mount gluster volume in your client!!

You can use this (dockit)executable for:

* Installing required docker packages in fedora/centos/rhel for docker.
* This binary is capable of starting docker deamon if its not running in your system.
* This binary can be used to pull docker images.
* This binary can build containers based on dockerfile.
* This binary can start containers based on provided image.
* This binary can be used to deploy gluster trusted pool on containers. 

#### PREPARE YOUR SETUP:

* Make sure "selinux" is turned off in the system where you run containers!!
* If you can install 'docker' packages in the system before running this binary, I will be happy :). Eventhough this binary
can install docker packages, yum transactions performed by this binary is very sensitive on minor errors like repodata error..etc
I am looking for alternatives.
* Base/official image 'pulling' (ex: ubuntu official image) is disabled for this version.  How-ever if you have specified base image in docker file, it should work..
* The image which you use for gluster deployment should have "ssh" deamon running in it.
 An example image can be found @https://index.docker.io/u/humble/fed20-gluster/
* Finally read the "help" output to use this in its full strength.
* When running this binary it may require 'image tag' at times, you can use default tag called 'latest' if you dont have any other choice.


#### How to start

Step 1: Clone the repo
```
https://github.com/humblec/dockit.git
```
Step 2: Install 'dockit'

```
#cd dockit
#python setup.py install
```

Step 3: Verify there exist a binary called 'dockit`

Step 4: If possible , install docker-io package in your distro(ex: fedora/centos/rhel)

Step 5: Read dockit's help

```
#dockit --help
```

Step 6: If you are planning to use it for gluster deployment ( -g option flag of dockit) and for automatic volume creation , create a file in your filesystem with below entry/entries for giving brick configuration. 

```
[root@ dockit]# cat /configfile 
BRICKS="/brick6,/brick7,/brick8,/brick9"
[root@dockit]# 

```

When invoking 'dockit' binary , If -g is enabled with --gv option , it will ask for below information, how-ever if you want to read these inputs
from configuration file , it is also possible (... -g -c '/home/hchiramm/configfile') by giving config file as an input:
```
Gluster Volume Type (ex: 2x2x1 where (distribute,replica, stripe count in order)     :2x2x1
Gluster Volume Name (ex: glustervol)     :myvol
Gluster Export Dir Name (ex: /rhs_bricks)    :/humble
Gluster brick file (ex: /home/configfile)    :/configfile
```

Where 'Volume Type' is the configuration of gluster configurtion wrt distribut-replica-stripe.. Volume name is self explanatory and 'Export Dir Name' will be the mount point inside the containers where brick is configured. The brick file is mentioned above.
For ex: If you give options like '2x2x1' which means it create 4 containers and brick names will be fetched in order from above config file. Make sure you have equal number of entries in your config file against the number of gluster containers you wish to spawn..




Step 7: Use it and Report bugs/comment/suggestions/RFEs @humble.devassy@gmail.com , if you come across any.


#### TODO:

[Fill later]


Lets run this executable:


```
[root@humbles-lap dockit]# dockit --help
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
Invoke dockit with any of (-d , -p, -b, -s) options

1. Install and Run Docker deamon                     (-d)   -->  dryrun
2. Pull image from docker repo and Run containers    (-p)   -->  requires -i <IMAGE> and -r <DOCKERREPO>
3. Build from dockerfile and Run Containers          (-b)   -->  requires -f <DOCKER FILE> and -t <IMAGE TAG>
4. Run container from existing image                 (-s)   -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>

 Optional:
 Create and start gluster containers  (-g)   -->  Effective only with -s option

                                                   (--gi) -->  To install Gluster From Source

                                                   (--gv) -->  To auto configure Gluster Volume
------------------------------------------------------------
None
dockit      : INFO     Dockit starting..
Usage: dockit [options]

Options:
  -h, --help            show this help message and exit
  -d, --dry_run         Do dry run - dont try to install any packages
  -p, --pullimage       Whether to pull from the docker repo ? Need to specify
                        dockerrepo and image name
  -s, --startc          Whether to start from an image ? Need to specify image
                        and tag
  -b, --buildimage      Whether to build image from the dockerfile? Need to
                        specify dockerfile path, and imagetag
  -g, --gluster_mode    Configure gluster volume in containers
  -i IMAGE, --image=IMAGE
                        Image name  - Containers will be based on this image
  -t IMAGETAG, --imgtag=IMAGETAG
                        Image tag name  - Containers will be assigned this tag
  -n COUNT, --count=COUNT
                        Number of containers to start  -
  -c CONFIGFILE, --configfile=CONFIGFILE
                        COnfig file path to read gluster configuration  -
  -f DOCKERFILE, --dockerfile=DOCKERFILE
                        Docker file path to build the container  -
  -r DOCKERREPO, --dockerrepo=DOCKERREPO
                        Docker repository name with a trailing blackslash  -
  --gv, --glustervolume
                        Gluster Volume Creation  inside containers  - Valid
                        with -g option
  --gi=GLUSTERVERSION, --glusterinstall=GLUSTERVERSION
                        Install gluster inside containers  - Valid with -g
                        option
```

If we run the binary with options:

Example 1: Pull an image (fed20-gluster) from docker repo (humble) and start 3 containers from it.

```
[root@humbles-lap dockit]#  dockit -p -i fed20-gluster -r humble -s -n 3
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
Invoke dockit with any of (-d , -p, -b, -s) options

1. Install and Run Docker deamon                     (-d)   -->  dryrun
2. Pull image from docker repo and Run containers    (-p)   -->  requires -i <IMAGE> and -r <DOCKERREPO>
3. Build from dockerfile and Run Containers          (-b)   -->  requires -f <DOCKER FILE> and -t <IMAGE TAG>
4. Run container from existing image                 (-s)   -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>

 Optional:
 Create and start gluster containers  (-g)   -->  Effective only with -s option

                                                   (--gi) -->  To install Gluster From Source

                                                   (--gv) -->  To auto configure Gluster Volume
------------------------------------------------------------
None
dockit      : INFO     Dockit starting..
Do you want to continue (y/n)y
dockit      : INFO     Proceeding
dockit      : INFO     Run containers natively, no mode configured
dockit      : INFO     Distribution:fedora Required ['docker-io', 'python-docker-py'] packages
 	 	 	 Making yum transactions
Loaded plugins: langpacks, refresh-packagekit, versionlock
Requirement already up-to-date: docker-py in /usr/lib/python2.7/site-packages
Requirement already up-to-date: requests==2.2.1 in /usr/lib/python2.7/site-packages/requests-2.2.1-py2.7.egg (from docker-py)
Requirement already up-to-date: six>=1.3.0 in /usr/lib/python2.7/site-packages (from docker-py)
Requirement already up-to-date: websocket-client==0.11.0 in /usr/lib/python2.7/site-packages/websocket_client-0.11.0-py2.7.egg (from docker-py)
Requirement already up-to-date: mock==1.0.1 in /usr/lib/python2.7/site-packages (from docker-py)
Cleaning up...
dockit      : INFO     Successfully pulled docker image:humble/fed20-gluster
root        : INFO     Enable Gluster Volume :0
dockit      : INFO       Information about running containers
dockit      : INFO     Containers are running successfully.. please login and work!!!!
------------------------------------------------------------
dockit      : INFO     Details about running containers..

dockit      : INFO     Container IPs 	 : [u'172.17.0.55', u'172.17.0.56', u'172.17.0.57']

dockit      : INFO     Container Ids 	 : [u'8ee194a323d7a28bfd70490c87bfbe3c76f48d578a24f89b063532874eceed77', u'8ee194a323d7a28bfd70490c87bfbe3c76f48d578a24f89b063532874eceed77', u'8ee194a323d7a28bfd70490c87bfbe3c76f48d578a24f89b063532874eceed77']

------------------------------------------------------------
dockit      : INFO     Done!

```


Example 2:

Start 4 containers using image humble/fed20-gluster with tag 'latest' and run in gluster mode and auto start volume by reading configuration from file /home/hchiramm/config

Where /home/hchiramm/config has below entries:



```
[root@humbles-lap dockit]# dockit -i humble/fed20-gluster -t latest -s -n 4 -g -c /home/hchiramm/config --gv
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
Invoke dockit with any of (-d , -p, -b, -s) options

1. Install and Run Docker deamon                     (-d)   -->  dryrun
2. Pull image from docker repo and Run containers    (-p)   -->  requires -i <IMAGE> and -r <DOCKERREPO>
3. Build from dockerfile and Run Containers          (-b)   -->  requires -f <DOCKER FILE> and -t <IMAGE TAG>
4. Run container from existing image                 (-s)   -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>

 Optional:
 Create and start gluster containers  (-g)   -->  Effective only with -s option

                                                   (--gi) -->  To install Gluster From Source

                                                   (--gv) -->  To auto configure Gluster Volume
------------------------------------------------------------
None
dockit      : INFO     Dockit starting..
Do you want to continue (y/n)y
dockit      : INFO     Proceeding
dockit      : INFO
 Need to configure gluster volume..

dockit      : INFO     Reading gluster configuration from config file
{'BRICKS': '/brick9,/brick10,/brick11,/brick12', 'VOLNAME': 'DemoVolume', 'VOL_TYPE': '2x2x1'}
dockit      : INFO     No of gluster containers to spawn:4
Do you want to continue (y/n):y
dockit      : INFO     Configuration read from configuration file
dockit      : INFO     {'BRICKS': '/brick9,/brick10,/brick11,/brick12', 'VOLNAME': 'DemoVolume', 'SERVER_EXPORT_DIR': 'default_server_Export', 'VOL_TYPE': '2x2x1'}
dockit      : INFO     Distribution:fedora Required ['docker-io', 'python-docker-py'] packages
 	 	 	 Making yum transactions
Loaded plugins: langpacks, refresh-packagekit, versionlock
Requirement already up-to-date: docker-py in /usr/lib/python2.7/site-packages
Requirement already up-to-date: requests==2.2.1 in /usr/lib/python2.7/site-packages/requests-2.2.1-py2.7.egg (from docker-py)
Requirement already up-to-date: six>=1.3.0 in /usr/lib/python2.7/site-packages (from docker-py)
Requirement already up-to-date: websocket-client==0.11.0 in /usr/lib/python2.7/site-packages/websocket_client-0.11.0-py2.7.egg (from docker-py)
Requirement already up-to-date: mock==1.0.1 in /usr/lib/python2.7/site-packages (from docker-py)
Cleaning up...
dockit      : INFO     Bricks will be using in order:['/brick9', '/brick10', '/brick11', '/brick12']
root        : INFO     Enable Gluster Volume :1

dockit      : INFO       Information about running containers
dockit      : INFO     Containers are running successfully.. please login and work!!!!
------------------------------------------------------------
dockit      : INFO     Details about running containers..

dockit      : INFO     Container IPs 	 : [u'172.17.0.60', u'172.17.0.61', u'172.17.0.62', u'172.17.0.63']

dockit      : INFO     Container Ids 	 : [u'0fa6d87f17fae00b91c7be15ea843c74c2ac46f8dfbd615c7d557d491caaa58d', u'0fa6d87f17fae00b91c7be15ea843c74c2ac46f8dfbd615c7d557d491caaa58d', u'0fa6d87f17fae00b91c7be15ea843c74c2ac46f8dfbd615c7d557d491caaa58d', u'0fa6d87f17fae00b91c7be15ea843c74c2ac46f8dfbd615c7d557d491caaa58d']

------------------------------------------------------------
dockit      : INFO     Gluster installation not required
dockit      : INFO     nodes are [u'172.17.0.61', u'172.17.0.60', u'172.17.0.63', u'172.17.0.62']
dockit      : INFO     Number of nodes: 4
dockit      : INFO     number of bricks:4


root        : INFO     Gluster Volume operations done


[root@dcd54b4a9463 /]# gluster
gluster> pool list
UUID					Hostname	State
cfa0dce8-9090-4a04-9e4d-74a2e37b49a4	172.17.0.60	Connected
cebac333-cfd8-4dbc-954a-6c2be0b16f7b	172.17.0.63	Connected
ee9b942f-2cb7-4af5-a14b-6fb212c8000b	172.17.0.62	Connected
2e1a6fae-a053-44ac-b0bc-7e1783cce6b4	localhost	Connected


```


Example 3: Install 3.4 gluster binary on 2 containers started using humble/fed20-gluster images.

```
[root@humbles-lap dockit]# dockit -i humble/fed20-gluster -t latest -s -n 2 -g -c /home/hchiramm/config --gi 3.4
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
Invoke dockit with any of (-d , -p, -b, -s) options

1. Install and Run Docker deamon                     (-d)   -->  dryrun
2. Pull image from docker repo and Run containers    (-p)   -->  requires -i <IMAGE> and -r <DOCKERREPO>
3. Build from dockerfile and Run Containers          (-b)   -->  requires -f <DOCKER FILE> and -t <IMAGE TAG>
4. Run container from existing image                 (-s)   -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>

 Optional:
 Create and start gluster containers  (-g)   -->  Effective only with -s option

                                                   (--gi) -->  To install Gluster From Source

                                                   (--gv) -->  To auto configure Gluster Volume
------------------------------------------------------------
None
dockit      : INFO     Dockit starting..
Do you want to continue (y/n)y
dockit      : INFO     Proceeding
dockit      : INFO     Need to install gluster inside containers
dockit      : INFO     Distribution:fedora Required ['docker-io', 'python-docker-py'] packages
 	 	 	 Making yum transactions
Loaded plugins: langpacks, refresh-packagekit, versionlock
Requirement already up-to-date: docker-py in /usr/lib/python2.7/site-packages
Requirement already up-to-date: requests==2.2.1 in /usr/lib/python2.7/site-packages/requests-2.2.1-py2.7.egg (from docker-py)
Requirement already up-to-date: six>=1.3.0 in /usr/lib/python2.7/site-packages (from docker-py)
Requirement already up-to-date: websocket-client==0.11.0 in /usr/lib/python2.7/site-packages/websocket_client-0.11.0-py2.7.egg (from docker-py)
Requirement already up-to-date: mock==1.0.1 in /usr/lib/python2.7/site-packages (from docker-py)
Cleaning up...
root        : INFO     Enable Gluster Volume :0
dockit      : INFO       Information about running containers
dockit      : INFO     Containers are running successfully.. please login and work!!!!
------------------------------------------------------------
dockit      : INFO     Details about running containers..

dockit      : INFO     Container IPs 	 : [u'172.17.0.73', u'172.17.0.74']

dockit      : INFO     Container Ids 	 : [u'3930da92c5d15948452fbd4b7332747576bf1d88d1fc4ce7cf631c72296e2c52', u'3930da92c5d15948452fbd4b7332747576bf1d88d1fc4ce7cf631c72296e2c52']

------------------------------------------------------------
dockit      : INFO     Trying to install gluster on [u'172.17.0.74', u'172.17.0.73'] nodes
dockit      : INFO     Configuring/installing on node:172.17.0.74

dockit      : INFO     Continuing ..

dockit      : INFO     Successfully configured GlusterFS binary on node:172.17.0.74
dockit      : INFO     Configuring/installing on node:172.17.0.73

dockit      : INFO     Successfully configured GlusterFS binary on node:172.17.0.73
dockit      : INFO     Successful Gluster Package Installation and GlusterFS Binary installation on all the nodes!
dockit      : INFO     Gluster Volume creation not required

```
So glusterd binary has been installed on above containers with '3.4' version.

Lets confirm:

```
ssh root[hchiramm@humbles-lap dockit]$ ssh root@172.17.0.74
root@172.17.0.74's password:
Last login: Sun Jul 13 17:55:20 2014 from 172.17.42.1
[root@2a04bf9182ad ~]# gluster
gluster     glusterd    glusterfs/  glusterfsd
[root@2a04bf9182ad ~]# glusterd --version
glusterfs 3.4git built on Jul 13 2014 18:11:48
Repository revision: git://git.gluster.com/glusterfs.git
Copyright (c) 2006-2013 Red Hat, Inc. <http://www.redhat.com/>
GlusterFS comes with ABSOLUTELY NO WARRANTY.
It is licensed to you under your choice of the GNU Lesser
General Public License, version 3 or any later version (LGPLv3
or later), or the GNU General Public License, version 2 (GPLv2),
in all cases as published by the Free Software Foundation.
[root@2a04bf9182ad ~]#
```


Example DockerFiles:

```

############################################################
# Dockerfile to run Gluster Containers
# Part of dockit project :https://github.com/humblec/dockit
############################################################

# Set the base image to Ubuntu if you need ubuntu

FROM fedora

# Set the file maintainer

MAINTAINER Humble Chirammal humble.devassy@gmail.com


RUN yum update

RUN yum install -y gluster*

RUN yum install -y openssh*

RUN mkdir /var/run/sshd

RUN echo "root:redhat"| chpasswd

EXPOSE 22

CMD ["/bin/bash"]



[root@humbles-lap dockit]# 

```

From a "fedora" base image it will install gluster packages and start containers from the built image. 

```
###docker ps

[root@humbles-lap dockit]# docker ps
CONTAINER ID        IMAGE                 COMMAND                CREATED              STATUS              PORTS                                          NAMES
7723fe4fdd15        mynewgluster:latest   /usr/bin/supervisord   About a minute ago   Up About a minute   0.0.0.0:49215->22/tcp, 0.0.0.0:49216->80/tcp   goofy_pare   




```
