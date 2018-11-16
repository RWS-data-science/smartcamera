# smartcamera

This repository contains the software required to transform a Linux system equipped with the necessary sensory hardware into a smartcam device. Since the devices are not expected to be remotely accessible, we rely heavily on regularly polling this repository for new instructions and/or updates to ensure continued stable & secure functioning. 

#### Development model

1. Changes land in the **master** branch to be evaluated
2. Reviewed changes are merged into the **devrelease** branch and tested using the smartcam device in the lab
3. Provided the devrelease passes all tests, the new changes are merged with the **release** branch where they are automatically picked up by the existing smartcam devices in production

#### Initial device configuration

Here follow the required steps to go from a default Stretch (Debian 9 / Raspbian) installation to a functional smartcamera device:

##### 1. Preinstall script

This script is not included within this repository and configures the following:

* Creates the user that runs the smartcam processes
* Imports pre-made ssh key for user above
* Adds user above to video/dialout groups
* Installs file containing REST target url

##### 2. Postinstall script

Please use the '--branch' flag to force a software channel for your target device. 

`wget -O - https://raw.githubusercontent.com/RWS-data-science/smartcamera/master/postinstall | bash `

* Installs a minimal firewall using netfilter/iptables
* Runs all available package updates using apt
* Configures unique hostname to identity the camera
* Installs required tools & dependencies for smartcam
* Configures ramdisk mount point for application scratch space
* Configures smartcam systemd service
* Installs smartcam software

#### Device updates & maintenance

Devices are configured to regularly poll this repository for updates on the branch they were configured with. The main process will take appropriate actions depending on the type of update:

- Main : runs integrity checks on update & restarts updated main process
- Worker : terminates existing worker, re-imports worker module and restarts worker
- Model : restarts worker

Additionally, a smartcam_cmds process is installed to allow executing custom commands at defined epochs. This process runs with unrestricted access to enable OS level package updates. New commands are scheduled by making entries into the 'custom_cmds' file found in this repository. Please see 'custom_cmds' for more information on syntax and usage. 

#### Future improvements

* Remove worker dependency on main process
* Set up python env for easier dependency mgmt
* Intrusion detection 
