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
    openNum = models.IntegerField(default=0)  # 播放量
    title = models.CharField(max_length=200, default="")  # 标题
    musicLabel = models.CharField(max_length=200, default="")  # 标签 用来分类
    artist = models.CharField(max_length=200, default="")  # 艺术家
    country = models.CharField(max_length=200, default="")  # 国家
    upTime = models.FloatField(max_length=400, default=-1)  # 上传时间


class MusicAlbum(models.Model):
    imgUrl = models.CharField(max_length=200)
    musicAlbumList = models.CharField(max_length=3000)
    title = models.CharField(default="", max_length=100)


class ArtistList(models.Model):
    name = models.CharField(max_length=200, default="")
    age = models.CharField(max_length=200, default="")
    six = models.CharField(max_length=200, default="")
    brief = models.CharField(max_length=2000, default="")
    head = models.CharField(max_length=200, default="")
    country = models.CharField(max_length=200, default="")
    recommend = models.CharField(max_length=200, default=-1)


class Country(models.Model):
    name = models.CharField(max_length=200)
    banner = models.CharField(max_length=200, default="")
