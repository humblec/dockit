#!/usr/bin/python

# Copyright (C) 2014 Red Hat Inc.
# Authors: # M S Vishwanath Bhat < msvbhat@gmail.com >
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
import re
import paramiko

import getopt
import threading
from dockglobals import logger
import logging


rh_config_dict = {}
con_pass = ''


def read_config_file():
    global rh_config_dict
    rh_config_dict = {}
    f = open('configfile', 'r')
    for line in f.readlines():
        match = re.search(r'([\w]+)="([^"]+)"', line)
        if match:
            key = match.group(1)
            value = match.group(2)
            rh_config_dict[key] = value
    f.close()
    return None


def usage():
    logger.debug(
        'Usage: run_helper.py {[-c "file to be copied:path in '
        'destination machine"] [-r "command to be run"]}')
    return 0

# get the ip address of the nodes from the config file


def get_nodes_ip():
    logger.debug("Received below configuration from caller")
    logger.debug('%s', rh_config_dict)

    try:
        servers = rh_config_dict['SERVER_IP_ADDRS']
    except:
        logger.critical(
            'Unable to retrive the server ip address from configfile. '
            'Please set SERVERS_IP_ADDRS in configfile')
        sys.exit(1)

    server_set = set([])

    for server in servers:

        server_set.add(server)

    return list(server_set)


# get the client ip


def get_client_ip():
    try:
        clients = rh_config_dict['CLIENT_IP_ADDRS']
    except:
        logger.critical('Unable to find client IP address.')
        sys.exit(1)

    clients_set = set([])
    for client in clients.split(','):
        clients_set.add(client)

    return list(clients_set)


# get the prefix path to install gluster


def get_prefix_path():
    try:
        prefix_path = rh_config_dict['PREFIX_PATH']
    except:
        prefix_path = ''

    return prefix_path


def get_server_export_dir():
    try:
        export_dir = rh_config_dict['SERVER_EXPORT_DIR']
    except:
        export_dir = None

    if export_dir[-1] == '/':
        export_dir = export_dir[:-1]
    invalid_export_dir = [
        '/', '//', '/root', '/root/', '/usr',
        '/usr/', '/etc', '/etc/', '/sbin',
        '/sbin/', '/boot', '/boot/', '/opt',
        '/opt/', '/var', '/var/', '/bin', '/bin/']
    if export_dir in invalid_export_dir:
        logger.critical(
            '%s can NOT be the server export directory. '
            'Please give other valid directory', export_dir)
        sys.exit(1)

    return export_dir


def get_volume_type():
    try:
        vol_type = rh_config_dict['VOL_TYPE']
    except:
        vol_type = None
    return vol_type


def get_vol_name():
    try:
        volname = rh_config_dict['VOLNAME']
    except:
        volname = None

    return volname


def get_trans_type():
    try:
        trans_type = rh_config_dict['TRANS_TYPE']
    except:
        trans_type = None

    supported_trans_types = ['tcp', 'rdma', 'tcp,rdma']
    if trans_type not in supported_trans_types:
        logger.critical(
            "%s is not a supported transport type. "
            "Please set the proper supported transport type",
            trans_type)
        sys.exit(1)

    return trans_type


def get_mountpoint():
    try:
        mountpoint = rh_config_dict['MOUNTPOINT']
    except:
        logger.critical(
            'Unable to find the mount point. '
            'Please set the MOUNTPOINT in configfile')
        sys.exit(1)

    invalid_mountpoints = [
        '/', '//', '/root', '/root/', '/usr',
        '/usr/', '/etc', '/etc/', '/sbin', '/sbin/',
        '/boot', '/boot/', '/opt', '/opt/', '/var',
        '/var/', '/bin', '/bin/']
    if mountpoint in invalid_mountpoints:
        logger.critical(
            "%s  + ' is not a valid mountpoint."
            "Please provide a valid mountpoint. "
            "Aborting...", mountpoint)
        sys.exit(1)

    if mountpoint[-1] == '/':
        mountpoint = mountpoint[:-1]

    return mountpoint


