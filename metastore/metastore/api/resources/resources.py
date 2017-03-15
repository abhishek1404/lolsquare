import json
import logging
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=2)

from test import get_videos
from fb_down import get_facebook_url,get_twitter_url,get_youtube_url
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
import pafy
import subprocess
import urllib
import Queue
import urllib2
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
from threading import Thread
import time
logger.addHandler(logging.NullHandler())
servers = {1: "fzaqn", 2: "agobe",
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
        result = True
        # if urllib.urlopen(url).getcode()==200:
        #     print 200
        #     result = True
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
    e_url = fields.CharField(attribute='e_url')
    url = fields.CharField(attribute='url')
    class Meta:
        resource_name = 'down'
        allowed_method = ['get']

    def get_d_test(self,url):
        ret= {'d_url': get_videos(url),'m_url':'','url':url,'e_url':''
        }#))
        return ret


    def get_mp3_url(self,url,queue=None):
        print "thread is working"
        m_url = ''
        url = url
        try:
            check_url = 'https://d.yt-downloader.org/check.php?/f=mp3&v='+(url).split("v=")[1]
            print check_url
            response = requests.get(check_url)
            response=json.loads(response.content)
            print response
            m_url ='http://' + servers[int(response['sid'])] + '.yt-downloader.org/download.php?id=' + response['hash']
            print m_url
        except Exception as ex:
            print ex
        ret ={'m_url':m_url,'url':url}
        #queue.put(ret)
        return ret

    def youtube_url(self,url):
        # paff=pafy.new(url)
        # out = paff.getbest(preftype="mp4")
        # return out.url
        return get_youtube_url(url)

    def facebook_url(self,url):
        return get_facebook_url(url)

    def twitter_url(self,url):
        return get_twitter_url(url)


    def get_download_url(self,url,queue):
        print Thread.name
        m_url=''
        url = url
        d_url=''
        if "youtube" in url:
            out=self.youtube_url(url)
            d_url=out

            m_url = self.get_mp3_url(url)['m_url']
        if "facebook" in url:
            d_url=self.facebook_url(url)
            print d_url
        if "twitter" in url:
            d_url=self.twitter_url(url)

        ret= {'d_url': d_url,'m_url':m_url,'url':url,'e_url':''
        }
        queue.put(ret)
        return ret

    def get_search_list(self,query):
        yt_yrl = query
        textToSearch = yt_yrl
        query = urllib.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        urls = []
        count =0
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if '/watch' in (vid['href']):
                count =count+1
                v_id = (vid['href']).split("&")[0]
                url = 'https://www.youtube.com/' + v_id
                e_url ='http://www.youtube.com/embed'+v_id

                urls.append(
                {'e_url': e_url,   'url':url,'m_url':'','d_url':''})
            if count==3:
                break

        return urls


    def obj_get_list(self, bundle, **kwargs):
        yt_yrl = bundle.request.GET['yt_url']
        list = bundle.request.GET.get('list')
        posts = []
        if  ".com/" in yt_yrl:
            urls=[{'e_url': '',   'url':yt_yrl,'m_url':'','d_url':''}]
        else:
            urls = self.get_search_list(yt_yrl)
        print urls
        if list:
            return [dict2obj(x) for x in urls]



        q = Queue.Queue()
        q1 = Queue.Queue()
        threads = []

        for argument in urls:
            t = Thread(target=self.get_download_url, args=(argument['url'], q),name= argument['url'])
            t.start()
            threads.append(t)


        for t in threads:
            t.join()

        posts = [q.get() for _ in xrange(len(urls))]
        posts =[dict2obj(x) for x in posts]
        return posts




