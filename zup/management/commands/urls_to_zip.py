#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, csv
from optparse import make_option
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from zup.utils import urls_to_zip, unicode_dict_reader


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
            help='tsv file for the list. Header "urls" has to be provided'),
    )

    def handle(self, *args, **options):
        # set default owner if ldap is not
        self.stdout.write("\n                      *     .--.\n                           / /  `\n          +               | |\n                 '         \\ \\__,\n             *          +   '--'  *\n                 +   /\\\n    +              .'  '.   *\n           *      /======\\      +\n                 ;:.  _   ;\n                 |:. (_)  |\n                 |:.  _   |\n       +         |:. (_)  |          *\n                 ;:.      ;\n               .' \:.    /  `.\n              / .-'':._.'`-. \\\n              |/    /||\\    \\|\n        jgs _..--\"\"\"````\"\"\"--.._\n      _.-'``                    ``'-._\n    -'                                '-\n\n")
        
        if not options['tsv']:
          self.stderr.write("    csv file must be specified")
          return

        self.stdout.write("    opening file: '%s'" % options['tsv'])
        
        f = open(options['tsv'], 'rb')
        d = unicode_dict_reader(f, delimiter='\t')


        # check fields
        urls = [row['urls'] for i,row in enumerate(d)]

        urls_to_zip(urls=urls)


        self.stdout.write("    done!")
        self.stdout.write('''

                      +
       +                            *
              
                   *          


            _..--"""````"""--.._
      _.-'``                    ``'-._
    -'                                '-

        ''')
          

    
        


