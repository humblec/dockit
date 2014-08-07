#!/usr/bin/python


# Copyright (C) 2014 Red Hat Inc.
# Author Humble Chirammal <humble.devassy@gmail.com> | <hchiramm@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import sys
import yum
import os
from optparse import OptionParser
import logging
import platform
import subprocess
import re
import pty
import time
import docker
import pip
import json
from dockactions import dockit
from dockutils import run_helper
from dockutils import create_vol
from dockglobals import logger


dockit_log_file = "/var/log/dockit/dockit.log"
sysdict = {'dist': '', 'ver': '', 'name': ''}

fedora_req_pcks = centos_req_pcks = rhel_req_pcks = ["docker-io", "python-docker-py"]
rhel7_req_pcks = ["docker",  "python-docker-py"]
req_pcks = mis_pcks = avail_pcks = []
gluster_config= globalopts={}


def talktoDocker(pulloption, baseimage, imagetag, numcontainers, dockerfile, dockerrepo, buildoption, startoption, gluster_mode, gluster_install, gluster_volume):

    new_image_tag=''
    flag= flag1 = gluster_flag = 0
    cons_ids=[]
    logger.debug("Docker image name :%s \t Image Tag:%s \t number of Containers:%s", baseimage, imagetag, numcontainers)

    try:
        connret = dockit.DockerCli("connect", pulloption, baseimage, imagetag, numcontainers,
                                   dockerfile, dockit_log_file, dockerrepo, buildoption)
        if connret:
            logger.info("Successfully connected to docker deamon: \n"
                         "\t \t \t pull/build/start containers accordingly.")

        else:
            logger.error("Connection return failed..exiting.")

            sys.exit(1)

        if pulloption:
            logger.debug("Proceeding with actions on Image:%s", baseimage)
            #if dockerrepo == None:
            #    logger.debug("Base image pulling is not supported with this version of dockit \n"
            #                 " please provide dockerrepo")
            #    sys.exit(1)
            pullret = connret.pullC()
            if pullret:
                logger.info("Done with pulling.. continuing")
                if dockerrepo and baseimage:
                    new_image_tag=dockerrepo+'/'+baseimage+':'+'latest'
                    flag1=1
                logger.debug( "new_image_tag:%s", new_image_tag)
            else:
                logger.error("Error when pulling ")
                #sys.exit(1)
        else:
            logger.info("Not trying to pull image:%s.. continuing", baseimage)
        if buildoption:
            logger.debug("Continuing build process with %s", dockerfile)

            built_image =  connret.buildC()
            if built_image:
                logger.info(" Image built from docker file :%s with id:%s and tag:%s",
                             built_image, built_image['Id'],built_image['RepoTags'])
                if imagetag:
                    logger.debug("Image tag:%s", imagetag)
                    new_image_tag=imagetag+':latest'
                    flag=1
                logger.debug( "new_image_tag:%s", new_image_tag)

            else:
                logger.error("Failed when building from docker file:\nCheck docker file path and options ")

        else:
            logger.debug ("Not trying to build the image from docker file")

        if startoption:

            if flag or flag1:
                logger.debug("Flag:%s \t Flag1:%s image tag:\t %s" ,flag, flag1,new_image_tag)

            else:
                if baseimage and imagetag:
                    new_image_tag = baseimage+':'+imagetag
                logger.debug("Using image tag :%s" ,new_image_tag)

            ret_exist=  connret.image_by_tag(new_image_tag)

            if ret_exist:
                logger.debug("Image exists :%s with ID:%s  ", ret_exist, ret_exist['Id'])
                logger.info("Going to run the containers")

                if gluster_mode:
                    if gluster_volume:
                        gluster_flag = 1
                    else:
                        gluster_flag = 0
                runret =  connret.runC(ret_exist['RepoTags'][0], gluster_flag, gluster_config, )
                if runret:
                    if not connret.container_ips:
                        logger.critical( "Something went wrong when spawning containers:exiting")
                        sys.exit(1)


                    logger.info("Containers are running successfully.. please login and work!!!!")
                    print (60 * '-')
                    logger.info("Details about running containers..\n")
                    logger.info("Container IPs \t : %s\n ", connret.container_ips)

                    for c in connret.cons_ids:
                        c_id =  dict(connret.cons_ids[0])['Id']
                        cons_ids.append(c_id)
                    logger.info("Container Ids \t : %s \n ", cons_ids)
                    print (60 * '-')
                    #todo : Its possible to auto login to these containers via below , commenting it out for now
                    #loginC(connret.container_ips, connret.cons_ids)
               	    if gluster_mode:
                        gluster_cli = create_vol.glusteractions()
                        if gluster_cli:
                            logger.debug("Successfully created gluster client")
                            run_helper.rh_config_dict['SERVER_IP_ADDRS'] =connret.container_ips
                        else:
                            logger.error("Failed to create gluster client")
                        if gluster_install:
                            ginst =  gluster_config.get('GLUSTER_VERSION','3.5')
                            if ginst:
                                gluster_cli.gluster_install(ginst)
                            else:
                                logger.debug("Failed to get Gluster Version from dict.")
                        else:
                            logger.info("Gluster installation not required")
                        if gluster_volume:

                    	    run_helper.rh_config_dict['VOL_TYPE'] = gluster_config['VOL_TYPE']
                    	    run_helper.rh_config_dict['SERVER_EXPORT_DIR'] =gluster_config['SERVER_EXPORT_DIR']
                    	    run_helper.rh_config_dict['TRANS_TYPE'] ='tcp'
                    	    run_helper.rh_config_dict['VOLNAME'] =gluster_config['VOLNAME']
                    	    logger.debug("Successfully filled configuration details:%s", run_helper.rh_config_dict)
                            gluster_cli.create_gluster_volume(start=True)
                            logging.info('Gluster Volume operations done! Please mount volume :%s in your client', gluster_config['VOLNAME'])
                        else:
                            logger.debug("Gluster Volume creation not required")
                    else:
                        logger.info("Done!")
                else:
                    logger.error( "Failed when starting/inspecting containers")
            else:
                logger.error("Image + tag does not exist.. I cant start container from this..exiting")

                sys.exit(1)
        else:
            logger.debug( "Not trying to start containers..")
            logger.info( "Dockit finished...")
            return True




    except Exception as e:
        logger.critical("Failed on :%s", e)
        sys.exit(1)


