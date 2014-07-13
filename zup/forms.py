from django import forms
from zup.models import Job, Url


class JobForm(forms.ModelForm):
  url_list = forms.CharField()

  def clean_url_list(self):
    urls = filter(None, self.cleaned_data['url_list'].split('\n'))
    return urls

  class Meta:
    model = Job
    fields = ['name', 'url_list']