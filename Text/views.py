import json
import time

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from Text import models
from Text.models import Test
from operator import itemgetter, attrgetter

# 文件路径配置
filePath = "D:\\work\\python_project\\file"


# filePath = "\\mnt\\ceph\\file"


def hello(request):
    context = {"hello": 'Hello World!'}
    return render(request, 'hello.html', context)


def testdb(request):
    return HttpResponse("<p>" + "" + "</p>")


def suuccessResult():
    result = {"fileId": "creat success"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 图片上传接口  字段传file  调用http://127.0.0.1:8000/upLoad
def upLoadFile(request):
    path = filePath
    file_obg = request.FILES.get('file')
    fileId = getAnStr(str(time.time()) + "fileId")
    import os
    if not os.path.exists(path):
        os.makedirs(path)
    if not file_obg:
        return HttpResponse("no file uoLoad")
    destination = open(os.path.join(path, fileId), 'wb')
    for chunk in file_obg.chunks():
        destination.write(chunk)
    destination.close()
    models.UpLoadFile.objects.create(fileId=fileId)
    result = {"fileId": fileId}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def getAnStr(fileName):
    if "jpg" in str(fileName):
        return fileName + ".jpg"
    if "png" in str(fileName):
        return fileName + ".png"
    if "mp3" in str(fileName):
        return fileName + ".mp3"
    else:
        return fileName


# 下载文件
def downLoadFile(request, file_name):
    name = file_name
    print("下载ID=" + name)

    def file_iterator(name_file, chunk_size=51200000):
        with open(name_file, 'rb') as f:
            if f:
                yield f.read(chunk_size)
                print('下载完成')
            else:
                print('未完成下载')

    the_file_name = filePath + "\\" + name
    print("下载路径=" + the_file_name)
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename="{0}"'.format(name)
    return response


# 处理音乐列表数据
def musicCr(request):
    if request.method == "GET":
        musicLabels = str(request.GET.get("musicLabel"))
        print("musicLabels=" + musicLabels)
        if musicLabels != 'None' and musicLabels != '':
            print("说明传了标签")
            musicList = models.Music.objects.filter(musicLabel=musicLabels).reverse()
            json_datas = serializers.serialize("json", musicList)
            return HttpResponse(json_datas, content_type="application/json")
        else:
            musicList = models.Music.objects.all().order_by("openNum").reverse()  # 返回所有音频列表
            if musicList.count() > 100:
                musicList = musicList[0, 100]
            json_datas = serializers.serialize("json", musicList)
            print("json_datas get方法" + json_datas)
            return HttpResponse(json_datas, content_type="application/json")

    if request.method == "POST":
        audioId = request.POST.get("audioId")
        imgId = request.POST.get("imgId")
        title = request.POST.get("title")
        musicLabel = request.POST.get("musicLabel")
        musicId = str(time.time()) + imgId
        artist = request.POST.get("artist")
        country = request.POST.get("country")
        upTime = time.time()
        models.Music.objects.create(audioId=audioId, imgId=imgId, title=title, musicLabel=musicLabel, musicId=musicId,
                                    artist=artist, country=country, upTime=upTime)
        return suuccessResult()
    if request.method == "DELETE":
        musicId = request.DELETE.get("musicId")
        models.Music.objects.filter(musicId=musicId).delete()
        return suuccessResult()
    return HttpResponse("success")


# 创建一个音乐集合（现在用于首页）
def houseMusicAlbum(request):
    if request.method == "GET":
        musicList = models.MusicAlbum.objects.all()
        jsonsn = serializers.serialize("json", musicList)
        return HttpResponse(jsonsn, content_type="application/json")
    if request.method == "POST":
        imgUrl = request.POST.get("imgUrl")
        title = request.POST.get("title")
        musicAlbumList = request.POST.get("musicAlbumList")
        albumId = time.time() + "album"
        models.MusicAlbum.objects.create(imgUrl=imgUrl, musicAlbumList=musicAlbumList, title=title, albumId=albumId)
        return suuccessResult()
    if request.method == "DELETE":
        albumId = request.DELETE.get("albumId")
        models.MusicAlbum.objects.filter(albumId=albumId).delete()
        return suuccessResult()
    return HttpResponse("success")


# 艺术家添加或获取
def artistList(request):
    if request.method == "GET":
        artistAll = models.ArtistList.objects.all()
        jsondata = serializers.serialize("json", artistAll)
        return HttpResponse(jsondata, content_type="application/json")
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        six = request.POST.get("six")
        brief = request.POST.get("brief")
        head = request.POST.get("head")
        country = request.POST.get("country")
        recommend = request.POST.get("recommend")
        upId = time.time() + name
        models.ArtistList.objects.create(name=name, age=age, six=six, brief=brief, head=head, country=country,
                                         recommend=recommend, upId=upId)
        return suuccessResult()
    if request.method == "DELETE":
        upId = request.DELETE.get("upId")
        models.ArtistList.objects.filter(upId=upId).delete()
        return suuccessResult()


# 国家种类添加或获取
def country(request):
    if request.method == "GET":
        countryAll = models.Country.objects.all()
        jsondata = serializers.serialize("json", countryAll)
        return HttpResponse(jsondata, content_type="application/json")
    if request.method == "POST":
        name = request.POST.get("name")
        banner = request.POST.get("banner")
        models.Country.objects.create(name=name, banner=banner)
        return suuccessResult()
    if request.method == "DELETE":
        name = request.DELETE.get("name")
        models.Country.objects.filter(name=name).delete()
        return suuccessResult()


# 声音种类添加或获取
def sound(request):
    if request.method == "GET":
        soundAll = models.Sound.objects.all()
        jsondata = serializers.serialize("json", soundAll)
        return HttpResponse(jsondata, content_type="application/json")
    if request.method == "POST":
        name = request.POST.get("name")
        imgUrl = request.POST.get("imgUrl")
        models.Sound.objects.create(name=name, imgUrl=imgUrl)
        return suuccessResult()
    if request.method == "DELETE":
        name = request.DELETE.get("name")
        models.Sound.objects.filter(name=name).delete()
        return suuccessResult()


# 用户收藏Up主的表
def userCollectUp(request):
    if request.method == "GET":
        userId = str(request.GET.get("userId"))
        soundAll = models.UserCollectUp.objects.all().filter(userId=userId)
        jsondata = serializers.serialize("json", soundAll)
        return HttpResponse(jsondata, content_type="application/json")
    if request.method == "POST":
        userId = request.POST.get("userId")
        upId = request.POST.get("upId")
        models.UserCollectUp.objects.create(userId=userId, upId=upId)
        return suuccessResult()
    if request.method == "DELETE":
        userId = request.DELETE.get("userId")
        upId = request.DELETE.get("upId")
        models.UserCollectUp.objects.filter(userId=userId, upId=upId).delete()
        return suuccessResult()
