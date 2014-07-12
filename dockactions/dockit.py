#!/usr/bin/python -tt


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
import os
import logging
import platform
import subprocess
import re
import pty
import docker
import dockinstall
from dockglobals import logger
import time




DOCK_SOCK = "unix://var/run/docker.sock"
DOCK_VERSION = "1.8"


#rh_config_dict={}

failed_con=[]
inspect_failed_con=[]

class DockerCli (docker.Client):
    """
        This class list the methods which can be used to connect to the deamon
        """

    def __init__(self, action, pulloptionval, imageval, imagetagval , numc, dockerfile, docklog, dockerrepo, buildoptionval ):

        super(DockerCli, self).__init__(version=DOCK_VERSION)

        self.dock_action = action
        self.dock_image = imageval
        self.dock_tag=imagetagval
        self.dock_pull=pulloptionval
        self.dock_build=buildoptionval
        self.dock_numc = numc
        self.dock_command=''
        self.dock_filepath= dockerfile
        self.repository=dockerrepo
        self.dc = ""
        self.gflag=0
        self.docklogfile=docklog
        self.container_ips=[]
        self.cons_ids = []

        if self.dock_action == "connect":
            self.dc = self.connectD()

    def connectD(self):
        try:
            # note: "version" can play a role in functionality
            self.dc = docker.Client(base_url=DOCK_SOCK,
                                    version=DOCK_VERSION,
                                    timeout=30)
            #self.dc = docker.Client(base_url='unix://var/run/docker.sock',
            #   version='1.10',
            #   timeout=10)

            if self.dc:

                dcinfo = self.dc.info()
                logger.debug("Docker information \n %s", dcinfo)
            else:

                logger.critical("Failed to get docker info:")

        except Exception as e:
            logger.debug(e)
            sys.exit(1)


        return self.dc

    def pullC(self):
        """
         This pull input image
        """
        logger.debug(self.dock_pull)
        if self.dock_pull:
            logger.debug("Trying to pull %s from docker repo:%s ... \n "
                         "This can take some time, please wait...", self.dock_image, self.repository)
            if self.repository:
                self.dock_image=self.repository+'/'+self.dock_image
            logger.debug("Repo+image:%s", self.dock_image)
            try:
                ret = self.dc.pull(self.dock_image)
                #if '404' in ret:
                #    print "Failed when pulling image from docker repo"
                #    logger.debug("Failed when pulling image from docker repo")
                #    return False
                #else:
                logger.info("Successfully pulled docker image:%s" % (self.dock_image))
                return True
            except Exception as e:
                logger.critical("Failed to pull %s with an exception: %s", self.dock_image, e)
                return False

        else:
            logger.debug("Dont attempt to pull given image from docker repo")
            return True

    def image_by_id (self, id):
        """
        Return image with given Id
        """

        if not id:
            return None
        return next((image for image in self.dc.images() if image['Id'] == id), None)

    def image_by_tag(self, tag):
        """
        Return image with given tag
        """

        if not tag:
            return None
        return next((image for image in self.dc.images() if tag in image['RepoTags']), None)

    def runC(self , image_tag, gl_flag, gluster_dict={}, ):
        """
        Run the container
        Creates a container that can then be `start`ed.
        Parameters are similar to those for the `docker run` command
        except it doesn't support the attach options (`-a`). See "Port bindings" and "Using volumes"  for
        more information on how to create port bindings and volume mappings.
        """

        #self.command="exec >/dev/tty 2>/dev/tty </dev/tty && /usr/bin/screen -s /bin/bash"

        self.c_tag = image_tag
        self.container_id = ""
        self.info_array = ["Hostname", "NetworkSettings"]
        #todo: For now, dont enable dock_command .
        #self.dock_command=''
        self.brick_ext = 0
        self.gflag=gl_flag
        self.brick_set=[]
        logger.debug(" Create and start containers with image :%s ", self.c_tag)

        if self.gflag:
            bricks =  gluster_dict['BRICKS']
            self.brick_set = []
            for b in bricks.split(','):
                self.brick_set.append(b)

            logger.info("Bricks will be using in order:%s", self.brick_set)

        logging.info( "Enable Gluster :%s" ,self.gflag)
        try:
            #docker run -i -t ubuntu /bin/bash

            for num in range(0,self.dock_numc):
                #todo: If we just want to enable auto dir creation inside same directory


                # self_note : when tty=False, the containers were just exited
                # as soon as it is created or executed the provided command
                # when its  True ,containers are  up and running , u can attach.
                # also stdin_open to True, for docker attach comand
                # ctrl+P+Q can detach the container
                # detach=False means it wont exit the shell ?
                if self.gflag:
                    self.brick_mount=gluster_dict['SERVER_EXPORT_DIR']
                    if len(self.brick_set ) < self.dock_numc:

                        logger.critical("Number of bricks given to me is less than number of nodes,  check configfile")
                        return False
                    else:
                        print "..."

                    self.dock_command =''
                    self.container_id = self.dc.create_container(
                                                    self.c_tag, command=self.dock_command, hostname=None, user=None,
                                                    detach=True, stdin_open=True, tty=True, mem_limit=0,
                                                    ports=[22, 80], environment=None, dns=None, volumes=[self.brick_mount],
                                                    volumes_from=None, network_disabled=False, name=None,
                                                    entrypoint=None, cpu_shares=None, working_dir=None)

                else:
                    #self.dock_command ='/bin/bash'
                    self.container_id = self.dc.create_container(
                                                    self.c_tag, command=self.dock_command, hostname=None, user=None,
                                                    detach=True, stdin_open=True, tty=True, mem_limit=0,
                                                    ports=[22, 80], environment=None, dns=None, volumes=None,
                                                    volumes_from=None, network_disabled=False, name=None,
                                                    entrypoint=None, cpu_shares=None, working_dir=None)

                self.cons_ids.append(self.container_id)
            logger.debug("Container Ids : %s" ,self.cons_ids)
            if not self.cons_ids:
                logger.critical( "Failed when creating Containers")
                return False

            for ids in self.cons_ids:
                try:
                    if self.gflag:
                        #self.brick_ext += 1
                        #self.brick_mount = '/rhs_bricks/brick'+str(self.brick_ext)
                        self.brick_source = self.brick_set[self.brick_ext]
                        self.brick_ext += 1
                    # TODO : look at other options
                    #mostly need to link these containers using link option
                    #http://blog.docker.io/2013/10/docker-0-6-5-links-container-naming-advanced-port-redirects-host-integration/
                    #regarding lxc_conf you can give me in dict formats
                    #also it helps when changing to static ips .etc
                    #-n flag looks similar:
                    #https://github.com/dotcloud/docker-py/issues/79

                        ret = self.dc.start(
                                            ids, binds={self.brick_source:self.brick_mount}, port_bindings={22: None, 80: None},
                                            lxc_conf=None,publish_all_ports=False, links=None, privileged=True)
                    else:

                        ret = self.dc.start(ids, binds=None, port_bindings={22: None, 80: None}, lxc_conf=None,
                                            publish_all_ports=False, links=None, privileged=True)
                    logger.debug("Container with ID :%s is started", ids)
                    time.sleep(10)

		  	   # TODO: may be I need to commit these containers later with a different workflow.
                except Exception as e:
                    logger.critical("Exception raised when starting Container with id:%s", ids)

                    logger.debug(e)
                    return False


            #TODO: This may not be the right place to put list containers
            #and capturing the requested information
            #logger.debug "Going to list the containers"
            #cons =  self.dc.containers(quiet=False, all=False, trunc=True, latest=False, since=None,
            #                   before=None, limit=-1)
            #for c in cons:
            #   self.c_id =  dict(cons[0])['Id']
            #   self.cons_ids.append( self.c_id)

            logger.info("  Information about running containers ")

            for ids in self.cons_ids:
                try:
                    insp_obj = self.dc.inspect_container(ids)
                    #logger.debug(insp_obj['Config']['Hostname'])
                    #logger.debug(insp_obj['NetworkSettings']['IPAddress'])
                    hostname =insp_obj['Config']['Hostname']
                    ipaddr = insp_obj['NetworkSettings']['IPAddress']
                    if not ipaddr :
                        logger.critical("Not able to get IP address of %s", hostname)

                    self.container_ips.append(insp_obj['NetworkSettings']['IPAddress'])
                except Exception as e:
                    logger.critical('Exception raised when inspecting Containers')
                    logger.debug(e)

                    return False

        except Exception as e:

            logger.critical('Exception raised when creating/starting Containers')
            logger.debug(e)
            return False

        return True


    def buildC(self):
        """
                        #Eqvnt to `docker build` command. Either `path` or `fileobj` needs
                        #to be set. `path` can be a local path (to a directory containing a
                        #Dockerfile) or a remote URL. `fileobj` must be a readable file-like
                        #object to a Dockerfile.

                        # Best option would be to create a docker file according to the input
                        # provided from the command line:
                        # That said, suppose if we specify fedora 2*2 it should spawn
                        # 4 containers with gluster packages installed

                        # An easy way of doing this is ship repos with glusterd running
                        # for different distros. so that that image can be mentioned in
                        # in the docker file.
        """
        #todo: Add support for github url

        self.waitsecs = 15
        logger.debug("Timeout for build process has been set to :%s seconds", self.waitsecs)
        try:
            logger.debug("Working on docker file :%s", self.dock_filepath)
            if self.dock_filepath:
                logger.info("Build it with dockerfile:%s \t and Tag: %s and self.dc: %s .."
                             "need to wait .." , self.dock_filepath, self.dock_tag, self.dc)
                #ret = self.dc.build( path=self.dock_filepath, tag=self.dock_tag, quiet=False, fileobj=None, nocache=False,
                #                   rm=False, stream=False)
                ret = self.dc.build(path=self.dock_filepath, tag=self.dock_tag)

                if ret:
                    while(self.waitsecs >= 0):
                        time.sleep(60)
                        logger.debug("Fetching docker images and tags for %s", self.dock_tag)

                        # More optimization can be as shown below.. how-ever disabling it for now:
                        #if next((image for image in self.dc.images() if self.dock_tag in image['RepoTags']), None):
                        #    logger.debug("Image found with tag")
                        #    return True
                        #else:
                        #    logger.debug("Failed to find requested tagged image in first attempt")
                        #    self.waitsecs =- 180

                        self.images = self.dc.images(name=None, quiet=False, all=False, viz=False)
                        for im in self.images:
                            for tag in im['RepoTags']:
                                if self.dock_tag in str(tag):
                                    logger.debug("dock_tag:%s  successfully built and available in repo", self.dock_tag)
                                    #return True
                                    return im

                        self.waitsecs = self.waitsecs - 1
                    logger.debug("Just before returning")
                    return False

                else:
                    logger.critical("Failed to build docker image")
            else:
                logger.critical("I am sorry, I cant build without dockerfile")
                return False



        except Exception as e:
            logger.debug("Failed build: ...")
            logger.debug(e)
            return False





