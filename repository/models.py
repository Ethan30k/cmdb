from django.db import models

# Create your models here.


class UserProfile(models.Model):
    """用户信息"""
    name = models.CharField(max_length=32, verbose_name="姓名")
    email = models.EmailField(verbose_name="邮箱")
    password = models.CharField(max_length=64, verbose_name="密码")
    phone = models.CharField(max_length=32, verbose_name="电话")
    role = models.ManyToManyField("Role")
    status_choice = (
        (0, "正常"),
        (1, "禁用")
    )
    status = models.SmallIntegerField(choices=status_choice)

    class Meta:
        verbose_name_plural = "用户信息表"

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32, verbose_name="角色名")
    menus = models.ManyToManyField("Menu")
    permission = models.ManyToManyField("Permission")

    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.name


class Menu(models.Model):
    """动态菜单"""
    name = models.CharField(unique=True, max_length=32, verbose_name="菜单名")
    url_type = models.SmallIntegerField(choices=((0, 'relative_name'), (1, 'absolute_url')), verbose_name="菜单类型")
    url_name = models.CharField(unique=True, max_length=128)

    class Meta:
        verbose_name_plural = "动态菜单"

    def __str__(self):
        return self.name


class Permission(models.Model):
    """权限表"""
    name = models.CharField(unique=True, max_length=32, verbose_name="权限名")
    url = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.name


class BusinessUnit(models.Model):
    """
    业务线
    """
    name = models.CharField('业务线', max_length=64, unique=True)
    contact = models.ForeignKey('Role', verbose_name='业务联系人', related_name='c')

    class Meta:
        verbose_name_plural = "业务线表"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )
    device_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )

    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)

    cabinet_num = models.CharField('机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField('机位号', max_length=30, null=True, blank=True)
    floor = models.IntegerField('楼层', default=1, null=True, blank=True)

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True)

    latest_date = models.DateField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产表"

    def __str__(self):
        return "%s-%s-%s" % (self.idc.name, self.cabinet_num, self.cabinet_order)


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField('机房', max_length=32)
    addr = models.CharField('地址', max_length=64)
    watch_tel = models.CharField('值班电话', max_length=11)
    manager = models.CharField('值班经理', max_length=32)
    manager_tel = models.CharField('经理电话', max_length=11)

    class Meta:
        verbose_name_plural = "机房表"

    def __str__(self):
        return self.name


class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField('Asset')

    hostname = models.CharField(max_length=128, unique=True)
    sn = models.CharField('SN号', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)

    ilo_ip = models.GenericIPAddressField('管理IP', null=True, blank=True)

    os_platform = models.CharField('系统', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    latest_date = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "服务器表"

    def __str__(self):
        return self.hostname


class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField('插槽位', max_length=8)
    model = models.CharField('磁盘型号', max_length=32)
    capacity = models.FloatField('磁盘容量GB')
    pd_type = models.CharField('磁盘类型', max_length=32)
    server_obj = models.ForeignKey('Server', related_name='disk')

    class Meta:
        verbose_name_plural = "硬盘表"

    def __str__(self):
        return self.slot


class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField('网卡名称', max_length=128)
    hwaddr = models.CharField('网卡mac地址', max_length=64)
    netmask = models.CharField(max_length=64)
    ipaddrs = models.CharField('ip地址', max_length=256)
    up = models.BooleanField(default=False)
    server_obj = models.ForeignKey('Server', related_name='nic')

    class Meta:
        verbose_name_plural = "网卡表"

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField('插槽位', max_length=32)
    manufacturer = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64)
    capacity = models.FloatField('容量', null=True, blank=True)
    sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField('速度', max_length=16, null=True, blank=True)

    server_obj = models.ForeignKey('Server', related_name='memory')

    class Meta:
        verbose_name_plural = "内存表"

    def __str__(self):
        return self.slot


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    management_ip = models.CharField('管理IP', max_length=64, blank=True, null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    manufacture = models.CharField(verbose_name='制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.CharField('设置详细配置', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "网络设备"

    def __str__(self):
        return "%s-%s" % (self.model, self.sn)


class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset_obj = models.ForeignKey('Asset', related_name='ar')
    content = models.TextField(null=True)
    creator = models.ForeignKey('UserProfile', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产记录表"

    def __str__(self):
        return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)


class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True)
    title = models.CharField(max_length=16)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志表"

    def __str__(self):
        return self.title
