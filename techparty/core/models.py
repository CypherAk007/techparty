#encoding=utf-8
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from imagekit.models import ImageModel

class UserProfile(models.Model):
    user = models.ForeignKey(User,verbose_name=u'用户')
    description = models.TextField(u'简介')
    is_lecturer = models.BooleanField(u'讲师')
    avatar = models.URLField(u'头像',null=True,blank=True) # 第三方帐号的头像链接
    custom_avatar = models.ImageField(u'自定义头像',upload_to='avatars',null=True,blank=True) # 自定义头像,上传时将该头像转换几种size。
    tags = TagField(u'标签')

    def avatar_normal(self):
        if not self.custom_avatar:
            return self.avatar
        else:
            pass # 返回相应size的头像

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u'用户资料'
        verbose_name_plural = u'用户资料'

class UserLink(models.Model):
    """
    用户连接
    """
    user = models.ForeignKey(User,verbose_name=u'用户')
    link = models.URLField(u'链接')
    title = models.CharField(u'标题',max_length=50)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'用户链接'
        verbose_name_plural = u'用户链接'

class Event(models.Model):
    """
    一次沙龙的活动。
    """
    name = models.CharField(u'名称',max_length=50)
    alias = models.SlugField(u'标识',max_length=50)
    intro = models.TextField(u'内容')
    hash_tag = models.CharField(u'微博标签',max_length=20,blank=True,null=True) # 用于微博、Twitter
    start_time = models.DateTimeField(u'开始时间')
    end_time = models.DateTimeField(u'结束时间')
    creator = models.ForeignKey(User,verbose_name=u'发起人')
    create_time = models.DateTimeField(u'发起时间',auto_now_add=True)
    tags = TagField(u'tag')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'活动'
        verbose_name_plural = u'活动'

class Enroll(models.Model):
    """
    某一次活动的报名纪录
    """
    event = models.ForeignKey(Event,verbose_name=u'活动')
    user = models.ForeignKey(User,verbose_name=u'成员')
    time = models.DateTimeField(u'报名时间',auto_now_add=True)
    comment = models.CharField(u'报名理由',max_length=140) #yeah,140 chars,a tweet's length
    is_permited = models.BooleanField(u'允许') # 被通过的报名才能收到邀请邮件

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u'报名'
        verbose_name_plural = u'报名'


class Topic(models.Model):
    """
    某次活动的一个主题
    """
    event = models.ForeignKey(Event,verbose_name=u'活动')
    title = models.CharField(u'标题',max_length=50)
    sub_title = models.CharField(u'副标题',max_length=50,null=True,blank=True)
    description = models.TextField(u'简介')
    author = models.ForeignKey(User,verbose_name=u'讲师')
    add_time = models.DateTimeField(u'加入时间',auto_now_add=True)
    tags = TagField(u'标签')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'主题'
        verbose_name_plural = u'主题'

class Photo(ImageModel):
    event = models.ForeignKey(Event,verbose_name=u'活动')
    name = models.CharField(u'名称',max_length=50)
    description = models.CharField(u'描述',max_length=140,blank=True,null=True)
    original_image = models.ImageField(u'原图',upload_to='photos/%Y/%m/%d')
    num_views = models.PositiveIntegerField(u'查看次数',editable=False,default=0)
    add_time = models.DateTimeField(u'上传时间',auto_now_add=True)
    add_by = models.ForeignKey(User,verbose_name=u'上传者')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'相片'
        verbose_name_plural = u'相片'

    class IKOptions:
        spec_module = 'core.specs'
        cache_dir = 'cache'
        image_field = 'original_image'
        save_count_as = 'num_views'

class Vote(models.Model):
    """
    某位成员为某个主题所投的票
    """
    topic = models.ForeignKey(Topic,verbose_name=u'主题')
    member = models.ForeignKey(User,verbose_name=u'成员')
    comment = models.CharField(u'评论',max_length=140)
    time = models.DateTimeField(u'投票时间',auto_now_add=True)

    class Meta:
        verbose_name = u'投票'
        verbose_name_plural = u'投票'

class LiveMessage(models.Model):
    """
    某次活动中的一条直播消息,可能会被同时发送至微博或Twitter。
    """
    event = models.ForeignKey(Event,verbose_name=u'活动')
    text = models.CharField(u'消息',max_length=140)
    create_by = models.ForeignKey(User,verbose_name=u'作者',related_name="createdMessage")
    create_time = models.DateTimeField(u'发送时间',auto_now_add=True)
    update_by = models.ForeignKey(User,verbose_name=u'最后修改人',related_name="updatedMessage")
    update_time = models.DateTimeField(u'更新时间',auto_now=True)

    class Meta:
        verbose_name = u'直播消息'
        verbose_name_plural = u'直播消息'


