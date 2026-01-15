#!/usr/bin/env python3


import subprocess


# Отправка конфига
def config_send(hv_ip, vm_id, vm_name, new_vm_id, hv_username):
    new_vm_id = is_new_wm_id(vm_id, new_vm_id)
    status = subprocess.run(["scp", "{}@{}:/etc/pve/qemu-server/{}.conf".format(hv_username, hv_ip, vm_id), "/etc/pve/qemu-server/{}.conf".format(new_vm_id)], stdout=subprocess.PIPE)
    if status.returncode != 0:
        print("Config vm {} {} not send".format(new_vm_id, vm_name))
    print("Config vm {} {} sended".format(new_vm_id, vm_name))


def is_new_wm_id(vm_id, new_vm_id):
    if new_vm_id == False:
        return vm_id
    else:
        return new_vm_id