def get_mount_type():
    try:
        mount_type = rh_config_dict['MOUNT_TYPE']
    except:
        logger.critical(
            'unable to find the valid mount type. '
            'Please set MOUNT_TYPE in configfile')
        sys.exit(1)

    return mount_type


# run commands in the remote machine


def run_command(node, cmd, verbose):
        # pmk = logging.getLogger("paramiko")
        # pmk.setLevel(logging.WARNING)
        # logger.addHandler(pmk)

    logging.getLogger("paramiko").setLevel(logging.WARNING)
    ssh_handle = paramiko.SSHClient()
    ssh_handle.load_system_host_keys()
    ssh_handle.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # TODO: may need to look at user name as well
    ssh_handle.connect(node, username='root', password=con_pass)

    chan = ssh_handle.get_transport().open_session()

    try:
        chan.exec_command(cmd)
    except:
        logger.critical(
            "unable to execute the command %s on the "
            "remote server %s ", cmd, node)

    fout = chan.makefile('rb')
    ferr = chan.makefile_stderr('rb')
    ret_code = chan.recv_exit_status()
    if verbose is True:
        logger.debug(
            "node: %s -> cmd: %s ->  exit status: %d ", node, cmd, ret_code)
        # print cmd
        print '\n' + fout.read() + ferr.read()
        # logger.debug("%s ",fout.read())
        # logger.error("%s ",ferr.read())

    ssh_handle.close()

    return ret_code

"""
NOTE: I'm not sure how much of above code is robust.
Because if the remote machine sends back enough data to fill
the buffer of 'channel file object' then, host (this machine)
may hang forever.
Need a better way to handle this issue. Current code just
assumes that the remote machine doesn't send lot of data.
"""

# Do scp to node machine using scp command


def rcopy(node, srcfile, destpath, verbose):
    if verbose is True:
        print '>>>>>>>>>>>>>>>>>>> doing remote copy to host ' + \
            node + ' <<<<<<<<<<<<<<<<<<<<<<'
    scpcmd = 'scp ' + srcfile + ' ' + 'root@' + node + ':' + destpath
    if verbose is True:
        print scpcmd
    try:
        if verbose is True:
            os.system(scpcmd)
        else:
            os.system(scpcmd + '> /dev/null 2>&1')
    except:
        print scpcmd + ' failed'

    if verbose is True:
        print '\n\n'

    return None


def main():
    opt = arg = []
    try:
        opt, arg = getopt.getopt(sys.argv[1:], "c:r:C:R:p:", ["copy=",
                                 "run=", "Run=", "Copy=", "parallel="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    threaded_run = False
    scpsend = remoterun = in_all_machines = None
    for k, v in opt:
        if k in ("-c", "--copy"):
            scpsend = True
            filepath = v.split(':')
        elif k in ("-C", "--Copy"):
            scpsend = True
            filepath = v.split(':')
            in_all_machines = True
        elif k in ("-r", "--run"):
            remoterun = True
            cmd = v
        elif k in ("-R", "--Run"):
            remoterun = True
            cmd = v
            in_all_machines = True
        elif k in ("-p", "--parallel"):
            threaded_run = True
            cmd = v
        else:
            assert False, "unhandled option"

    if scpsend is True:
        sfile = filepath[0]
        destpath = filepath[1]

    nodes = get_nodes_ip()

    if in_all_machines is True:
        client_ips = get_client_ip()
        for client_ip in client_ips:
            if client_ip not in nodes:
                nodes.append(client_ip)

    if remoterun is True:
        for node in nodes:
            run_command(node, cmd, True)

    if threaded_run is True:
        threads = []
        for node in nodes:
            t = threading.Thread(target=run_command, args=(node, cmd, True))
            t.start()
            threads.append(t)

    if scpsend is True:
        for node in nodes:
            rcopy(node, sfile, destpath, True)

    if not scpsend and not remoterun and not threaded_run:
        logger.error('Option unhandled. Please execute with proper option')
        usage()
        sys.exit(1)

    return 0


# read_config_file()
if __name__ == '__main__':
    main()
