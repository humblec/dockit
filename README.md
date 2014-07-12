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

When -g is enabled, when invoking 'dockit' binary it will ask for below information, how-ever if want to read these inputs
from configuration file , it is also possible (... -g -c '/home/hchiramm/configfile'):
```
Gluster Volume Type (ex: 2x2x1 where (distribute,replica, stripe count in order)     :2x2x1
Gluster Volume Name (ex: glustervol)     :myvol
Gluster Export Dir Name (ex: /rhs_bricks)    :/humble
Gluster brick file (ex: /home/configfile)    :/configfile
```

Where 'Volume Type' is the configuration of gluster deployement which you wish.. Volume name is self explanatory and 'Export Dir Name' will be the mount point inside the containers where brick is configured. The brick file is mentioned above.
For ex: If you give options like '2x2x1' which means it create 4 containers and brick names will be fetched in order from above config file. Make sure you have equal number of entries in your config file against the number of gluster containers you wish to spawn..




Step 7: Use it and Report bugs/comment/suggestions/rfes @humble.devassy@gmail.com , if you come across any. 


#### TODO:

[Fill later]


Lets run this executable:


```
[root@humbles-lap dockit]# dockit --help
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
You should invoke dockit with any of (-d , -p, -b, -s) options 

1. Install and Run Docker deamon                  (-d) -->  dryrun   
2. Pull image from docker repo and Run containers (-p) -->  requires -i <IMAGE> and -r <DOCKERREPO>
3. Build from dockerfile and Run Containers       (-b) -->  requires -f <DOCKER FILE> and -t <IMAGE TAG> 
4. Run container from existing image              (-s) -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>
Optional: Create and start gluster containers     (-g) -->  Effective only with -s option
------------------------------------------------------------
None
Dockit process logs are available at /var/log/dockit.log 
Would you like to continue? (y/n)y
Continuing..
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
  -i IMAGE, --image=IMAGE
                        Image name  - Containers will be based on this image
  -t IMAGETAG, --imgtag=IMAGETAG
                        Image tag name  - Containers will be assigned this tag
  -n COUNT, --count=COUNT
                        Number of containers to start  -
  -f DOCKERFILE, --dockerfile=DOCKERFILE
                        Docker file path to build the container  -
  -r DOCKERREPO, --dockerrepo=DOCKERREPO
                        Docker repository name with a trailing blackslash  -


```

If we run the binary with options:

Example 1: Below example ask 'dockit' to pull image (-p) called 'fed20-gluster' from docker repo (-r) 'humble' with tag 'latest' 
and start (-s) 3 (-n 3) containers , then deploy gluster!! If you have enabled '-g' the number of containers ( 3 here) are masked
and the configuration will be based on the input like '2x2x1' which will be fetched as soon as you start the binary.
  

