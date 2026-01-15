#!/usr/bin/env python3


import re
#from prox_automigrate.config_send import is_new_wm_id

def config_edit(vm_id, new_vm_id):
    if new_vm_id != False:
        with open ("/etc/pve/qemu-server/{}.conf".format(new_vm_id), "r") as f:
            data = f.read()
        new_data = data.replace("vm-{}-disk-".format(vm_id), "vm-{}-disk-".format(new_vm_id))
        with open ("/etc/pve/qemu-server/{}.conf".format(new_vm_id), "w") as f:
            print(new_data)
            f.write(new_data)

def is_new_wm_id(vm_id, new_vm_id):
    if new_vm_id == False:
        return vm_id
    else:
        return new_vm_id

def config_edit_dataset(dest, zpool_list, vm_id, new_vm_id):
    with open ("/etc/pve/storage.cfg", "r") as f:
        data = f.read()
    # Разделяем вывод по двум символам переноса строки
    stor_arr = data.split('\n\n')
    dataset_list = {}
    for i in stor_arr:
    # Ищем имя зфс датасета и его путь
        name = re.search(r"(?<=(zfspool: )).*", i)
        path = re.search(r"(?<=(pool )).*", i)
    # Если совпадений не найдено пропускаем итерацию
        if name == None or path == None:
            continue
    # Если совпадение найдено создаем запись в словаре
        else:
            dataset_list[path.group(0)] = name.group(0)
    if dataset_list.get(dest, False) == False:
        print("Хранилища {} не существует на данном сервере. Конфигурация VM не изменена.".format(dest))
        return 1
    vm_id_conf = is_new_wm_id(vm_id, new_vm_id)
    with open ("/etc/pve/qemu-server/{}.conf".format(vm_id_conf), "r") as f:
        data = f.read()
    for i in zpool_list.keys():
        data = data.replace(i, dataset_list[dest])
    with open ("/etc/pve/qemu-server/{}.conf".format(vm_id_conf), "w") as f:
        print(data)
        f.write(data)      