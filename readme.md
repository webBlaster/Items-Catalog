# LOGS ANALYSIS

## ABOUT
a Udacity project where you answer three questions with sql on a large database
the questions include:
1, what are the top three most popular post of all time
2, who are the top three authors that got the most views
3, on which day did more than one percent of request led to errors

## SETUP
to run this program you need a virtual machine(VM) that runs a SQL databse server and 
the web app that uses it
the tools which will be used to install and manage the VM will be Vagrant and VirtualBox
### INSTALLING VIRTUALBOX
VirtualBox is the software that runs the virtual machine. You can get it [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
Install the platform package for your operating system. You do not need the extension pack or the SDK.
You do not need to launch VirtualBox after installing it: Vagrant will do that.

### INSTALLING VAGRANT
Vagrant is the software that configures the VM and lets you share files between your host computer and
the VM's filesystem. You can get it [here](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

### DOWNLOADING VM CONGIGURATION
You can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm
## VIEWS
this project contains two views err and req
which are used in question three

### VIEW SETUP
first view:

create view err as select cast(time as date) as date,count(*) from log where status !='200 OK' group by date order by count(*) desc;

second view:

create view req as select cast(time as date) as date,count(*) as num from log
group by date order by num desc;
