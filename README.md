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
* Install python-setuptools package or make sure you have 'setuptools' module available in your python path.
* If you are running in RHEL systems , please subscribe to EPEL channels as mentioned here (https://docs.docker.com/installation/rhel/)to make docker packages available.Also start docker process manually.
* If you can install 'docker' packages in the system before running this binary, I will be happy :). Eventhough this binary
can install docker packages, yum transactions performed by this binary is very sensitive on minor errors like repodata error..etc
I am looking for alternatives.
* Base/official image 'pulling' (ex: ubuntu official image) is disabled for this version.  How-ever if you have specified base image in docker file, it should work..
* The image which you use for gluster deployment should have "ssh" deamon running in it with ssh password 'redhat'.
 An example image can be found @https://index.docker.io/u/humble/fed20-gluster/
* [IMP] If you are using --gi option , its better if you can use an image which already have gluster build prerequisites packages ( http://gluster.org/community/documentation/index.php/Building_GlusterFS )installed , otherwise it can take long time.

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

Step 6: If you are planning to use it for gluster deployment ( -g option flag ) and for automatic volume creation (--gv), there are 2 ways to give input:


1) Give the configuration manually.
2) Let dockit read the configuration from a configuration file (-c option)

Either of above, you need a configuration file in your filesystem. The configuration file should have atleast  below entry.

```
[root@ dockit]# cat /configfile 
BRICKS="/brick6,/brick7,/brick8,/brick9"
[root@dockit]# 

```
If you opt for option 1 :

```
Gluster Volume Type (ex: 2x2x1 where (distribute,replica, stripe count in order)     :2x2x1
Gluster Volume Name (ex: glustervol)     :myvol
Gluster Export Dir Name (ex: /rhs_bricks)    :/humble
Gluster brick file (ex: /home/configfile)    :/configfile
```

Where 'Volume Type' is the configuration of gluster configurtion wrt distribut-replica-stripe.. Volume name is self explanatory and 'Export Dir Name' will be the mount point inside the containers where brick is configured. The brick file is mentioned above.
For ex: If you give options like '2x2x1' which means it create 4 containers and brick names will be fetched in order from above config file. Make sure you have equal number of entries in your config file against the number of gluster containers you wish to spawn..

If you opt for option 2, you may define these variables in config file,otherwise it will take default values for Volume name, Export Dir, Volume type..etc

```
[root@ dockit]# cat /configfile 
BRICKS="/brick6,/brick7,/brick8,/brick9"
VOLNAME="testvol"
VOL_TYPE="2x2x1"
SERVER_EXPORT_DIR="/rhs_bricks"

[root@dockit]# 
```


Step 7: Use it and Report bugs/comment/suggestions/RFEs @humble.devassy@gmail.com , if you come across any.


#### TODO:

* Remove pre-defined ssh password dependency on the image.
[list to be filled later]


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
dockit      : INFO     {'BRICKS': '/brick9,/brick10,/brick11,/brick12', 'VOLNAME': 'DemoVolume', 'SERVER_EXPORT_DIR': '/defaultExport', 'VOL_TYPE': '2x2x1'}
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
...
...
...
...
dockit      : INFO       Information about running containers 
dockit      : INFO     Containers are running successfully.. please login and work!!!!
------------------------------------------------------------
dockit      : INFO     Details about running containers..

dockit      : INFO     Container IPs 	 : [u'172.17.0.75', u'172.17.0.76', u'172.17.0.77', u'172.17.0.78']
 
dockit      : INFO     Container Ids 	 : [u'3bfbbe4d53ad0ff7424b87fdffa24f58cb176cbde9673e5ec3bddf2dc89fe005', u'3bfbbe4d53ad0ff7424b87fdffa24f58cb176cbde9673e5ec3bddf2dc89fe005', u'3bfbbe4d53ad0ff7424b87fdffa24f58cb176cbde9673e5ec3bddf2dc89fe005', u'3bfbbe4d53ad0ff7424b87fdffa24f58cb176cbde9673e5ec3bddf2dc89fe005'] 
 
------------------------------------------------------------
dockit      : INFO     Gluster installation not required
dockit      : INFO     nodes are [u'172.17.0.76', u'172.17.0.77', u'172.17.0.75', u'172.17.0.78']
dockit      : INFO     Number of nodes: 4
dockit      : INFO     number of bricks:4









volume create: DemoVolume: success: please start the volume to access data

root        : INFO     Gluster Volume operations done

```

Lets login to one of the container and check the gluster configuration:

```
[root@humbles-lap dockit]# ssh root@172.17.0.76
The authenticity of host '172.17.0.76 (172.17.0.76)' can't be established.
RSA key fingerprint is c0:b6:86:7a:b6:61:21:f1:05:16:ee:62:c1:e8:d4:1f.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '172.17.0.76' (RSA) to the list of known hosts.
root@172.17.0.76's password: 
[root@bb7c8d37d5db ~]# gluster v i
 
Volume Name: DemoVolume
Type: Distributed-Replicate
Volume ID: 494574bc-ab2a-4034-996e-4a376395558a
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: 172.17.0.76:/defaultExport/DemoVolume_brick0
Brick2: 172.17.0.77:/defaultExport/DemoVolume_brick1
Brick3: 172.17.0.75:/defaultExport/DemoVolume_brick2
Brick4: 172.17.0.78:/defaultExport/DemoVolume_brick3
[root@bb7c8d37d5db ~]# 
[root@bb7c8d37d5db ~]# gluster peer status
Number of Peers: 3

Hostname: 172.17.0.77
Uuid: ec2a2b78-84fb-4f67-bff9-52c5ab8c1829
State: Peer in Cluster (Connected)

Hostname: 172.17.0.75
Uuid: 266cdf12-01d7-4528-91b2-d932298127de
State: Peer in Cluster (Connected)

Hostname: 172.17.0.78
Uuid: 71230049-ee31-40d1-80f2-58a0800f8ac0
State: Peer in Cluster (Connected)
[root@bb7c8d37d5db ~]# 

```
Cool, the gluster volume has started perfectly!!

Lets try to mount it on the host.

```
[root@humbles-lap dockit]# mount -t glusterfs 172.17.0.76:/DemoVolume /mnt
[root@humbles-lap dockit]# ll /mnt/
total 0
[root@humbles-lap dockit]# mount |grep glusterfs
172.17.0.76:/DemoVolume on /mnt type fuse.glusterfs (rw,relatime,user_id=0,group_id=0,default_permissions,allow_other,max_read=131072)
[root@humbles-lap dockit]# 


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
