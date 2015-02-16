#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
  d = _helper_shared_context(request)
  return render_to_response("zup/index.html", RequestContext(request, d))



def _helper_shared_context(request, tags=[], d={}):
  '''
  Return an happy shared contex for your view
  '''
  d.update({
    'TITLE': settings.TITLE,
    'DEBUG': settings.DEBUG,
    'ENABLE_CDN_SERVICES': settings.ENABLE_CDN_SERVICES,
    'LANGUAGE': request.LANGUAGE_CODE
  })
  return d