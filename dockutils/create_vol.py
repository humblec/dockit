#!/usr/bin/python

# Copyright (C) 2014 Red Hat Inc.
# Author      :M S Vishwanath Bhat < msvbhat@gmail.com >
# Contributors:Humble Chirammal <humble.devassy@gmail.com> | <hchiramm@redhat.com>
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

import os, sys
import re
from . import run_helper
import time
import logging
from dockglobals import logger

class glusteractions():
    def __init__(self):
        logger = logging.getLogger('dockit')
        #logger.info(" Module : createvol")




    def pre_create_cleanup(self,nodes, export_dir):
        for node in nodes:
            cmd = 'pgrep gluster | xargs kill -9'
            run_helper.run_command(node, cmd, False)

            cmd = 'mkdir -p ' + export_dir
            run_helper.run_command(node, cmd, False)

            cmd = 'rm -rf ' + export_dir + '/*'
            run_helper.run_command(node, cmd, False)

            cmd = 'rm -rf /etc/glusterd'
            run_helper.run_command(node, cmd, False)

            cmd = 'rm -rf /usr/local/var/log/glusterfs/*'
            run_helper.run_command(node, cmd, False)

            cmd = 'rm -f /usr/local/var/log/glusterfs/.c*'
            run_helper.run_command(node, cmd, False)


            cmd = 'rm -rf /var/log/glusterfs/*'
            run_helper.run_command(node, cmd, False)

            cmd = 'rm -f /var/log/glusterfs/.c*'
            run_helper.run_command(node, cmd, False)

        return 0

    def gluster_install(self, version):
        failed_package_nodes=[]
        failed_install_nodes=[]


        nodes = run_helper.get_nodes_ip()
        logger.info("Trying to install gluster on %s nodes ", nodes)


        gluster_package_command = 'yum -y install python-devel python-setuptools gcc deltarpm yum-utils git \
                   autoconf automake bison dos2unix flex glib2-devel \
                   libaio-devel libattr-devel libibverbs-devel \
                   librdmacm-devel libtool libxml2-devel make openssl-devel \
                   pkgconfig python-devel python-eventlet python-netifaces \
                   python-paste-deploy python-simplejson python-sphinx \
                   python-webob pyxattr readline-devel rpm-build gdb dbench \
                   net-tools systemtap-sdt-devel attr psmisc findutils which \
                   xfsprogs yajl-devel lvm2-devel e2fsprogs mock nfs-utils \
                   openssh-server supervisor openssl fuse-libs wget >/dev/null'
        #gluster_package_command='ls'
        #gluster_install_command = 'cd /root/glusterfs && make install'
        gluster_install_command = "rm -rf /root/glusterfs && cd /root && git clone git://review.gluster.org/glusterfs && cd glusterfs && \
                                 git checkout -b %s origin/release-%s  && ./autogen.sh >/dev/null && ./configure>/dev/null && make >/dev/null && make install> /dev/null " %(version, version)


        for node in nodes:
            flag = flag1 = status1 = status2 = 0
            logger.info("Configuring/installing on node:%s", node)
            status1 = run_helper.run_command(node, gluster_package_command, True)
            #time.sleep(20)

            if status1:
                logger.error('Required Gluster package installation failed on node: %s' , node)
                failed_package_nodes.append(node)
                flag = 1
            else:
                logger.info("Continuing ..")
                status2 = run_helper.run_command(node, gluster_install_command, True)
                time.sleep(20)
                if status2:
                    logger.error("Failed to configure GlusterFs from source repository ")
                    failed_install_nodes.append(node)
                    flag1 = 1

                else:
                    logger.info("Successfully configured GlusterFS binary on node:%s", node)

        if status1 or status2:
            logger.critical("Failed to install gluster packages on:%s or GlusterFs binary installation failed on :%s ", failed_package_nodes, failed_install_nodes)
        else:
            logger.info("Successful Gluster Package Installation and GlusterFS Binary installation on all the nodes!")
       # if status1 == 0 and status2 == 0:
       #         logger.info("Everything went fine")
        return



    def create_gluster_volume(self,start=True):

        nodes = run_helper.get_nodes_ip()
        logger.info( "nodes are %s" , nodes)

        masternode = nodes[0]
        export_dir = run_helper.get_server_export_dir()
        if export_dir == None:
            export_dir = '/rhs_bricks'
        vol_type = run_helper.get_volume_type()
        if vol_type != None:
            volconfig = re.search(r'([0-9]+)x([0-9]+)x([0-9]+)', vol_type)
            distcount = volconfig.group(1)
            repcount = volconfig.group(2)
            stripecount = volconfig.group(3)
        else:
            distcount = '2'
            repcount = '2'
            stripecount = '1'

        trans_type = run_helper.get_trans_type()
        if trans_type == '':
            trans_type = 'tcp'

        volname = run_helper.get_vol_name()
        if volname == '':
            volname = 'hosdu'

        number_nodes = len(nodes)
        logger.info( "Number of nodes: %s" ,number_nodes)
        if distcount == '0':
            distcount =  1
        if repcount == '0':
            repcount =  1
        if stripecount == '0':
            stripecount =  1

        number_bricks = int(distcount) * int(repcount) * int(stripecount)

        logger.info( "number of bricks:%s" , number_bricks)

        if number_bricks > number_nodes:
            logger.critical("number of bricks and number of servers don't match.\n")
            logger.critical("The support to have more than 1 brick per container is not there yet \n")
            return 1

        if repcount == '1':
            replica_count = ''
        else:
            replica_count = "replica %s" % repcount

        if stripecount == '1':
            stripe_count = ''
        else:
            stripe_count = "stripe %s" % stripecount
        #pre_create_cleanup(nodes, export_dir)

        brick_list = []
        node_index = 0
        for i in range(0, number_bricks):
            brick = "%s:%s/%s_brick%d" % (nodes[node_index], export_dir, volname, i)
            brick_list.append(brick)
            node_index = node_index + 1
            if node_index > number_nodes:
                node_index = 0

        vol_create_cmd = "gluster --mode=script volume create %s %s %s transport %s %s force" % (volname, replica_count, stripe_count, trans_type, ' '.join(brick_list))

        flag = 0
        for node in nodes:
            status = run_helper.run_command(node, 'pgrep glusterd || glusterd', True)
            if status:
                logger.error('glusterd can not be started in node: %s' , node)
                flag = 1

        if flag:
            logger.info('glusterd can not be started successfully in all nodes. Exiting...')
            sys.exit(1)

        flag = 0
        for node in nodes:
            if node != masternode:
                status = run_helper.run_command(masternode, 'gluster peer probe ' + node, False)
                time.sleep(20)
                if status:
                    logger.error('peer probe went wrong in %s' , node)
                    flag = 1

        if flag:
            logger.critical('Peer probe went wrong in some machines. Exiting...')
            sys.exit(1)

        status = run_helper.run_command(masternode, vol_create_cmd, True)
        if status:
            logger.critical('volume creation failed.')

        if status == 0 and start == True:
            status = run_helper.run_command(masternode, "gluster --mode=script volume start %s" % volname, False)

        return status




    def start_gluster_volume(self,masternode, volname):
        vol_start_cmd = 'gluster volume start ' + volname
        status = run_helper.run_command(masternode, vol_start_cmd, True)
        return status

