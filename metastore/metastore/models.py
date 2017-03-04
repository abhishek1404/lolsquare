# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
# * Rearrange models' order
# * Make sure each model has one field with primary_key=True
# * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

import json
import logging
import traceback

import django.db.models.options as options
from django.contrib.contenttypes.models import ContentType
from django.db import models
import subprocess


# This attribute is used to filter models that can be exported while moving solutions from sandbox to prod.
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('allow_sandbox_export',)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LolsModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True, )
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True
import hashlib
import random
class Videos(LolsModel):
    id = models.AutoField(primary_key=True)
    guid = models.CharField(max_length=40,blank=True)
    video_url = models.TextField(blank=True)
    video_title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    views = models.IntegerField(default=0)
    category = models.TextField(blank=True)
    download_url = models.TextField(blank=True)


    def __unicode__(self):
        return self.video_url
    def save(self, *args, **kwargs):

      if not self.guid:
        self.guid = hashlib.sha1(str(random.random())).hexdigest()
        super(Videos, self).save(*args, **kwargs)
      if not self.download_url:
        p = subprocess.Popen(["youtube-dl", "-g",self.video_url], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.download_url = out
        super(Videos, self).save(*args, **kwargs)


    class Meta:
        managed = True

