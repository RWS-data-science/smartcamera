#!/usr/bin/env python3

# This module is managed by systemd as a root process and should provide
# a relatively safe way to execute system commands as long as the repo
# isn't compromised. Please see custom_cmds on the repo for more
# information on syntax and usage.

import subprocess as sp
import sys
import time

import requests

import utils

###

GIT_BRANCH = utils.get_git_branch()

CMD_BASE_URL = 'https://raw.githubusercontent.com/RWS-data-science/smartcamera'
CUSTOM_CMDS = "%s/%s/custom_cmds" % (CMD_BASE_URL, GIT_BRANCH)

ZZZ_TIME = {'devrelease' : 600,
            'release'    : 3600}.get(GIT_BRANCH, 30)

###

while True:
    res = requests.get(CUSTOM_CMDS, timeout=60)
    if res.status_code != 200:
        # possible connection issue
        # systemd will handle respawn
        sys.exit(0)

    for line in res.text.split('\n'):
        if not line.startswith('#'):
            # skip accidently committed empty lines
            if not "@" in line: continue

            elems = line.split(' @ ')
            cmd_epoch, commands = int(elems[0]), elems[1:]

            cur_epoch = int(time.time())
            epoch_diff = abs(cur_epoch - cmd_epoch)

            if (cmd_epoch > cur_epoch) and (epoch_diff < ZZZ_TIME):
                # run cmds sequentially:
                for cmd in commands:
                    print("executing: %s" % cmd)
                    p = sp.Popen(cmd.split(' '))
                    p.communicate()

    time.sleep(ZZZ_TIME)
