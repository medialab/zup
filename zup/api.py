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
      # Cfr forms.py clened data is here a list of (not yet) valid url
      
      for url in form.cleaned_data['url_list']:
        u = Url(url=url)
        u.save()
        job.urls.add(u)

    job.start(cmd='urls_to_zip')
    epoxy.item(job)

  return epoxy.json()