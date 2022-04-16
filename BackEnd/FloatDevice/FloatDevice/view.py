import mimetypes
import os
import json
import re
from wsgiref.util import FileWrapper

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse


if os.name=="nt":
    OS_TYPE="windows"
elif os.name=="posix":
    OS_TYPE="linux"


def parse_return_dir_data(root,dirs,files):
    """根据当前文件夹信息生成返回的json消息

    Args:
        root (str): 当前路径
        dirs (list): 文件夹列表
        files (list): 文件列表
    """
    result={}
    result['cur_path']=root
    result['dirs']=dirs
    result['files']=files
    return json.dumps(result)

def get_dirs_and_files(request):
    path=request.GET.get("path","/")
    if os.path.isfile(path):
        pass
    elif os.path.isdir(path):
        if OS_TYPE=="linux":
            for root,dirs,files in os.walk(path):
                return JsonResponse(
                    {
                        "code":200,
                        "data":parse_return_dir_data(root,dirs,files),
                    }
                )
    else:
        #路径有误
        return JsonResponse(
                    {
                        "code":404,
                        "data":"",
                    }
                )


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data

def get_staict_video_file(request):
    """将视频文件以流媒体的方式响应"""
    path=request.GET.get("path",None)
    if path:
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
        range_match = range_re.match(range_header)
        size = os.path.getsize(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = first_byte + 1024 * 1024 * 8    # 8M 每片,响应体最大体积
            if last_byte >= size:
                last_byte = size - 1
                length = last_byte - first_byte + 1
                resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
                resp['Content-Length'] = str(length)
                resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            # 不是以视频流方式的获取时，以生成器方式返回整个文件，节省内存
            resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
            resp['Content-Length'] = str(size)
        resp['Accept-Ranges'] = 'bytes'
        return resp

def get_static_file(request):
    path=request.GET.get("path",None)
    if path:
        file = open(path, "rb")
        if 'jepg' in path or 'jpg' in path:
            return HttpResponse(file.read(), content_type='image/jpg')
        if 'text' in path or 'jpg' in path:
            return HttpResponse(file.read(), content_type='text/plain')
        if 'png' in path:
            return HttpResponse(file.read(), content_type='image/png')
        if 'pdf' in path:
            return HttpResponse(file.read(), content_type='application/pdf')
            

def get_back(request):
    path=request.GET.get("path","/")
    path=path.strip("/")
    path=path.split("/")
    path="/"+"/".join(path[:-1])
    if path=="":
        path='/'
    if OS_TYPE=="linux":
        for root,dirs,files in os.walk(path):
            return JsonResponse(
                {
                    "code":200,
                    "data":parse_return_dir_data(root,dirs,files),
                }
            )