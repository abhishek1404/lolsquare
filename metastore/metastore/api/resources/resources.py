import json
import logging
# import traceback
# from datetime import datetime
#
# from django.apps import apps
# from django.conf import settings
# from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Max
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from reversion.models import Version
# from tastypie import fields
# from tastypie import http
# from tastypie.bundle import Bundle
# from tastypie.exceptions import BadRequest
# from tastypie.resources import ALL, ALL_WITH_RELATIONS
# from tastypie.utils.mime import build_content_type
#
# from metastore import models
# from metastore.api.core import utils as core_utils
# from metastore.api.core.compare_reversion import VersionCompare
# from metastore.api.core.resource_reversion import BaseMetastoreResource, BaseModelResource, BaseModelVersionResource, \
#     CloneResource
# from metastore.api.utils import querybuilder, scm
# from metastore.api.utils import utils
from metastore.models import Videos
from tastypie.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.paginator import Paginator
from django.http import HttpResponse
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
import requests
from tastypie.resources import Resource
#import youtube-dl
import subprocess
import urllib
import urllib2
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
servers = {
            1: "fzaqn",
            2: "agobe",
            3: "topsa",
            4: "hcqwb",
            5: "gdasz",
            6: "iooab",
            7: "idvmg",
            8: "bjtpp",
            9: "sbist",
            10: "gxgkr",
            11: "njmvd",
            12: "trciw",
            13: "sjjec",
            14: "puust",
            15: "ocnuq",
            16: "qxqnh",
            17: "jureo",
            18: "obdzo",
            19: "wavgy",
            20: "qlmqh",
            21: "avatv",
            22: "upajk",
            23: "tvqmt",
            24: "xqqqh",
            25: "xrmrw",
            26: "fjhlv",
            27: "ejtbn",
            28: "urynq",
            29: "tjljs",
            30: "ywjkg"
        }
class dict2obj(object):
    """
    Convert dictionary to object
    @source http://stackoverflow.com/a/1305561/383912
    """
    def __init__(self, d):
        self.__dict__['d'] = d

    def __getattr__(self, key):
        value = self.__dict__['d'][key]
        if type(value) == type({}):
            return dict2obj(value)

        return value


import urllib
class PageNumberPaginator(Paginator):
    def page(self):
        output = super(PageNumberPaginator, self).page()
        output['page_number'] = int(self.offset / self.limit) + 1
        return output

class VideosResource(ModelResource):
    class Meta:
        allowed_methods = ['get', 'post', 'put']
        authentication = Authentication()
        authorization = Authorization()
        queryset = Videos.objects.all()
        limit = 4
        resource_name = 'videos'
        always_return_data = True
        filtering = {
            'category': ALL_WITH_RELATIONS,
            'video_title':ALL,
        }
        paginator_class = Paginator

    def test_download_url(self,url):
        result = False
        if urllib.urlopen(url).getcode()==200:
            print 200
            result = True
        return result

    def dehydrate(self, bundle):
        url = bundle.data['download_url']
        if not self.test_download_url(url):
            p = subprocess.Popen(["youtube-dl", "-g",bundle.data['video_url']], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out, err = p.communicate()
            # video = Videos.objects.get(id=bundle.data['id'])
            # video.download_url=out
            # video.save()
            bundle.data['download_url']= out
        return bundle





























class DownloadResource(Resource):
    d_url = fields.CharField(attribute='d_url')
    m_url = fields.CharField(attribute='m_url')
    url = fields.CharField(attribute='url')
    class Meta:
        resource_name = 'down'
        allowed_method = ['get']
    def obj_get_list(self, bundle, **kwargs):
        yt_yrl = bundle.request.GET['yt_url']
        textToSearch = yt_yrl
        query = urllib.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        posts = []
        count =0
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if '/watch' in (vid['href']):
                count =count+1
                url = 'https://www.youtube.com' + (vid['href']).split("&")[0]
                check_url = 'https://d.yt-downloader.org/check.php?/f=mp3&v='+(vid['href']).split("&")[0].split("v=")[1]
                print check_url
                response = requests.get(check_url)
                response=json.loads(response.content)
                print response
                m_url ='http://' + servers[int(response['sid'])] + '.yt-downloader.org/download.php?id=' + response['hash']
                print m_url
                p = subprocess.Popen(["youtube-dl", "-g",url], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                out, err = p.communicate()
        #
                posts.append(dict2obj(
                {
                    'd_url': out,
                    'm_url':m_url,
                    'url':url
                }))
            if count==1:
                break

        return posts

    # def test_download_url(self,url):
    #     result = True
    #     if urllib.urlopen(url).getcode()==200:
    #         result = True
    #     return result

    # def dehydrate(self, bundle):
    #     url = bundle.data['download_url']
    #     #if self.test_download_url(url):
    #     p = subprocess.Popen(["youtube-dl", "-g",bundle.data['video_url']], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #     out, err = p.communicate()
    #     bundle.data['download_url']= out
    #     return bundle

