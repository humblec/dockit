### DOCKIT installation 

## Possibility 1:

When running 'python setup.py install'

```
Processing pycrypto-2.6.1.tar.gz
Writing /tmp/easy_install-DvHDFa/pycrypto-2.6.1/setup.cfg
Running pycrypto-2.6.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-DvHDFa/pycrypto-2.6.1/egg-dist-tmp-UBuB9z
configure: error: in `/tmp/easy_install-DvHDFa/pycrypto-2.6.1':
configure: error: no acceptable C compiler found in $PATH
See `config.log' for more details
Traceback (most recent call last):


  File "/usr/lib64/python2.7/distutils/cmd.py", line 326, in run_command
    self.distribution.run_command(command)
  File "/usr/lib64/python2.7/distutils/dist.py", line 972, in run_command
    cmd_obj.run()
  File "setup.py", line 278, in run

```

Install 'gcc' in your system



## Possibility 2:

When running 'python setup.py install'

```
Downloading https://pypi.python.org/packages/source/p/pycrypto/pycrypto-2.6.1.tar.gz#md5=55a61a054aa66812daf5161a0d5d7eda
Processing pycrypto-2.6.1.tar.gz
Writing /tmp/easy_install-7x9dbh/pycrypto-2.6.1/setup.cfg
Running pycrypto-2.6.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-7x9dbh/pycrypto-2.6.1/egg-dist-tmp-JxZ1Mw
warning: GMP or MPIR library not found; Not building Crypto.PublicKey._fastmath.
src/MD2.c:31:20: fatal error: Python.h: No such file or directory
 #include "Python.h"
                    ^
compilation terminated.
error: Setup script exited with error: command 'gcc' failed with exit status 1


error: Setup script exited with error: command 'gcc' failed with exit status 1
```

Install python2-devel in your system



## Possibility 1: 

When dockit try to install docker packages, you may see :

```
dockit : ERROR Yum transaction failure:[u'Errors were encountered while downloading packages.', u'docker-io-1.0.0-6.fc20.x86_64: Caching enabled but no local cache of /var/cache/yum/x86_64/20/updates/packages/docker-io-1.0.0-6.fc20.x86_64.rpm from updates/20/x86_64', u'python-websocket-client-0.14.1-1.fc20.noarch: Caching enabled but no local cache of /var/cache/yum/x86_64/20/updates/packages/python-websocket-client-0.14.1-1.fc20.noarch.rpm from updates/20/x86_64', u'python-docker-py-0.2.3-8.fc20.x86_64: Caching enabled but no local cache of /var/cache/yum/x86_64/20/updates/packages/python-docker-py-0.2.3-8.fc20.x86_64.rpm from updates/20/x86_64'] .. Giving one more try

```

There are 2 attempts by dockit to install docker packages. The transaction errors may pop up when trying with the first method, even if you see above messages, please put your attention on end of the message "Giving one more try.." ,  mostly this second attempt will be a success. Once there is a message saying "Pre-requisites are installed", it is covered and package installation went through.


## Possibility 2:

```
"Error when pulling image..." 
```
If you got above error, yes , there was an error when pulling. I would suggest to execute same command again and find the result.

## Possibility 3:

```
dockit : ERROR Image + tag does not exist.. I cant start container from this..exiting
```

This comes when there is no image exist in your local/remote docker repo on given name:

For ex: if you have specified '-i humble/fed20-gluster ' in your command, you have to make sure the image exist, in the same name in your image repo.

You can check existing images of your docker repo by :

```
docker images 
```
## Possibility 4:

```
dockit      : CRITICAL Failed on :'BRICKS'
```

I am sure you dont have proper entry of 'BRICKS' in your config file.

An ex: would be :
```
BRICKS="/brick9,/brick10,/brick11,/brick12"
```


