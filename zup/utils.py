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


def urls_to_zip(urls=[], path=None, max_length=64, fields=['title', 'tags', 'meta_keywords']):
  '''

  Cfr Goose documentation
  '''
  if path is None:
    path = "untitled"

  # create unique folder
  path = unique_mkdir(os.path.join(settings.TMP_ROOT, os.path.basename(path)))
  # create zip filename
  zipfied = os.path.join(settings.TMP_ROOT, 'urls_to_zip.zip')
  # create csv report
  report_path = os.path.join(path, 'report.csv')

  c = 1
  while os.path.exists(zipfied):
    candidate = '%s-%s.zip' % ('urls_to_zip', c)
    zipfied = os.path.join(settings.TMP_ROOT, candidate)
    c += 1

  reports = []

  with ZipFile(zipfied, 'w') as myzip:
    print "writing zip file ... "

    for i,url in enumerate(urls):
      index = '%0*d' % (5, int(i) + 1)
      
      g = gooseapi(url=url)
      slug = '%s-%s' % (index,slugify(g.title)[:max_length])
      slug_base = slug

      textified = os.path.join(path, slug)
      print "pre writing on %s" % textified

      c = 1
      while os.path.exists(textified):
        
        candidate = '%s-%s-%s' % (index, slug_base, c)
        print "writing on %s" % candidate
        if len(candidate) > max_length:
          slug = slug[:max_length-len('-%s' % c)]
        slug = re.sub('\-+','-',candidate)
        textified = os.path.join(path, slug)
        c += 1

      textified = "%s.txt" % textified

      print "writing on %s" % textified

      with codecs.open(textified, encoding='utf-8', mode='w') as f:
        f.write('\n\n%s\n\n\n\n' % g.title)
        f.write(g.cleaned_text)
      
      result = {
        'id': i,
        'path': os.path.basename(textified),
        'url': url
      }

      for i in fields:
        if i == 'tags':
          result[i] = ', '.join(getattr(g, i))
        else:
          result[i] = getattr(g, i)

      reports.append(result)


      myzip.write(textified, os.path.basename(textified))
      print "writing on %s" % textified
      
      print reports
    #  2. write csv data
    
    with open(report_path, 'w') as report:
      writer = csv.DictWriter(report, ['id', 'path', 'url'] + fields)
      writer.writeheader()
      for report in reports:
        writer.writerow(report)
  
    myzip.write(report_path, os.path.basename(report_path))

  shutil.rmtree(path)
  return zipfied
   

      