def  loginC (cont_ips, cont_ids):
    for ips in cont_ips:
        print ips
    for ids in cont_ids:
        cmd = 'sudo docker inspect {}'.format(ids['Id'])
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        data = json.loads(output)
        port = data[0]['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']
        cmd = 'sshpass -p "redhat" ssh root@localhost -p {}  -o StrictHostKeyChecking=no'.format(port)
        subprocess.call(cmd, shell=True)

class Packageinst:
    """
		 Class to retrieve system specific information, then call
	"""

    def __init__(self, dryrun):
        self.skipflag = dryrun


    def getsysinfo(self):
        """
			  This function will fetch system/platform information
		"""
        try:
            dist, ver, name = platform.dist()
            sysdict['dist'] = dist
            sysdict['ver'] = ver
            sysdict['name'] = name

        except Exception as e:
            logger.debug(e)
            sys.exit(1)
        logger.info("Distribution:%s",sysdict['dist'])
        return True

    def checkprereq(self):
        """
			This function will check for pre-req packages
			which need to be installed and if its not available
			it will be installed
		"""
        try:
            if sysdict['dist'] == "fedora":
                req_pcks = list(fedora_req_pcks)
            elif sysdict['dist'] == "redhat":

                if sysdict['ver'] < '7':
                    req_pcks = list(rhel_req_pcks)
                else:
                    req_pcks = list(rhel7_req_pcks)
            elif sysdict['dist'] == "centos":
                req_pcks = list(centos_req_pcks)
            else:
                logger.error("Unknown Distribution for me")
                sys.exit(1)

            logger.info("Distribution:%s Required %s packages \n\t \t \t Making yum transactions", sysdict['dist'], req_pcks)
            yb = yum.YumBase()
            yb.conf.cache = os.geteuid() != 1
            for pck in req_pcks:
                if yb.rpmdb.searchNevra(name=pck):
                    logger.info("%s -> Installed" % (pck))
                    avail_pcks.append(pck)
                else:
                    logger.info("%s -> not installed" % (pck))
                    mis_pcks.append(pck)
                    if not self.skipflag:
                        try:
                            if pck == "python-docker-py":
                                logger.debug("Trying with pip")
                                cmd = "sudo pip install {0} -U >/dev/null".format("docker-py")
                                os.system(cmd)
                                mis_pcks.remove(pck)
                            else:
                                logger.info("Unknown package for me to install via pip.. Proceeding")
                        except Exception as e:
                            logger.error(e)
                            logger.error("Error occurred when trying to install %s  using pip -> Try to install manually" % (pck))
                            sys.exit(1)
                        try:
                            yb.install(name=pck)
                            time.sleep(5)
                        except yum.Errors.InstallError, err:
                            logger.error("exiting : Error when installing package %s", pck)
                            logger.error("%s", (str(err)))
                            sys.exit(1)
                        except Exception as e:
                            logger.critical(e)
                            logger.error("Error occurred when trying to install %s -> Try to install manually" % (pck))
                            sys.exit(1)
            if len(mis_pcks) > 0:
                if self.skipflag:
                    logger.info("Please install the %s packages and try again.", mis_pcks)

                    sys.exit(1)
                else:
                    try:
                        yb.resolveDeps()
                        yb.buildTransaction()
                        yb.processTransaction()
                        return True
                    except Exception as e:
                        logger.error(
                            "Yum transaction failure:%s .. Giving one more try", e)
                        for pkgs in mis_pcks:
                            os_cmd = "yum install -y %s >/dev/null" %(pkgs)
                            if os.system(os_cmd):
                                print "Failed again to install %s package" % (pkgs)
                                sys.exit(1)


        except Exception as e:
            logger.critical("Exiting..%s", e)

            sys.exit(1)
        return True


