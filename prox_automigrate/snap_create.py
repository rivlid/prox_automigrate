#!/usr/bin/env python3


from datetime import datetime
import subprocess


def snap_create(hv_ip, dataset_list, hv_username):
    c_dt = datetime.now()
    f_dt = '-{}-{}-{}-{}-{}-{}'.format(c_dt.year, c_dt.month, c_dt.day, c_dt.hour, c_dt.minute, c_dt.second)
    snap_done = []
    for i in dataset_list:
        snap_name = '{}@am{}'.format(i, f_dt)
        result = subprocess.run(["ssh", "{}@{}".format(hv_username, hv_ip),  "zfs snapshot {}".format(snap_name)])
        if result.returncode != 0:
            for n in snap_done:
                snap_name = '{}@am{}'.format(n, f_dt)
                subprocess.run(["ssh", "{}@{}".format(hv_username, hv_ip),  "zfs destroy {}".format(snap_name)])
            print("snapshot {} ERROR".format(snap_name))
            break
        snap_done.append(i)
        print("snapshot {} CREATED".format(snap_name))
    return f_dt