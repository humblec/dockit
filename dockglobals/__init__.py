#!/usr/bin/python
import logging
import os

dockit_log_file="/var/log/dockit/dockit.log"


def create_logger():

    if not os.path.isdir("/var/log/dockit"):
        os.mkdir('/var/log/dockit/')
    dockit_out = open(dockit_log_file, 'a+',0)

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=dockit_log_file,
                    filemode='w')


    ch = logging.StreamHandler()

    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger('').addHandler(ch)
    #logger.addHandler(ch)
    #logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('dockit')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(dockit_log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    # create console handler with a higher log level
    return logger

logger= create_logger()
