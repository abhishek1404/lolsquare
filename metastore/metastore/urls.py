from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from metastore import views

from metastore.api.resources import resources



from django.conf import settings
from django.conf.urls.static import static

# from views import  SSOLoginView


# fine grained Resources - UI
v2_api = Api(api_name='v2')
v1_api = Api(api_name='v1')


v2_api.register(resources.VideosResource())
v2_api.register(resources.DownloadResource())

urlpatterns = patterns('',
                       # url(r'^login/$', SSOLoginView.as_view()),
                       url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^api/', include(v2_api.urls)),

                       # metastore can haz static
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^api/', include(v2_api.urls)),
                       url(r'^api/meta/', include(v2_api.urls)),
                       # url(r'^admin/compare/', views.diff_view, name='resource-diff-view'),
                       url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger'),
                           kwargs={
                               "tastypie_api_module": "metastore.urls.v2_api",
                               "namespace": "tastypie_swagger",
                               "version": "0.1"
                           }
                           ), )
# metastore can haz static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
