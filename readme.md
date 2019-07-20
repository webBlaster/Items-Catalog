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

# Item Catalog Project
The Item Catalog project is a requirement to finish Udacity's Full Stack Nanodegree program. The task is to develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit, delete their items. I chose to make a dessert catalog and use Google as my sole authentication system.

## Prepare The Software And Data
My operating system is Mac so the below information will reflect that. My preferred code editor is Atom. I will assume Python and Git has been downloaded and installed already.
 
### Install Virtual Box
VirtualBox is software that runs virtual machines. Download it from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads). Install the platform package for Mac. No need to download the extension pack or the SDK.

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from [vagrantup.com](https://www.vagrantup.com/downloads.html). Install the version for Windows.

### Download the repo
1. Clone the repo: https://github.com/kcalata/Item-Catalog.git into the directory of your choosing.
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

### Load the data
In your terminal, run the following:
```
python desserts.py
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
 
 ### Play around in the Dessert Catalog
 Play around in the [Dessert Catalog](http://localhost:8000/catalog).
 You may check out the desserts that I have set as the defaults. You can even add, edit, or delete your own dessert items after logging in through Google.
 
 ### Turn off web server
 Press CTRL+C to turn off the web server. This will stop the Dessert Catalog.
 
 ### Exit Vagrant
 Run the following command to exit vagrant,
 ```
 exit
 ```
