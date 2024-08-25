#!/usr/bin/env python
# D. Jones - 7/13/24

import sys
import io
import os
from pykoa.koa import Koa 
from astropy.table import Table,Column

class pyKOA:

    def add_args(self,parser=None, usage=None):
        if parser == None:
            parser = argparse.ArgumentParser(usage=usage, conflict_handler="resolve")

        parser.add_argument('start_date', type=str, default=None,
                            help='start date.  format YYYY-MM-DD')
        parser.add_argument('end_date', type=str, default=None,
                            help='end date')
        parser.add_argument('--outdir', type=str, default='rawdata',
                            help='output directory')
        parser.add_argument('--nologin', default=False, action="store_true",
                            help='assume already logged in')

        
    def main(self):

        if not self.options.nologin:
            Koa.login ('./tapcookie.txt')

        Koa.query_datetime (
            'deimos', \
            f'{start_date} 00:00:00/{end_date} 23:59:59', \
            './rawdata/DEIMOS_login.tbl', overwrite=True, format='ipac', \
            cookiepath='./tapcookie.txt' )

        rec = Table.read ('./rawdata/DEIMOS_login.tbl',format='ipac')
        print (rec)

        if not os.path.exists(self.options.outdir):
            os.makedirs(self.options.outdir)
        
        Koa.download (
            './rawdata/DEIMOS_login.tbl',
            'ipac',
            self.options.outdir,
            cookiepath='./tapcookie.txt')

    
if __name__ == "__main__":
    pk = pyKOA()
    parser = pk.add_args()
    args = parser.parse_args()
    pk.options = args

    pk.main()
