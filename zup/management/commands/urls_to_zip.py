#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, csv
from optparse import make_option
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from zup.utils import gooseapi, unicode_dict_reader


class Command(BaseCommand):
    '''
    usage type
    

    '''
    args = '<csv absolute path>'
    help = 'From a list of urls (one per line) get the title and the plaintext content.'
    option_list = BaseCommand.option_list + (
        make_option('--tsv',
            action='store',
            dest='tsv',
            type='string',
            default=None,
            help='tsv file for the list. Header "urls" has to be provided')
    )

    def handle(self, *args, **options):
        # set default owner if ldap is not
        self.stdout.write("\n                      *     .--.\n                           / /  `\n          +               | |\n                 '         \\ \\__,\n             *          +   '--'  *\n                 +   /\\\n    +              .'  '.   *\n           *      /======\\      +\n                 ;:.  _   ;\n                 |:. (_)  |\n                 |:.  _   |\n       +         |:. (_)  |          *\n                 ;:.      ;\n               .' \:.    /  `.\n              / .-'':._.'`-. \\\n              |/    /||\\    \\|\n        jgs _..--\"\"\"````\"\"\"--.._\n      _.-'``                    ``'-._\n    -'                                '-\n\n")
        
        if not options['tsv']:
          self.stderr.write("    csv file must be specified")
          return

        self.stdout.write("    opening file: '%s'" % options['csv'])
        

        
        # owner will be used as default owner; you can change it later
        try:
          owner = User.objects.get(username=options['owner'])
        except User.DoesNotExist, e:
          self.stderr.write("    user %s not found" % options['owner'])
          return
        
        self.stdout.write("    using owner: <user:%s>\n\n" % owner.username)

        f = open(options['tsv'], 'rb')
        d = unicode_dict_reader(f, delimiter='\t')


        # check fields
        for i,row in enumerate(d):
          print row
          self.stdout.write("    done!")
          
          g = gooseapi("http://www.nytimes.com/2014/07/07/us/mayor-mike-duggans-pledges-echo-in-detroits-north-end.html?hp&action=click&pgtype=Homepage&version=LargeMediaHeadlineSum&module=photo-spot-region&region=photo-spot&WT.nav=photo-spot&_r=0")

          print g.title

          print "----"

          print g.cleaned_text
          url = row['urls']


        self.stdout.write("    done!")
        self.stdout.write('''

                      +
       +                            *
              
                   *          


            _..--"""````"""--.._
      _.-'``                    ``'-._
    -'                                '-

        ''')
          

    
        


