# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from news.models import News
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexViews(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        news_list = News.objects.all()
        return news_list