```

[root@humbles-lap dockit]# dockit -p -i fed20-gluster -r humble -s -n 3 -g
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
Invoke dockit with any of (-d , -p, -b, -s) options 

1. Install and Run Docker deamon                  (-d) -->  dryrun   
2. Pull image from docker repo and Run containers (-p) -->  requires -i <IMAGE> and -r <DOCKERREPO>
3. Build from dockerfile and Run Containers       (-b) -->  requires -f <DOCKER FILE> and -t <IMAGE TAG> 
4. Run container from existing image              (-s) -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>
Optional: Create and start gluster containers     (-g) -->  Effective only with -s option
------------------------------------------------------------
None
INFO:root:Dockit process logs are available at /var/log/dockit.log 
DEBUG:root:Input 	 :[['count', '3'], ['image', 'fed20-gluster'], ['glumode', True], ['pullimg', True], ['startc', True], ['dockerrepo', 'humble']]
INFO:root:image tag : latest , docker repo:humble
Do you want to continue (y/n)y
Proceeding 
INFO:root:
 Need to configure gluster volumes, taking inputs 
Gluster Volume Type (ex: 2x2x1 where (distribute,replica, stripe count in order)	 :2x2x1
Gluster Volume Name (ex: glustervol)	 :myvol
Gluster Export Dir Name (ex: /rhs_bricks)	 :/humble
Gluster brick file (ex: /home/configfile)	 :/configfile
No of gluster containers to spawn:4
Do you want to continue (y/n):y
Continuing with..
{'BRICKS': '/brick6,/brick7,/brick8,/brick9', 'VOLNAME': 'myvol', 'BRICK_FILE': '/configfile', 'SERVER_EXPORT_DIR': '/humble', 'VOL_TYPE': '2x2x1'}
Loaded plugins: langpacks, refresh-packagekit
Containers: 51
Images: 19
Driver: devicemapper
 Pool Name: docker-253:1-1051107-pool
 Data file: /var/lib/docker/devicemapper/devicemapper/data
 Metadata file: /var/lib/docker/devicemapper/devicemapper/metadata
 Data Space Used: 3378.4 Mb
 Data Space Total: 102400.0 Mb
 Metadata Space Used: 5.9 Mb
 Metadata Space Total: 2048.0 Mb
 Successfully connected to docker deamon: 

May perform any action : pull/build/start containers according to the input
Done with pulling....continuing
Going to run the containers
  Information about running containers 

 Ip address :172.17.0.14

 Ip address :172.17.0.15

 Ip address :172.17.0.16

 Ip address :172.17.0.17

  Containers are running successfully.. please login and work!!!!
Received below configuration from caller
{'SERVER_IP_ADDRS': [u'172.17.0.14', u'172.17.0.15', u'172.17.0.16', u'172.17.0.17'], 'SERVER_EXPORT_DIR': '/humble', 'VOLNAME': 'myvol', 'VOL_TYPE': '2x2x1', 'TRANS_TYPE': 'tcp'}
nodes are [u'172.17.0.14', u'172.17.0.15', u'172.17.0.16', u'172.17.0.17']
Number of nodes: 4
number of bricks:4
command to execute: pgrep glusterd || glusterd
node: 172.17.0.14
command: pgrep glusterd || glusterd
exit status: 0


------------------------------------------------------------



command to execute: pgrep glusterd || glusterd
node: 172.17.0.15
command: pgrep glusterd || glusterd
exit status: 0


------------------------------------------------------------



command to execute: pgrep glusterd || glusterd
node: 172.17.0.16
command: pgrep glusterd || glusterd
exit status: 0


------------------------------------------------------------



command to execute: pgrep glusterd || glusterd
node: 172.17.0.17
command: pgrep glusterd || glusterd
exit status: 0


------------------------------------------------------------



command to execute: gluster peer probe 172.17.0.15
command to execute: gluster peer probe 172.17.0.16
command to execute: gluster peer probe 172.17.0.17
command to execute: gluster --mode=script volume create myvol replica 2  transport tcp 172.17.0.14:/humble/myvol_brick0 172.17.0.15:/humble/myvol_brick1 172.17.0.16:/humble/myvol_brick2 172.17.0.17:/humble/myvol_brick3 force
node: 172.17.0.14
command: gluster --mode=script volume create myvol replica 2  transport tcp 172.17.0.14:/humble/myvol_brick0 172.17.0.15:/humble/myvol_brick1 172.17.0.16:/humble/myvol_brick2 172.17.0.17:/humble/myvol_brick3 force
exit status: 0
volume create: myvol: success: please start the volume to access data


------------------------------------------------------------



command to execute: gluster --mode=script volume start myvol
Dockit finished...
```
Now, login and verify :)

```
[root@gprfc034 dockit]# ssh root@172.17.0.16
The authenticity of host '172.17.0.16 (172.17.0.16)' can't be established.
RSA key fingerprint is c0:b6:86:7a:b6:61:21:f1:05:16:ee:62:c1:e8:d4:1f.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '172.17.0.16' (RSA) to the list of known hosts.
root@172.17.0.16's password: 
[root@bc4b4f1d0433 ~]# ls


[root@gprfc034 brick8]# ssh root@172.17.0.16
root@172.17.0.16's password: 
Last login: Wed Jun  4 15:52:06 2014 from 172.17.42.1
[root@bc4b4f1d0433 ~]# gluster v i
 
Volume Name: myvol
Type: Distributed-Replicate
Volume ID: a9cab755-d924-47a7-b358-e664d0626bc0
Status: Started
Number of Bricks: 2 x 2 = 4
Transport-type: tcp
Bricks:
Brick1: 172.17.0.14:/humble/myvol_brick0
Brick2: 172.17.0.15:/humble/myvol_brick1
Brick3: 172.17.0.16:/humble/myvol_brick2
Brick4: 172.17.0.17:/humble/myvol_brick3
[root@bc4b4f1d0433 ~]# 

```

