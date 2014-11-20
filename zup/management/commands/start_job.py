#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, csv, time, codecs, shutil, urllib2, logging
from optparse import make_option
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from zipfile import ZipFile
from zup.utils import gooseapi, unicode_dict_reader, unique_mkdir
from zup.models import Job, Url


logger = logging.getLogger('zup')


class Command(BaseCommand):
  '''
  usage type:
  
  python manage.py start_job --job=1 --cmd=test
  '''
  args = ''
  help = 'execute some job on corpus.'
  option_list = BaseCommand.option_list + (
    make_option('--job',
      action='store',
      dest='job_pk',
      default=False,
      help='job primary key'),

    make_option('--cmd',
        action='store',
        dest='cmd',
        default=False,
        help='manage.py command to be executed'),
  )


  def _test(self, job):
    job.status = Job.RUNNING
    job.save()
    time.sleep(15)
    job.status = Job.COMPLETED
    job.save()


  def _scrape(self, job, fields=['title', 'tags', 'meta_keywords']):
    logger.debug('starting command "scrape"')
    job.status = Job.RUNNING
    job.save()
    
    job_path = job.get_path()
    path = unique_mkdir(os.path.join(job_path, 'files'))

    urls = job.urls.all()
    # create zip filename and remove previous one
    zip_path = os.path.join(job_path, 'urls_to_zip.zip')
    if os.path.exists(zip_path):
      os.remove(zip_path)

    # create csv report
    rep_path = os.path.join(path, 'report.csv')
    reports = []

    logger.debug('zip path: %s' % zip_path)
    

    # filename length
    max_length = 64

    with ZipFile(zip_path, 'w') as zip_file:
      for i,url in enumerate(urls): # sync or not async
        index = '%0*d' % (5, int(i) + 1)
        url.status= Url.READY
        url.save()

        try:
          g = gooseapi(url=url.url)
        except urllib2.HTTPError, e:
          url.status= Url.ERROR
          url.log = '%s' % e
          url.save()
          continue
        except urllib2.URLError, e:
          url.status= Url.ERROR
          url.log = '%s' % e
          url.save()
          continue
        except ValueError, e: # that is, url is not a valid url
          url.status= Url.ERROR
          url.log = '%s' % e
          url.save()
          continue
        except IOError, e: # probably the stopword file was not found, skip this url
          url.status= Url.ERROR
          url.log = '%s' % e
          url.save()
          continue
        except Exception, e:
          logger.exception(e)
          continue

        logger.debug('title: %s', g.title)
        logger.debug('url:   %s', url.url)
        # handling not found title stuff
        slug = '%s-%s' % (index,slugify(g.title if g.title else url.url)[:max_length])
        slug_base = slug
        
        textified = os.path.join(path, slug)

        c = 1
        while os.path.exists(textified):
          
          candidate = '%s-%s-%s' % (index, slug_base, c)
          
          if len(candidate) > max_length:
            slug = slug[:max_length-len('-%s' % c)]
          slug = re.sub('\-+','-',candidate)
          textified = os.path.join(path, slug)
          c += 1

        textified = "%s.txt" % textified

        with codecs.open(textified, encoding='utf-8', mode='w') as f:
          f.write('\n\n%s\n\n\n\n' % g.title)
          f.write(g.cleaned_text)
        
        # completed url scraping
        url.status= Url.COMPLETED
        url.save()

        zip_file.write(textified, os.path.basename(textified))
      
        # WRITE SOME REPORT
        result = {
          'id': index,
          'path': os.path.basename(textified),
          'url': url.url
        }

        for i in fields:
          if i == 'tags':
            result[i] = ', '.join(getattr(g, i))
          else:
            result[i] = getattr(g, i)
          result[i]=result[i].encode('utf8')
        reports.append(result)

      # JOB FINISHED, WRITING REPORT
      with open(rep_path, 'w') as report:
        writer = csv.DictWriter(report, ['id', 'path', 'url'] + fields)
        writer.writeheader()
        for report in reports:
          writer.writerow(report)
    
      zip_file.write(rep_path, os.path.basename(rep_path))
    
    shutil.rmtree(path)
    # close job
    job.status = Job.COMPLETED
    job.save()


  def handle(self, *args, **options):
    if not options['cmd']:
      raise CommandError("\n    ouch. You should specify a valid function as cmd param")
    if not options['job_pk']:
      raise CommandError("\n    ouch. please provide a job id to record logs and other stuff")
    
    # maximum 5 jobs at the same time
    try:
      job = Job.objects.get(pk=options['job_pk'])
    except Job.DoesNotExist, e:
      raise CommandError("\n    ouch. Try again, job pk=%s does not exist!" % options['job_pk'])

    cmd = '_%s' % options['cmd']

    getattr(self, cmd)(job=job) # no job will be charged!
    

  
