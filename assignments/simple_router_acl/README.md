## P4 Assignment

**NOTE:** Before you start this assignment, make sure you update your repo with `git pull` and then do `vagrant halt` and `vagrant up` followed by `vagrant provision`, this is required to install NetASM with all its dependencies.

In this assignment, you will learn how to write a P4 program for programmable data planes. Using P4 you will be able to 
create new headers, write parser specifications and add custom match+action tables to describe how the data plane device 
should process packets.

### Overview

This introductory video walks you through the simple router that the assignment uses as a base for the acl, it's highly recommended to watch this video before attempting the assignment:

* [P4 Simple Router - Tutorial Video] (http://p4.org/wp-content/uploads/2015/04/p4-demo-video-full.mp4)

For more information about the P4 language read the following material:
* [ An Introduction to P4](http://p4.org/wp-content/uploads/2015/03/p4-tutorial-12201423.pdf)
* [P4: Programming Protocol-Independent Packet Processors](http://www.sigcomm.org/sites/default/files/ccr/papers/2014/July/0000000-0000004.pdf)

### Simple Router with Access Control

In this exercise, you will be extending the simple router P4 program -- provided in the base P4 repository -- with an access control list.
In order to do this, you have to update the following aspects of the simple router program:
* Add support for reading and parsing tcp fields
* Add a new match+action table for access control
* Update the control flow to perform access control using tcp's source and destination ports

The following figures show the final parser and table flow graph for the simple router with acl. **The boxes in RED show what needs to be added.**

* [Parse Graph](https://github.com/mshahbaz/Coursera-SDN/blob/master/assignments/simple_router_acl/graphs/simple_router_acl.parser.png)
* [Table Flow Graph](https://github.com/mshahbaz/Coursera-SDN/blob/master/assignments/simple_router_acl/graphs/simple_router_acl.tables.png)

#### 1. Copy and build the assignment

* Copy the `simple_router_acl` directory to the `p4facorty/targets` folder

``` bash
$ cd ~/p4factory/targets
$ cp -rf /vagrant/assignments/simple_router_acl/ .
```

* Run `make` to test if the `simple_router_acl` builds properly. Note: that there is no acl support in the code at this time. You will be adding this support as part of this assignment.

``` bash
$ cd ~/p4factory/targets/simple_router_acl
$ make
```

#### 2. Update the source files to add support for access control

You need to modify the following three files:
* `p4src/includes/headers.p4`: add new header type for tcp
* `p4src/includes/parser.p4`: add a new parser function for tcp
* `p4src/simple_router_acl.p4`: add a new table for acl and update the control flow

#### 3. Test the assignment

* Run `make` to build the assignment.

``` bash
$ cd ~/p4factory/targets/simple_router_acl
$ make
```

* Setup the virtual ethernet pairs.

``` bash
$ sudo ~/p4factory/tools/veth_setup.sh
```

* Run the `behavioral-model`.

``` bash
$ sudo ./behavioral-model
```

* In another terminal, run the test script.

``` bash
$ cd ~/p4factory/targets/simple_router_acl
$ sudo python run_tests.py --test-dir=of-tests/tests/
```

* Upon successful completion, you should see the following output.

``` bash
...
VXLAN enabled
ERSPAN enabled
Geneve enabled
eth.py: device id is  0
echo.EchoTest ... ok
acl.AclTest ... ok

----------------------------------------------------------------------
Ran 2 tests in 1.843s

OK
```

#### 4. Submit your code

To submit your code. Run the `behavioral-model` again. However, this time instead of running the `run_test.py` script, run the `submit.py` script provided under the project directory in another terminal.

``` bash
$ cd ~/p4factory/targets/simple_router_acl
$ sudo python submit.py
```

The submission script will ask for your login and password. This password is not the general account password, but an assignment-specific password that is uniquely generated for each student. You can get this from the assignments listing page.

Once finished, it will prompt the results on the terminal (either passed or failed).