Now 'glustervol' can be mounted in client as shown below:

```
[root@gprfc034 root]# mkdir /m
[root@gprfc034 root]# mount -t glusterfs 172.17.0.14:/myvol /m
[root@gprfc034 root]# cd /m
[root@gprfc034 m]# ls
[root@gprfc034 m]#

```

If you specify the option to read from config file as shown below, it will be more automated.

```
[root@humbles-lap dockit]# dockit -p -i fed20-gluster -r humble -s -n 3 -g -c /home/hchiramm/config
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
Invoke dockit with any of (-d , -p, -b, -s) options

1. Install and Run Docker deamon                  (-d) -->  dryrun
2. Pull image from docker repo and Run containers (-p) -->  requires -i <IMAGE> and -r <DOCKERREPO>
3. Build from dockerfile and Run Containers       (-b) -->  requires -f <DOCKER FILE> and -t <IMAGE TAG>
4. Run container from existing image              (-s) -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>
Optional: Create and start gluster containers     (-g) -->  Effective only with -s option
------------------------------------------------------------
None
INFO:root:Dockit process logs are available at /var/log/dockit/dockit.log
INFO:root:image tag : latest , docker repo:humble
Do you want to continue (y/n)Proceeding
INFO:root:
 Need to configure gluster volumes, taking inputs

Reading gluster configuration from config file
{'BRICKS': '/brick3,/brick6,/brick7,/brick8', 'VOLNAME': 'MYGLUSTER', 'VOL_TYPE': '1x2x1'}
INFO:root:No of gluster containers to spawn:2
Do you want to continue (y/n):y
Configuration read from configuration file
Continuing with..
{'BRICKS': '/brick3,/brick6,/brick7,/brick8', 'VOLNAME': 'MYGLUSTER', 'SERVER_EXPORT_DIR': 'default_server_Export', 'VOL_TYPE': '1x2x1'}

.................

INFO:root:Details about running containers..

INFO:root:Container IPs 	 : [u'172.17.0.2', u'172.17.0.3']

INFO:root:Container Ids 	 : [u'1c4a2d72892186f5f68225be5c59f96872c5fcfdd3e8406a2cfe2e5dc26caf2c', u'1c4a2d72892186f5f68225be5c59f96872c5fcfdd3e8406a2cfe2e5dc26caf2c']

 ...........
```

Example 2: Below example ask 'dockit' to build (-b) a new image using docker file (-f) /home/hchiramm/dockit/dockerfiles and tag it to 'mynewgluster'(-t) and start (-s) containers from it.

```

[root@humbles-lap dockit]# dockit -b -t mynewgluster -f /home/hchiramm/dockit/dockerfiles/ -s 1 
Dockit process logs are available at /var/log/dockit.log 
------------------------------------------------------------
   M A I N - M E N U - O F - DOCKIT
------------------------------------------------------------
1. Install and Run Docker                             --> Configure: dryrun   (-d) option 
2. Pull image from docker repo and Run container      --> Configure: pullimg  (-p) option 
3. Build from dockerfile and Run Container            --> Configure: buildimg (-b) option
4. Run container from existing image                  --> Configure: startC   (-s) option
Optional: Create and start gluster containers     (-g) -->  Effective only with -s option
------------------------------------------------------------
........ [truncated]
Do you want to continue (y/n)y
Proceeding 
Loaded plugins: langpacks, refresh-packagekit, versionlock
Containers: 6
Images: 89
Storage Driver: devicemapper
 Pool Name: docker-8:10-1063742-pool
 Data file: /var/lib/docker/devicemapper/devicemapper/data
 Metadata file: /var/lib/docker/devicemapper/devicemapper/metadata
 Data Space Used: 2439.8 Mb
 Data Space Total: 102400.0 Mb
 Metadata Space Used: 3.8 Mb
 Metadata Space Total: 2048.0 Mb
Execution Driver: native-0.1
Kernel Version: 3.10.4-300.fc19.x86_64
Username: humble
Registry: [https://index.docker.io/v1/]
WARNING: No swap limit support
 Successfully connected to docker deamon: 

May perform any action : pull/build/start containers according to the input
Continuing build process with /home/hchiramm/dockit/dockerfiles/

Going to run the containers
  Information about running containers 

 Ip address :172.17.0.5

  Containers are running successfully.. please login and work!!!!
Dockit finished...

```



==============================================================



Example DockerFiles: 

1


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
