
# Utilities for smartcam application

from dbus import Interface, SystemBus
from subprocess import check_output

################################################################################

def get_git_branch():
    cmd_out = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    return(cmd_out.decode('utf-8').rstrip())

def __systemd_create_interface():
    try:
        systemd = SystemBus().get_object('org.freedesktop.systemd1',
                                         '/org/freedesktop/systemd1')
        return(Interface(systemd, 'org.freedesktop.systemd1.Manager'))
    except Exception as e:
        print(e)
    return

def systemd_unit_running(unit_name):
    interface = __systemd_create_interface()

    try:
        obj_path = interface.LoadUnit(unit_name)
        obj_proxy = SystemBus().get_object('org.freedesktop.systemd1', obj_path)

        properties = Interface(obj_proxy, 'org.freedesktop.DBus.Properties')
        res = properties.GetAll('org.freedesktop.systemd1.Unit')['ActiveState']
    except Exception as e:
        print(e)
        return(None)

    if 'active' == res:
        return(True)
    return(False)

def systemd_unit_start(unit_name):
    interface = __systemd_create_interface()

    try:
        interface.StartUnit(unit_name)
        return(True)
    except Exception as e:
        print(e)
    return(False)
