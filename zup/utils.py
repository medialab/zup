#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, csv, urllib2, re, codecs, shutil, unicodecsv, logging
from goose import Goose
from zipfile import ZipFile

from django.conf import settings
from django.utils.text import slugify



logger = logging.getLogger('zup')



def unicode_dict_reader(utf8_data, **kwargs):
  '''
  Smart csv reader for unicode chars
  '''
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
      yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])



def gooseapi(url):
  '''
  Return a goose instance for the given url. Goose instance brings together title and content from the pointed page body.
  '''
  logger.debug('fetching url: %s' % url);
  goo = Goose({'browser_user_agent': 'Mozilla'})
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
  response = opener.open(url)
  raw_html = response.read()
  return goo.extract(raw_html=raw_html)



def unique_mkdir(path):
  '''
  Return a unique filename for a given path
  '''
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
  Given a list of urls, try to extract the body content from each url and put it in a txt file.
  The files are zipped together and delivered as filepath at the end.
  Cfr Goose documentation and gooseapi function as well.
  '''
  if path is None:
    path = "untitled"

  # create unique folder
  path = unique_mkdir(os.path.join(settings.TMP_ROOT, os.path.basename(path)))
  # create zip filename
  zipfied = os.path.join(settings.TMP_ROOT, 'urls_to_zip.zip')
  # create csv report filename
  report_path = os.path.join(path, 'report.csv')

  c = 1
  while os.path.exists(zipfied):
    candidate = '%s-%s.zip' % ('urls_to_zip', c)
    zipfied = os.path.join(settings.TMP_ROOT, candidate)
    c += 1

  reports = []

  with ZipFile(zipfied, 'w') as myzip:
    logger.debug('zip file opened to bring %s urls' % len(urls))
    
    # 1 of 2. fill zip with each page body
    for i,url in enumerate(urls):
      index = '%0*d' % (5, int(i) + 1)
      logger.debug('url %s of %s' % (i+1, len(urls)))
      try:
        g = gooseapi(url=url)
      except urllib2.HTTPError, e:
        logger.debug('HTTPError %s for url %s'% (e, url))
      except Exception, e:
        logger.exception(e)
        continue

      slug = '%s-%s' % (index,slugify(g.title)[:max_length])
      slug_base = slug

      textified = os.path.join(path, slug)
      
      c = 1 # unique filename for the text file
      while os.path.exists(textified):  
        candidate = '%s-%s-%s' % (index, slug_base, c)
        print "writing on %s" % candidate
        if len(candidate) > max_length:
          slug = slug[:max_length-len('-%s' % c)]
        slug = re.sub('\-+','-',candidate)
        textified = os.path.join(path, slug)
        c += 1

      textified = "%s.txt" % textified

      # open textified file and write goose body content, with title.
      with codecs.open(textified, encoding='utf-8', mode='w') as f:
        f.write('\n\n%s\n\n\n\n' % g.title)
        f.write(g.cleaned_text)
      # the row dict to be written as csv row
      result = {
        'id': i,
        'path': os.path.basename(textified),
        'url': url
      }
      # if there are tags given from goose, they are given as a list. We join it with nice commas.
      for field in fields:
        if field == 'tags':
          result[field] = ', '.join(getattr(g, field))
        else:
          result[field] = getattr(g, field)
      # push our line with the others
      reports.append(result)
      logger.debug('txt file added to zip file')

      myzip.write(textified, os.path.basename(textified))

    # 2 of 2. write csv data
    logger.debug('writing csv report for %s url of %s' % (len(reports), len(urls)))
    with open(report_path, 'w') as report:
      writer = unicodecsv.DictWriter(report, ['id', 'path', 'url'] + fields)
      writer.writeheader()
      for report in reports:
        writer.writerow(report)
    
    myzip.write(report_path, os.path.basename(report_path))
    logger.debug('csv report added to zipfile %s' % zipfied)
    
  shutil.rmtree(path)
  return zipfied
   

      