import json
import time

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
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


# 处理音乐列表数据 0:全部 1：openNum  2:musicLabel 3:artist  4:upTime
def musicCr(request):
    if request.method == "GET":
        artType = int(request.GET.get("type"))
        quary = str(request.GET.get("content"))
        if artType == 0:
            musicList = models.Music.objects.all().order_by("openNum").order_by('-id')
        elif artType == 1:
            musicList = models.Music.objects.filter(openNum=quary).order_by('-id')
        elif artType == 2:
            musicList = models.Music.objects.filter(musicLabel=quary).order_by('-id')
        elif artType == 3:
            musicList = models.Music.objects.filter(artist=quary).order_by('-id')
        elif artType == 4:
            musicList = models.Music.objects.all().order_by("upTime").order_by('-id')
        else:
            musicList = models.Music.objects.all().order_by('-id')
        json_datas = serializers.serialize("json", musicList)
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


# 创建一个音乐集合（现在用于首页） type = 0 根据热门度排序
def houseMusicAlbum(request):
    if request.method == "GET":
        artType = int(request.GET.get("type"))
        if artType == 1:
            musicList = models.MusicAlbum.objects.all().order_by('-hotNum')
        else:
            musicList = models.MusicAlbum.objects.all().order_by('-id')
        jsonsn = serializers.serialize("json", musicList)
        return HttpResponse(jsonsn, content_type="application/json")
    if request.method == "POST":
        imgUrl = request.POST.get("imgUrl")
        title = request.POST.get("title")
        musicAlbumList = request.POST.get("musicAlbumList")
        albumId = str(time.time()) + "album"
        album = models.MusicAlbum.objects.create(imgUrl=imgUrl, musicAlbumList=musicAlbumList, title=title, albumId=albumId)
        list = str(musicAlbumList).split('~')
        for musicId in list:
            print("musicId=="+musicId)
            music = models.Music.objects.get(musicId=musicId)
            album.music_set.add(music)
        return suuccessResult()
    if request.method == "PUT":
        hotNum = request.GET.get("hotNum")
        albumId = request.GET.get("albumId")
        models.MusicAlbum.objects.filter(albumId=albumId).update(hotNum=hotNum)
        return suuccessResult()
    if request.method == "DELETE":
        albumId = request.DELETE.get("albumId")
        models.MusicAlbum.objects.filter(albumId=albumId).delete()
        return suuccessResult()
    return HttpResponse("success")


def musicAlbumDetail(request):
    if request.method == "GET":
        id = request.GET.get("albumId")
        musicAlbum = models.MusicAlbum.objects.get(albumId=id)
        list = musicAlbum.music_set.all()
        jsonsn = serializers.serialize("json", list)
        return HttpResponse(jsonsn, content_type="application/json")


# 艺术家添加或获取  type:约定 【0:不过滤 1:name 2：age 3：six 4：country 5：recommend 6：收藏列表 7:hot排序】
def artistList(request):
    if request.method == "GET":
        artType = int(request.GET.get("type"))
        typeContent = str(request.GET.get("typeContent"))
        userId = str(request.GET.get("userId"))
        print("type=" + str(artType))
        print("typeContent=" + typeContent)
        print("userId=" + userId)
        if artType == 0:
            artistAll = models.ArtistList.objects.all().order_by('-id')
        elif artType == 1:
            artistAll = models.ArtistList.objects.all().filter(name=typeContent)
        elif artType == 2:
            artistAll = models.ArtistList.objects.all().filter(age=typeContent)
        elif artType == 3:
            artistAll = models.ArtistList.objects.all().filter(six=typeContent)
        elif artType == 4:
            artistAll = models.ArtistList.objects.all().filter(country=typeContent)
        elif artType == 5:
            artistAll = models.ArtistList.objects.all().filter(recommend=typeContent).order_by('-id')
        elif artType == 6:
            artistAll = models.UserInfo.objects.get(uid=userId).artistlist_set.all().order_by('-id')
        elif artType == 7:
            artistAll = models.ArtistList.objects.all().order_by('-id').order_by('-hotNum')
        else:
            artistAll = models.ArtistList.objects.all()
        jsonsn = serializers.serialize("json", artistAll)
        return HttpResponse(jsonsn, content_type="application/json")
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        six = request.POST.get("six")
        brief = request.POST.get("brief")
        head = request.POST.get("head")
        country = request.POST.get("country")
        recommend = request.POST.get("recommend")
        upId = str(time.time())
        models.ArtistList.objects.create(name=name, age=age, six=six, brief=brief, head=head, country=country,
                                         recommend=recommend, upId=upId)
        return suuccessResult()
    if request.method == "PUT":
        hotNum = request.GET.get("hotNum")
        upId = request.GET.get("upId")
        models.ArtistList.objects.filter(upId=upId).update(hotNum=hotNum)
        return suuccessResult()
    if request.method == "DELETE":
        upId = request.GET.get("upId")
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
    if request.method == "POST":
        userId = request.POST.get("userId")
        upId = request.POST.get("upId")
        user = models.UserInfo.objects.get(uid=userId)
        artist = models.ArtistList.objects.get(upId=upId)
        artist.userInfos.add(user)
        return suuccessResult()
    if request.method == "DELETE":
        userId = request.GET.get("userId")
        upId = request.GET.get("upId")
        user = models.UserInfo.objects.get(uid=userId)
        artist = models.ArtistList.objects.get(upId=upId)
        artist.userInfos.remove(user)
        return suuccessResult()


def userAdd(request):
    if request.method == "POST":
        uid = request.POST.get("uid")
        name = request.POST.get("name")
        head = request.POST.get("head")
        try:
            models.UserInfo.objects.get(uid=uid)
        except:
            models.UserInfo.objects.create(uid=uid, name=name, head=head)
        return suuccessResult()


def version(request):
    if request.method == "GET":
        if (models.Version.objects.all().count() <= 0):
            return HttpResponse("json", models.Version.objects.all())
        else:
            versionAll = models.Version.objects.order_by("versionCode")
            jsondata = serializers.serialize("json", versionAll)
        return HttpResponse(jsondata, content_type="application/json")
    if request.method == "POST":
        versionCode = request.POST.get("versionCode")
        apkId = request.POST.get("apkId")
        models.Version.objects.create(versionCode=versionCode, apkId=apkId)
        return suuccessResult()
