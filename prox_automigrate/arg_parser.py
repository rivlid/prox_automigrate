#!/usr/bin/env python3


import argparse


# Принимаем аргументы коммандной строки ip адрес гипервизора
# и id виртуальной машины.
def cli():
    description_cli = "Proxmox zfs migration tools. Use on destination hypervisor. \
    Required arguments source hypervisor and virtual machine id."
    options = argparse.ArgumentParser(description=description_cli)
    options.add_argument('hv_ip', help="ip address of source hypervisor")
    options.add_argument('vm_id', help="virtual machine ID")
    options.add_argument('-u', '--user', default='root',
                        help='source server credential username default="root"')
    options.add_argument('-d', '--dest', default=False,
                        help='ZFS dataset destanation, example:"zfs-hdd/local/proxmox"')
    options.add_argument('-i', '--idvm', default=False,
                        help='New id for VM')
    options.add_argument('-f', '--force', action='store_true',
                        help='Ignore VM status')
    options.add_argument('-b', '--debug', action='store_true')
    return options.parse_args()