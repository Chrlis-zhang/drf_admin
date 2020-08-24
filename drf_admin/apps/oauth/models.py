from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=20, default='', verbose_name='真实姓名')
    mobile = models.CharField(max_length=11, default="", verbose_name='手机号码')
    image = models.ImageField(upload_to='media/%Y/%m', default='default.png', blank=True, verbose_name='头像')
    roles = models.ManyToManyField('system.Roles', blank=True, verbose_name='角色')
    department = models.ForeignKey('system.Departments', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='部门')

    class Meta:
        db_table = 'admin_oauth_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    def _get_user_permissions(self):
        # 获取用户权限
        permissions = []
        for roles in self.roles.values('name'):
            if 'admin' == roles.get('name'):
                permissions.append('admin')
        for item in self.roles.values('permissions__sign').distinct():
            sign = item.get('permissions__sign')
            if sign:
                permissions.append(sign)
        return permissions

    def get_user_info(self):
        # 获取用户信息
        user_info = {
            'username': self.username,
            'avatar': '/media/' + str(self.image),
            'email': self.email,
            'is_active': self.is_active,
            'permissions': self._get_user_permissions()
        }
        return user_info