class Procstart:
    """
        This class is defined for running process/deamon inside the system
    """

    def __init__(self, *args, **kwargs):

        for k, w in kwargs.items():
            logger.debug("%s :%s" % (k, w))
            self.proc = w
            if w == "docker":
                if os.path.exists("/usr/bin/systemctl"):
                    self.cmd = 'systemctl start docker'
                else:
                    self.cmd = 'docker -d'
                    logger.debug(self.cmd)
            else:
                logger.error("Unknown process %s ..exiting" % (w))
                self.cmd = 'exit 1'


    def checkproc(self):

        self.proc='docker -d'
        try:
            s = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
            for prs in s.stdout:
                if re.search(self.proc, prs):
                    logger.info(
                        "Requested process: %s is running" % (self.proc))
                    return True
        except Exception as e:
            logger.debug(e)
            return False

    def execproc(self):
        logger.debug("Start docker")
        master, slave = pty.openpty()
        p = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE,
                             stdout=slave, stderr=slave, close_fds=True)
        stdout = os.fdopen(master)
        #logger.debug stdout.readline()
        time.sleep(10)
        logger.debug("Checking for successful start of the process")
        return self.checkproc()

    def infoproc(self):
        if self.proc == "docker":
            self.cmd = 'docker info'
        logger.debug(self.cmd)
        try:
            subprocess.call(self.cmd, shell=True)
            return True
        except Exception as e:
            logger.debug(e)
            sys.exit(1)


def print_menu():
    print (60 * '-')
    print ("   M A I N - M E N U - O F - DOCKIT")
    print (60 * '-')
    print ("Invoke dockit with any of (-d , -p, -b, -s) options \n")
    print ("1. Install and Run Docker deamon                     (-d)   -->  dryrun   ")
    print ("2. Pull image from docker repo and Run containers    (-p)   -->  requires -i <IMAGE> and -r <DOCKERREPO>")
    print ("3. Build from dockerfile and Run Containers          (-b)   -->  requires -f <DOCKER FILE> and -t <IMAGE TAG> ")
    print ("4. Run container from existing image                 (-s)   -->  requires -i <IMAGE> and -t <IMAGE TAG> -n <COUNT>")
    print ("\n Optional: \n Create and start gluster containers  (-g)   -->  Effective only with -s option ")
    print ("\n                                                   (--gi) -->  To install Gluster From Source ")
    print ("\n                                                   (--gv) -->  To auto configure Gluster Volume")

    print (60 * '-')


def read_config_file_b(conf_file):

    f = open(conf_file, 'r')
    for line in f.readlines():
        match = re.search(r'([\w]+)="([^"]+)"', line)
        if  match:
            key = match.group(1)
            value = match.group(2)
            if key == 'BRICKS':
                gluster_config['BRICKS'] = value
                f.close()
                return


def read_config_file(conf_file):

    f = open(conf_file, 'r')
    for line in f.readlines():
        match = re.search(r'([\w]+)="([^"]+)"', line)
        if  match:
            key = match.group(1)
            value = match.group(2)
            gluster_config[key]=value
    f.close()

    return gluster_config

def create_logger():
    # create logger with 'dockit'


    stdout_log = stderr_log = dockit_log_file
    if not os.path.isdir("/var/log/dockit"):
        os.mkdir('/var/log/dockit/')
    dockit_out = open(dockit_log_file, 'a+',0)


    #logging.basicConfig(level=logging.INFO)
   # logger = logging.getLogger('dockit')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(dockit_log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)

    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.ERROR)
    logger.addHandler(fh)
    logger.addHandler(ch)




