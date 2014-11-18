import os, logging
from django.conf import settings
from django.test import TestCase
from utils import urls_to_zip



logger = logging.getLogger('zup')




class LoggerTest(TestCase):
  def setUp(self):
    '''
    it will create LOGGING_ROOT
    '''
    if not os.path.exists(settings.LOGGING_ROOT):
      os.mkdir(settings.LOGGING_ROOT)


  def test_check_permissions(selft):
    '''
    verify that logger has the right to write to logger folder...
    '''
    logger.debug('logger test is working as expected')
    


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
      "http://www.nytimes.com/2014/07/08/world/europe/eduard-shevardnadze-soviet-foreign-minister-under-gorbachev-is-dead-at-86.html?rref=homepage&module=Ribbon&version=origin&region=Header&action=click&contentCollection=Home%20Page&pgtype=article",
      "http://www.corriere.it/cronache/14_luglio_07/estate-ritirata-piogge-temporali-8e993fc8-0607-11e4-9ae2-2d514cff7f8f.shtml",
      "http://www.theguardian.com/news/datablog/2014/jul/07/which-phones-battery-life-stop-boarding-flight",
      "http://www.corrieredellosport.it/calcio/mondiali_2014/2014/07/11-368890/Roma%2C+visite+mediche+per+Emanuelson",
      "http://gasexchange.com/questions/do-labor-epidurals-increase-the-risk-of-instrumental-or-surgical-delivery/",
      "http://ghsm.hms.harvard.edu/uploads/pdf/PGSSC_Publications_2012.pdf",
      "http://guidance.nice.org.uk/CG/Published",
      "http://volunteermovement.org/ehsen-amri-activism-in-tunisia/"
    ])
    self.assertEquals
    if os.path.exists(zipified):
      os.remove(zipified)