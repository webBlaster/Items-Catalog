# ITEMS CATALOG

## ABOUT
a web app that displays items in different categories

## SETUP
to run this program you need a virtual machine(VM)
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

### Download the repo
1. Clone the repo: https://github.com/webBlaster/Items-Catalog into the directory of your choosing.
2. In your terminal, move into the directory containing the files of my project.

### Start the virtual machine
1. From your terminal, run the command:
```
vagrant up
```
2. When the above is finished running, run the command:
```
vagrant ssh
```
3. If your shell prompt starts with the word "vagrant", you're logged into your Linux VM.

```
This will create a database of starter dessert items and categories.

 ### Run app.py
 Run the following command:
 ```
 python app.py
 ```
 or, if the above doesn't work
 ```
 python3 app.py
 ```
 
 ### Turn off web server
 Press CTRL+C to turn off the web server. This will stop the Dessert Catalog.
 
 ### Exit Vagrant
 Run the following command to exit vagrant,
 ```
 exit
 ```
