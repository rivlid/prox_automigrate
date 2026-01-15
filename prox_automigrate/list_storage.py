#!/usr/bin/env python3


import paramiko
import re
import yaml


# Получение дисков для миграции
def list_storage(hv_ip, vm_id, hv_username, debug):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hv_ip, username=hv_username)
# Запрашиваем список хранилищь
    stdin, stdout, stderr = client.exec_command('cat /etc/pve/storage.cfg')
    out = bytes.decode(stdout.read(), encoding='utf-8')
    err = bytes.decode(stderr.read(), encoding='utf-8')
    if err != "":
        print(err)
        client.close()
        return 0
# Разделяем вывод по двум символам переноса строки
    stor_arr = re.split(r'\n\n', out)
    zpool_list = {}
    for i in stor_arr:
# Ищем имя зфс датасета и его путь
        name = re.search(r"(?<=(zfspool: )).*", i)
        path = re.search(r"(?<=(pool )).*", i)
# Если совпадений не найдено пропускаем итерацию
        if name == None or path == None:
             continue
# Если совпадение найдено создаем запись в словаре
        else:
            zpool_list[name.group(0)] = path.group(0)
# Запрашиваем список дисков виртуальной машины
    stdin, stdout, stderr = client.exec_command('cat /etc/pve/qemu-server/{}.conf'.format(vm_id))
    out = bytes.decode(stdout.read(), encoding='utf-8')
    err = bytes.decode(stderr.read(), encoding='utf-8')
    if err != "":
        print(err)
        client.close()
        return 0
    dataset_list = []
    out = yaml.load(out, Loader=yaml.FullLoader)
    for key in out:
# Если ключь соответствует scsi,sata,virtio,ide
        if bool(re.match(r'(scsi|sata|virtio|ide)\d+' , key)):
# Тогда для каждого наденного на гипервизоре зфс датасета
            for i in zpool_list:
# Ищем совпадение с дисками на виртуальной машине
                if bool(re.match(r'{}:'.format(i) , out[key])):
                    dataset = re.search(r'^[^,]*' ,out[key]).group(0)
# Если совпадение найдено добавляем в массив полный путь к диску
                    dataset_list.append(re.sub(r'{}:'.format(i) , "{}/".format(zpool_list[i]) , dataset))
    if debug == True:
        for i in dataset_list:
            print(i)
        for key, value in zpool_list.items():
            print("{}: {}".format(key, value))
        
    return dataset_list, zpool_list