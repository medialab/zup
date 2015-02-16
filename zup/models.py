#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, os, shutil, subprocess

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify

def helper_uuslug(model, instance, value, max_length=128):
  '''
  create a unique slug key for a specific value, according to other model instances.
  instance should be provided not to change instance's own name.

  '''
  slug = slugify(value)[:max_length] # safe autolimiting
  slug_base = slug
  i = 1;

  while model.objects.exclude(pk=instance.pk).filter(slug=slug).count():
    candidate = '%s-%s' % (slug_base, i)
    if len(candidate) > max_length:
      slug = slug[:max_length-len('-%s' % i)]
    slug = re.sub('\-+','-',candidate)
    i += 1

  return slug



class Url(models.Model):
  STARTED = 'BOO'
  READY = 'REA'
  ERROR = 'ERR'
  COMPLETED = 'END'

  STATUS_CHOICES = (
    (STARTED, u'started'),
    (READY, u'ready'),
    (ERROR, u'error'),
    (COMPLETED, u'job completed')  
  )

  url = models.URLField()
  log = models.TextField() # solo errore

  date_created = models.DateTimeField(auto_now_add=True)
  date_last_modified = models.DateTimeField(auto_now=True)

  status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STARTED)


  def json(self, deep=False):
    d = {
      'id': self.id,
      'url': self.url,
      'status': self.status,
      'date_created': self.date_created.isoformat(),
      'date_last_modified': self.date_last_modified.isoformat() if self.date_last_modified else None
    }

    if self.date_last_modified is not None:
      elapsedTime = self.date_created - self.date_last_modified
      d['elapsed'] = elapsedTime.total_seconds()
    else:
      d['elapsed'] = 0
    return d



class Job(models.Model):
  STARTED = 'BOO'
  RUNNING = 'RUN'
  LOST = 'RIP'
  COMPLETED = 'END'
  TOBEREMOVED = 'RIP'

  STATUS_CHOICES = (
    (STARTED, u'started'),
    (RUNNING, u'running'),
    (LOST, u'process not found'),
    (COMPLETED, u'job completed'),
    (TOBEREMOVED, u'to be deleted') 
  )

  name = models.CharField(max_length=64)
  slug = models.CharField(max_length=64, unique=True)
  
  date_created = models.DateTimeField(auto_now_add=True)
  date_last_modified = models.DateTimeField(auto_now=True)

  urls = models.ManyToManyField(Url)
  command = models.TextField()

  status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STARTED)
  

  def __unicode__(self):
    return '%s %s' % (self.name, self.status)


  def json(self, deep=False):
    d = {
      'id': self.id,
      'name': self.name,
      'status': self.status,
      'date_created': self.date_created.isoformat(),
      'date_last_modified': self.date_last_modified.isoformat() if self.date_last_modified else None,
    }
    if deep:
      d.update({
        'urls': [u.json() for u in self.urls.all()]
      })
      completed = 0.0;
      for url in d['urls']:
        completed += 1 if url['status'] != Url.STARTED else 0

      d['completion'] = completed / len(d['urls'])

      d['completion_label'] = '%s of %s' % (completed, len(d['urls']))
    return d
  

  def get_path(self):
    index = '%0*d' % (5, int(self.pk) + 1)
    path = os.path.join(settings.TMP_ROOT, "job-%s-%s" % (self.pk, self.slug))
    if not os.path.exists(path):
      os.makedirs(path)
    return path


  def save(self, **kwargs):
    if self.pk is None:
      self.slug = helper_uuslug(model=Job, instance=self, value=self.name)
    
    super(Job, self).save()

    # get_path makes use of newborn slug
    path = self.get_path()


  def start(self, cmd=''):
    popen_args = [
      settings.PYTHON_INTERPRETER,
      os.path.join(settings.BASE_DIR,'manage.py'),
      'start_job',
      '--cmd','scrape',
      '--job', str(self.pk)]
    if self.status == Job.STARTED:
      subprocess.Popen(popen_args, stdout=None, stderr=None, close_fds=True)
      
    print popen_args


@receiver(pre_delete, sender=Job)
def delete_job(sender, instance, **kwargs):
  '''
  rename or delete the job path linked to the corpus instance.
  We should provide a zip with the whole text content under the name <user>.<YYYYmmdd>.zip, @todo
  '''
  path = instance.get_path()
  shutil.rmtree(path)

