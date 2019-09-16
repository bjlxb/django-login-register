import time
import uuid

from django.db import models

# Create your models here.


class UserInfo(models.Model):
    LOGIN_TYPE_CHOICES = (
        ('password', '密码'),
        ('facebook', '脸书'),
        ('google', '谷歌'),
        ('QQ', 'QQ'),
        ('wechat', '微信'),
        ('phone_sms', '手机验证码'),
        ('email', '邮箱')
    )
    login_type = models.CharField(verbose_name='登录方式', choices=LOGIN_TYPE_CHOICES, max_length=50)
    first_login_time = models.DateTimeField(verbose_name='首次登录', auto_now_add=True)
    last_login_time = models.DateTimeField(verbose_name='最后登录', auto_now=True)
    auth_token = models.UUIDField(verbose_name='token', default=uuid.uuid1())
    login_status_expire_time = models.FloatField(verbose_name='失效时间', default=-1)
    is_activated = models.BooleanField(verbose_name='是否验证', default=False)
    is_locked = models.BooleanField(verbose_name='是否锁定', default=False)
    nick_name = models.CharField(verbose_name='昵称', max_length=200, null=True, blank=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='uploads/user/avatar/',
                               default="uploads/user/avatar/avatar.png")
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    phone_number = models.CharField(verbose_name='手机号', max_length=20, null=True, blank=True)
    location = models.CharField(verbose_name='位置', max_length=20, null=True, blank=True)
    about_me = models.CharField(verbose_name='关于我', max_length=20, null=True, blank=True)
    active_device_idfa = models.CharField(verbose_name='idfa', max_length=100, null=True, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.id, self.email)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def to_json(self):
        return {
            'id': self.id,
            'login_type': self.login_type,
            'nickname': self.nick_name if self.nick_name else '',
            'avatar': self.avatar.url if self.avatar else '',
            'email': self.email if self.email else '',
            'location': self.location if self.location else '',
            'about_me': self.about_me if self.about_me else '',
            'phone': self.phone_number if self.phone_number else ''
        }


class UserLoginHistory(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    time_login = models.DateTimeField(verbose_name="登录时间", auto_now_add=True)
    login_result = models.CharField(max_length=50, null=True, blank=True, verbose_name="登录结果")
    ip_address = models.CharField(max_length=100, null=True, blank=True, verbose_name="ip")
    is_success = models.BooleanField(default=False, verbose_name='是否成功')

    class Meta:
        verbose_name = "登录历史"
        verbose_name_plural = "登录历史"

    def __str__(self):
        return '{}-{}'.format(self.id, self.ip_address)


class CodeHistory(models.Model):
    email_or_phone = models.CharField(max_length=50, verbose_name='邮箱或手机号')
    code = models.CharField(max_length=50, verbose_name='验证码')
    captcha_for_img = models.CharField(max_length=50, verbose_name='图形验证码')
    user_id = models.IntegerField(verbose_name='用户ID', null=True, blank=True)
    ip_address = models.CharField(max_length=100, verbose_name='IP地址')
    # from_idfa = models.CharField(max_length=100, verbose_name='IDFA')
    kind = models.CharField(verbose_name='说明', max_length=500, null=True, blank=True)
    start_datetime = models.FloatField(verbose_name='验证码开始时间', default=time.time())
    exist_time = models.IntegerField(verbose_name='有效时长', default=5)
    expire_datetime = models.FloatField(verbose_name='验证码失效时间')
    is_verified = models.BooleanField(default=False, verbose_name='是否验证')
    verified_datetime = models.FloatField(verbose_name='验证码验证时间', null=True, blank=True)

    message_code = models.CharField(verbose_name='短信参照码', max_length=500, null=True, blank=True)
    message_charge = models.CharField(verbose_name='验证码扣费情况', max_length=500, null=True, blank=True)
    message_msg = models.CharField(verbose_name='验证码状态信息', max_length=500, null=True, blank=True)
    message_remain = models.CharField(verbose_name='短信剩余次数', max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "验证码历史"
        verbose_name_plural = "验证码历史"

    def __str__(self):
        return '{}-{}'.format(self.id, self.email_or_phone)

    def to_json(self):
        return {
            'id': self.id,
            'email_or_phone': self.email_or_phone,
            'code': self.code if self.code else '',
            'captcha_for_img': self.captcha_for_img if self.captcha_for_img else '',
            'user_id': self.user_id if self.user_id else '',
            'ip_address': self.ip_address if self.ip_address else '',
            'kind': self.kind if self.kind else '',
            'is_verified': self.is_verified if self.is_verified else ''
        }
