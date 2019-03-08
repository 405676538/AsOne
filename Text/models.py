from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=20)


class UserInfo(models.Model):
    name = models.CharField(max_length=20)
    photo = models.CharField(max_length=20, default="")
    pwd = models.CharField(max_length=20, default="")
    head = models.CharField(max_length=20, default="")


class Contact(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    email = models.EmailField()

    def __unicode__(self):
        return self.name


# 统一的上传文件接口
class UpLoadFile(models.Model):
    fileId = models.CharField(max_length=200)


class Music(models.Model):
    musicId = models.CharField(max_length=200)
    imgId = models.CharField(max_length=200)
    audioId = models.CharField(max_length=200)
    openNum = models.IntegerField(default=0)
    title = models.CharField(max_length=200, default="")
    musicLabel = models.CharField(max_length=200, default="")  # 标签 用来分类
