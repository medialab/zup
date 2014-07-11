#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


def helper_uuslug(model, instance, value, max_length=128):
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
  ERROR = 'ERR'
  COMPLETED = 'END'

  STATUS_CHOICES = (
    (STARTED, u'started'),
    (ERROR, u'error'),
    (COMPLETED, u'job completed')  
  )

  url = models.TextField()
  status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STARTED)



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

  date_created = models.DateTimeField(auto_now=True)
  date_last_modified = models.DateTimeField(auto_now_add=True)

  urls = models.ManyToManyField(Url)
  command = models.TextField()

  status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STARTED)
  
  
  def get_path(self):
    return os.path.join(settings.MEDIA_ROOT, "job-%s" % self.pk)


  def save(self, **kwargs):
    path = self.get_path()
    if not os.path.exists(path):
      os.makedirs(path)

    super(Job, self).save()



@receiver(pre_delete, sender=Job)
def delete_job(sender, instance, **kwargs):
  '''
  rename or delete the job path linked to the corpus instance.
  We should provide a zip with the whole text content under the name <user>.<YYYYmmdd>.zip, @todo
  '''
  path = instance.get_path()
  shutil.rmtree(path)

