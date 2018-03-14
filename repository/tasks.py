#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import sys

sys.path.append("..")
from utils.ansible_api import ANSRunner
from repository import models


@shared_task
def add(x, y):
    # time.sleep(3)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def server_info():
    resource = [
        # {"hostname": "192.168.189.133"},
        {"hostname": "192.168.84.115"},
        {"hostname": "192.168.84.146", "port": "2188"},
    ]
    # host_list = []
    host_list = ["192.168.84.115", "192.168.84.146"]
    # iplist = models.NIC.objects.values_list("ipaddrs")
    # for ip in iplist:
    #     host = ip[0]
    #     port = models.Server.objects.filter(nic__ipaddrs=host).first().port
    #     resource.append({"hostname": host, "port": port})
    #     host_list.append(host)

    ANS = ANSRunner(resource)
    ANS.run_model(host_list=host_list, module_name='setup', module_args="")
    print(ANS.get_model_result())
    data = ANS.handle_cmdb_data(ANS.get_model_result())
    # print(data)
    if data:
        for cmdb_data in data:
            status = cmdb_data.get('status')
            if status == 0:
                host = cmdb_data['ip']
                system = cmdb_data['system']
                system_version = cmdb_data['system_version']
                serial = cmdb_data['serial']
                cpu = cmdb_data['cpu']
                cpu_number = cmdb_data['cpu_number']
                vcpu_number = cmdb_data['vcpu_number']
                manufacturer = cmdb_data['manufacturer']
                network = cmdb_data['network']
                disk = cmdb_data['disk_info']
                hostname = cmdb_data['hostname']
                model = cmdb_data['model']
                server_obj = models.Server.objects.filter(nic__ipaddrs=host)
                server_obj_id = models.Server.objects.filter(nic__ipaddrs=host).first().id
                server_obj.update(hostname=hostname,
                                  sn=serial,
                                  manufacturer=manufacturer,
                                  model=model,
                                  os_platform=system,
                                  os_version=system_version,
                                  cpu_count=vcpu_number,
                                  cpu_physical_count=cpu_number,
                                  cpu_model=cpu)
                for k, v in network.items():
                    if 'ip' in v:
                        name = v['name']
                        ip = v['ip']
                        netmask = v['netmask']
                        mac = v['mac']
                        status = v['status']
                        nic = models.NIC.objects.filter(ipaddrs=ip)
                        if nic:
                            nic.update(name=name,
                                       hwaddr=mac,
                                       netmask=netmask,
                                       up=status)
                        else:
                            models.NIC.objects.create(name=name,
                                                      hwaddr=mac,
                                                      netmask=netmask,
                                                      up=status,
                                                      server_obj=server_obj.first(),
                                                      ipaddrs=ip)

                    else:
                        name = v['name']
                        mac = v['mac']
                        status = v['status']
                        nic = models.NIC.objects.filter(name=name).filter(server_obj_id=server_obj_id)
                        # models.NIC.objects.filter(name=name).filter(server_obj_id=server_obj_id).update(hwaddr=mac, up=status)
                        if nic.first():
                            nic.update(hwaddr=mac, up=status, )
                        else:
                            models.NIC.objects.create(name=name,
                                                      hwaddr=mac,
                                                      netmask=netmask,
                                                      up=status,
                                                      server_obj=server_obj.first(), )

                if disk:
                    for k, v in disk.items():
                        slot = k
                        model = v['disk_model']
                        pd_type = v['disk_type']
                        disk_size = v['disk_size']
                        j = models.Disk.objects.filter(server_obj_id=server_obj_id)
                        # j.filter(slot=slot).update(model=model, capacity=disk_size, pd_type=pd_type)

                        if j.filter(slot=slot).first():
                            j.filter(slot=slot).update(model=model,
                                                       capacity=disk_size,
                                                       pd_type=pd_type)
                        else:
                            models.Disk.objects.create(
                                    slot=slot,
                                    model=model,
                                    capacity=disk_size,
                                    pd_type=pd_type,
                                    server_obj=server_obj.first()
                            )