def main(dryr=0, dockit_log=dockit_log_file):

    #print print_menu()
   # create_logger()

    parser = OptionParser()
    parser.add_option("-d", "--dry_run",
                      action="store_true", dest="dry", default=False,
                      help="Do dry run - dont try to install any packages")

    parser.add_option("-p", "--pullimage",
                      action="store_true", dest="pullimg", default=False,
                      help="Whether to pull from the docker repo ? Need to specify dockerrepo and image name ")


    parser.add_option("-s", "--startc",
                      action="store_true", dest="startc", default=False,
                      help="Whether to start from an image ? Need to specify image and tag ")

    parser.add_option("-b", "--buildimage",
                      action="store_true", dest="buildimg", default=False,
                      help="Whether to build image from the dockerfile? Need to specify dockerfile path, and imagetag")

    parser.add_option("-g", "--gluster_mode",
                      action="store_true", dest="glumode", default=False,
                      help="Configure gluster volume in containers")

    parser.add_option("-i", "--image",
                      dest="image", help="Image name  - Containers will be based on this image", metavar="IMAGE")

    parser.add_option("-t", "--imgtag",
                      dest="imgtag", help="Image tag name  - Containers will be assigned this tag", metavar="IMAGETAG")

    parser.add_option("-n", "--count",
                      dest="count", help="Number of containers to start  - ", metavar="COUNT")

    parser.add_option("-c", "--configfile",
                      dest="configfile", help="COnfig file path to read gluster configuration  - ", metavar="CONFIGFILE")

    parser.add_option("-f", "--dockerfile",
                      dest="dockerfile", help="Docker file path to build the container  - ", metavar="DOCKERFILE")

    parser.add_option("-r", "--dockerrepo",
                      dest="dockerrepo", help="Docker repository name with a trailing blackslash  - ", metavar="DOCKERREPO")

    parser.add_option("--gv", "--glustervolume",
                      action="store_true", dest = "gluvolume", default=False,help="Gluster Volume Creation  inside containers  - Valid with -g option ")
                     # dest="gluvolume", help="Gluster Volume Creation  inside containers  - Valid with -g option ", metavar="GLUSTERVOLUME")

    parser.add_option("--gi", "--glusterinstall",
                      dest="gluinst", help="Install gluster inside containers  - Valid with -g option ", metavar="GLUSTERVERSION")

    logger.info("Dockit starting.. Process logs are available at:%s", dockit_log_file)

    options, arguments = parser.parse_args()
    globalopts=dict(options.__dict__)

    pull_option_args = ['image','dockerrepo']
    #pull_option_args = ['image']
    build_option_args = ['dockerfile','imgtag']
    start_option_args = ['image', 'imgtag', 'count']
    gluster_optins_args = ['gluvolume','gluinst']

    anyopt = [ options.pullimg , options.buildimg , options.startc , options.dry]
    anyopt_dict = { 'pullimg':pull_option_args , 'buildimg':build_option_args , 'startc':start_option_args }

    check = [o for o in anyopt if o]
    if not check:
        logging.error( "You missed one of the must required option..  reread and execute.... exiting .")
        print_menu()
        sys.exit(1)
    if options.gluinst or options.gluvolume:
        if not options.glumode:
            logger.error("You can not use gluster actions without -g option")
            sys.exit(1)
    if options.glumode and not options.gluvolume and not options.gluinst:
        logger.warn("-g dont have any effect without --gv or --gi options")

    final_true_list = [[key,value] for key,value in globalopts.items() if value != False if value != None]
    logger.debug("Input \t :%s" ,final_true_list)
    final_list=[]
    for it in final_true_list:
        for k,v in anyopt_dict.items():
            if k == it[0]:
                final_list.append(v)
    #print final_list
    my_good = list(set([item for sublist in final_list for item in sublist]))

    if options.startc and options.buildimg:
        my_good.remove('image')
        logger.debug("Required Parameters for your request:%s", my_good)

    if options.pullimg and options.startc:
        if options.imgtag== None:
            options.imgtag='latest'
            logger.debug("image tag : %s , docker repo:%s", options.imgtag, options.dockerrepo)

    if options.pullimg and options.buildimg:
        logger.error( "Only one at a time, pull or build")
        sys.exit(1)

    for good in my_good:
        if not options.__dict__[good]:
                logger.error("\n \t Unfortunately  You Missed:%s", good)
                parser.print_help()
                sys.exit(1)


    if options.count:
        options.count=int(options.count)

    if options.startc:

        prefer =  raw_input ("Do you want to continue (y/n)")
        if prefer=='y':
            logger.info( "Proceeding ")
            if options.glumode:


                if options.gluinst:
                    logger.info( "Need to install gluster inside containers")
                    gluster_config['GLUSTER_VERSION'] = options.gluinst

                if options.gluvolume:
                    logger.info( "\n Need to configure gluster volume..\n")

                    g_voltype=''
                    if not options.configfile:
                        g_voltype = raw_input("Gluster Volume Type (ex: 2x2x1 where (distribute,replica, stripe count in order)\t :")
                        g_volname = raw_input("Gluster Volume Name (ex: glustervol)\t :")
                        g_export  = raw_input("Gluster Export Dir Name (ex: /rhs_bricks)\t :")
                        g_brick_file = raw_input("Gluster brick file (ex: /home/configfile)\t :")
                    else:
                        logger.info( "Reading gluster configuration from config file")
                        print read_config_file(options.configfile)

                    try:
                        if g_voltype:
                            volumeconfig = re.search(r'([0-9]+)x([0-9]+)x([0-9]+)', g_voltype)
                        else:
                            gluster_config['VOL_TYPE'] = gluster_config.get('VOL_TYPE', '1x2x1')
                            gluster_config['VOLNAME']=gluster_config.get('VOLNAME', 'defaultVol')
                            gluster_config['SERVER_EXPORT_DIR']=gluster_config.get('SERVER_EXPORT_DIR','/defaultExport')
                            volumeconfig = re.search(r'([0-9]+)x([0-9]+)x([0-9]+)',gluster_config['VOL_TYPE'])
                        distributecount = volumeconfig.group(1)
                        replicacount = volumeconfig.group(2)
                        stripevcount = volumeconfig.group(3)
                    except Exception as e:
                        logger.debug( "Error in parsing volume type string..exiting")
                        logger.debug(e)
                        sys.exit(1)

                    if distributecount == '0':
                        distributecount =  1
                    if replicacount == '0':
                        replicacount =  1
                    if stripevcount == '0':
                        stripevcount =   1

                    options.count = int(distributecount) * int(replicacount) * int(stripevcount)
                    logger.info( "No of gluster containers to spawn:%s" , options.count)
                    prefer = raw_input ("Do you want to continue (y/n):")
                    if prefer == 'y':
                        if not options.configfile:
                            gluster_config['VOLNAME']=g_volname
                            gluster_config['VOL_TYPE']=g_voltype
                            gluster_config['SERVER_EXPORT_DIR']=g_export
                            gluster_config['BRICK_FILE']=g_brick_file
                            #gluster_config['BRICKS'] = read_config_file_b(g_brick_file)
                            read_config_file_b(g_brick_file)
                        else:
                            logger.info( "Configuration read from configuration file")

                        logger.info("%s", gluster_config)
                    else:
                        logger.error( "Exiting.. Invoke dockit command with proper option of gluster mode")
                        sys.exit(1)
            else:
                logger.info( "Run containers natively, no mode configured")
            prefer=''
        else:
            logger.debug( "Exiting ")
            sys.exit(1)

    if options.dry:
        logger.info("Dry run : Dockit will not attempt to install any package")
        dryr= 1
    else:
        logger.debug("Install packages if required, this is not a dry run...")

    try:
        sysobj = Packageinst(dryr)
        if sysobj:
            sysobj.getsysinfo()
            ret = sysobj.checkprereq()

            if ret:
                logger.info("Pre-requisites are installed")
            else:
                logger.debug("Either install it or let me install ")
                sys.exit(1)
            logger.debug("Going to check/start docker daemon")
            procd = Procstart(process="docker")
            checkret = procd.checkproc()
            if not checkret:
                ret = procd.execproc()
                if ret:
                    logger.info("Successfully started docker deamon... ")
                else:
                    logger.error('Exiting')
                    sys.exit(1)
            procd.infoproc()
            logger.debug("Connecting to the docker deamon")

            talktoDocker(options.pullimg, options.image, options.imgtag, options.count, options.dockerfile,
                         options.dockerrepo , options.buildimg, options.startc, options.glumode, options.gluinst, options.gluvolume)

    except Exception as e:
        logger.debug(e)
        sys.exit(1)


if __name__ == "__main__":
#   Program to install and start a process/daemon

    main()


