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


from tastypie.resources import Resource
#import youtube-dl
import subprocess

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

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




class BaseModelResource(ModelResource):
    class Meta:
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True

    def determine_format(self, request):
        format = request.GET.get('format', 'json')
        if format in self._meta.serializer.formats:
            return self._meta.serializer.get_mime_for_format(format)
        return super(BaseModelResource, self).determine_format(request)

    def hydrate(self, bundle):
        if bundle.request.method == "POST":
            bundle.data['created_by'] = bundle.request.user.ldap_id
        elif bundle.request.method == "PUT":
            bundle.data['modified_by'] = bundle.request.user.ldap_id
        return bundle

    @classmethod
    def get_fields(cls, fields=None, excludes=None):
        """
        Unfortunately we must override this method because tastypie ignores 'blank' attribute
        on model fields.
        Here we invoke an insane workaround hack due to metaclass inheritance issues:
            http://stackoverflow.com/questions/12757468/invoking-super-in-classmethod-called-from-metaclass-new
        """
        this_class = next(c for c in cls.__mro__ if c.__module__ == __name__ and c.__name__ == 'BaseModelResource')
        fields = super(this_class, cls).get_fields(fields=fields, excludes=excludes)
        if not cls._meta.object_class:
            return fields
        for django_field in cls._meta.object_class._meta.fields:
            if django_field.blank == True:
                res_field = fields.get(django_field.name, None)
                if res_field:
                    res_field.blank = True
        return fields

import urllib
class PageNumberPaginator(Paginator):
    def page(self):
        output = super(PageNumberPaginator, self).page()
        output['page_number'] = int(self.offset / self.limit) + 1
        return output

class VideosResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
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
        if urllib.urlopen(url).getcode()==200:
            result = True
        return result

    def dehydrate(self, bundle):
        url = bundle.data['download_url']
        if not self.test_download_url(url):
            p = subprocess.Popen(["youtube-dl", "-g",bundle.data['video_url']], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out, err = p.communicate()
            bundle.data['download_url']= out
        return bundle

class DownloadResource(Resource):
    d_url = fields.CharField(attribute='d_url')
    class Meta:
        resource_name = 'down'
        allowed_method = ['get']
    def obj_get_list(self, bundle, **kwargs):
        yt_yrl = bundle.request.GET['yt_url']

        posts = []
        #your actual logic to retrieve contents from external source.
        p = subprocess.Popen(["youtube-dl", "-g",yt_yrl], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = p.communicate()
        #example
        posts.append(dict2obj(
            {
                'd_url': out,
            }
        ))


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

