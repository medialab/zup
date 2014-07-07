#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, csv, urllib2, re, codecs, shutil
from goose import Goose
from zipfile import ZipFile

from django.conf import settings
from django.utils.text import slugify


def unicode_dict_reader(utf8_data, **kwargs):
  '''
  Smart csv reader for unicode chars
  '''
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
      yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])



def gooseapi(url):
  '''
  Return a goose instance (with title and content only) for a specific url provided.
  '''
  
  goo = Goose()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
  response = opener.open(url)
  raw_html = response.read()
  return goo.extract(raw_html=raw_html)


def unique_mkdir(path):
  base_path = path
  c = 1
  while os.path.exists(path):
    candidate = '%s-%s' % (base_path, c)
    path = os.path.join(base_path, candidate)
    c += 1
  os.mkdir(path)
  return path


def urls_to_zip(urls=[], path=None, max_length=64):
  if path is None:
    path = "untitled"

  path = unique_mkdir(os.path.join(settings.TMP_ROOT, os.path.basename(path)))

  #create unique zip filename
  zipfied = os.path.join(settings.TMP_ROOT, 'urls_to_zip.zip')

  c = 1
  while os.path.exists(zipfied):
    candidate = '%s-%s.zip' % ('urls_to_zip', c)
    zipfied = os.path.join(settings.TMP_ROOT, candidate)
    c += 1

  with ZipFile(zipfied, 'w') as myzip:
    print "writing zip file ... "

    for i,url in enumerate(urls):
      print url
      g = gooseapi(url=url)
      slug = slugify(g.title)[:max_length]
      slug_base = slug

      textified = os.path.join(path, slug)
      print "pre writing on %s" % textified

      c = 1
      while os.path.exists(textified):

        candidate = '%s-%s' % (slug_base, c)
        print "writing on %s" % candidate
        if len(candidate) > max_length:
          slug = slug[:max_length-len('-%s' % c)]
        slug = re.sub('\-+','-',candidate)
        textified = os.path.join(path, slug)
        c += 1
      print "writing on %s" % textified

      with codecs.open(textified, encoding='utf-8', mode='w') as f:
        f.write('\n\n%s\n\n\n\n' % g.title)
        f.write(g.cleaned_text)
      
      myzip.write(textified, os.path.basename(textified))
      print "writing on %s" % textified
  shutil.rmtree(path)
  return zipfied
   

      