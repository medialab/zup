import os
from django.conf import settings
from django.test import TestCase
from utils import urls_to_zip

class UtilsTest(TestCase):
  def setUp(self):
    '''
    it will create TMP_ROOT and MEDIA_ROOT
    '''
    if not os.path.exists(settings.TMP_ROOT):
      os.mkdir(settings.TMP_ROOT)
    if not os.path.exists(settings.MEDIA_ROOT):
      os.mkdir(settings.MEDIA_ROOT)

  def test_urls_to_zip(self):
    zipified = urls_to_zip([
      "http://www.nytimes.com/2014/07/07/us/mayor-mike-duggans-pledges-echo-in-detroits-north-end.html?hp&action=click&pgtype=Homepage&version=LargeMediaHeadlineSum&module=photo-spot-region&region=photo-spot&WT.nav=photo-spot&_r=0",
      "http://www.nytimes.com/2014/07/08/world/europe/eduard-shevardnadze-soviet-foreign-minister-under-gorbachev-is-dead-at-86.html?rref=homepage&module=Ribbon&version=origin&region=Header&action=click&contentCollection=Home%20Page&pgtype=article"
    ])
    if os.path.exists(zipified):
      os.remove(zipified)