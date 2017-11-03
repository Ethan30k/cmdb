from django.db import models

# Create your models here.


class UserProfile(models.Model):
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
    name = models.CharField(max_length=32, verbose_name="角色名")
    menus = models.ManyToManyField("Menu")

    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.name

