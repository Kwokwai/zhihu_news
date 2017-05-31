# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class News(models.Model):
    news_id = models.CharField('id', max_length=32)
    news_title = models.CharField('新闻标题', max_length=100)
    image_url = models.CharField('图片链接', max_length=255)
    share_url = models.CharField('新闻链接', max_length=255)