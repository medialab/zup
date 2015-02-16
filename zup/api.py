from django.conf import settings
from django.db import transaction
from glue import Epoxy, API_EXCEPTION_AUTH, API_EXCEPTION_FORMERRORS, API_EXCEPTION_DOESNOTEXIST
from zup.forms import JobForm
from zup.models import Url, Job

# api
def home(request):
  '''
  Help or manual should be placed here
  '''
  result = Epoxy(request)
  return result.json()


def job(request, pk):
  epoxy = Epoxy(request)
  try:
    epoxy.item(Job.objects.get(pk=pk), deep=True)
  except Job.DoesNotExist, e:
    return epoxy.throw_error(code=API_EXCEPTION_DOESNOTEXIST, error=e).json()
  
  return epoxy.json()



def jobs(request):
  epoxy = Epoxy(request)

  if epoxy.is_POST():
    form = JobForm(epoxy.data)

    if not form.is_valid():
      return epoxy.throw_error(error=form.errors).json()

    with transaction.atomic():
      job = form.save()
      # Cfr forms.py claened data is here a list of (not yet) valid url
      urllist = form.cleaned_data['url_list']
      # limit on url list
      if not request.user.is_staff:
        urllist = urllist[:settings.URLS_LIMIT]

      for url in urllist:
        u = Url(url=url)
        u.save()
        job.urls.add(u)

    job.start(cmd='scrape')
    epoxy.item(job)

  return epoxy.json()



def job_download(request, pk):
  import os
  from mimetypes import guess_type
  from django.core.servers.basehttp import FileWrapper
  from django.http import HttpResponse

  epoxy = Epoxy(request) # useful to handle errors
  try:
    j = Job.objects.get(pk=pk)
  except Job.DoesNotExist, e:
    return epoxy.throw_error(code=API_EXCEPTION_DOESNOTEXIST, error=e).json()
  
  filepath = os.path.join(j.get_path(), 'urls_to_zip.zip')

  if not os.path.exists(filepath):
    return epoxy.throw_error(code=API_EXCEPTION_DOESNOTEXIST, error='Job does not seem to have any downloadable file associated').json()
  
  content_type = guess_type(filepath)
  wrapper = FileWrapper(file(filepath))
  response = HttpResponse(wrapper, content_type=content_type[0])
  response['Content-Length'] = os.path.getsize(filepath)
  response['Content-Disposition'] = 'attachment; filename=%s--%s[zup].zip' % (j.slug, j.date_created.strftime('%Y-%m-%d--%H-%M-%S'))
  return response
