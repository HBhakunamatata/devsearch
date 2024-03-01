from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User

# 信号量定义
    
# @receiver(post_save, sender=Profile)
def profile_updated(sender, instance, created, **kwargs):
    """用户信息存储信号action"""
    print('User profile saved!')
    print("Instance" , instance)
    print('created:  ' , created)


def profile_deleted(sender, instance, **kwargs):
    """用户信息删除action"""
    print('User profile deleted!')
    print('Instance: ', instance)


def on_user_created(sender, instance, created, **kwargs):
    """只当新User被创建时，自动添加Profile"""
    print('user created signal received!')
    if created:
        Profile.objects.create(
            user = instance,
            username = instance.username,
            email = instance.email,
        )
    


def on_profile_deleted(sender, instance, **kwargs):
    """当Profile被删除时自动删除关联的User"""
    try:
        user = instance.user
        user.delete()
    except:
        # 当删除user时，会触犯cascade删除profile，但此时profile的user已经被删除了，会报错
        pass


def updateUser(sender, instance, created, **kwargs):
    """当Profile被修改时更新User信息"""
    profile = instance
    if profile.user:
        user = profile.user
        if created == False:
            user.first_name = profile.name
            user.username = profile.username
            user.email = profile.email
            user.save()

# 信号量关联
# post_save.connect(profile_updated, sender=Profile)
# post_delete.connect(profile_deleted, sender=Profile)
post_save.connect(on_user_created, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(on_profile_deleted, sender=Profile)