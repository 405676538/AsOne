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
    timesa = str(time.time())
    return render(request, 'hello.html', context)


def testdb(request):
    response1 = ""
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Test.objects.all()
    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = Test.objects.filter(id=1)
    # 获取单个对象
    response3 = Test.objects.get(id=1)
    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    var = Test.objects.order_by('name')[0:2]
    # 数据排序
    Test.objects.order_by("id")
    # 更新id = 1的参数值
    # Test.objects.filter(id=1).update(name='Google')
    # 修改所有的列
    # Test.objects.all().update(name='Google')
    # 上面的方法可以连锁使用
    Test.objects.filter(name="runoob").order_by("id")
    # 删除id=1的数据
    # Test.objects.filter(id=1).delete()
    # 删除所有数据
    # Test.objects.all().delete()
    # 输出所有数据
    for var in list:
        response1 += var.name + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")


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


# 处理音乐数据
def musicCr(request):
    if request.method == "GET":
        musicLabels = str(request.GET.get("musicLabel"))
        print("musicLabels=" + musicLabels)
        if musicLabels != 'None' and musicLabels != '':
            print("说明传了标签")
            musicList = models.Music.objects.filter(musicLabel=musicLabels)
            json_datas = serializers.serialize("json", musicList)
            return HttpResponse(json_datas, content_type="application/json")
        else:
            musicList = models.Music.objects.all().order_by("openNum")  # 返回所有音频列表
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
        result = {"fileId": "creat success"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
    return HttpResponse("success")


def houseMusicAlbum(request):
    if request.method == "GET":
        musicList = models.MusicAlbum.objects.all()
        json = serializers.serialize("json", musicList)
        return HttpResponse(json, content_type="application/json")
    if request.method == "POST":
        imgUrl = request.POST.get("imgUrl")
        musicAlbumList = request.POST.get("musicAlbumList")
        models.MusicAlbum.objects.create(imgUrl=imgUrl, musicAlbumList=musicAlbumList)
        result = {"msg": "creat success"}
        data = serializers.serialize(result, content_type="application/json")
        return HttpResponse(data, content_type="application/json")
    return HttpResponse("success")
