#!/usr/bin/env python
# D. Jones - 5/6/24
# Attempt at a simple pipeline for running
# the various PyPEIT data reduction steps
# on GNIRS SN Ia data

import numpy as np
import argparse
import os
import subprocess
import astropy.table as at
from astropy.io import fits
import glob

def run(cmd):
    print('running')
    print(cmd)
    os.system(cmd)


class Py_DEIMOS:
    def __init__(self):
        pass

    def add_args(self, parser=None, usage=None):

        parser = argparse.ArgumentParser(
            usage=usage, conflict_handler="resolve")

        parser.add_argument(
            '--rawdatadir', type=str, default='/Users/david/research2/EB/2024A/rawdata_240728/lev0',
            help='folder containing the raw data')
        parser.add_argument(
            'objname', type=str, default=None,
            help='name of your object (used for output filenames only)')
        parser.add_argument(
            '-s','--std_star_mag', type=float, default=6.292,
            help='magnitude of the A0 standard star')
        parser.add_argument(
            '--ex_value', type=str, default='BOX',
            help='type of extraction -- OPT or BOX (sometimes OPT fails)')
        parser.add_argument(
            '--pypeitdatadir', type=str, default='/Users/david/research2/EB/DEIMOS/deimos.20240728',
            help='dir to put raw data specific to one object')
        parser.add_argument(
            '--pypeitworkdir', type=str, default='/Users/david/research2/EB/DEIMOS/red_deimos.20240728',
            help='working directory')
        parser.add_argument(
            '--mskname', type=str, default='Long1.0B',
            help='working directory')

        return parser

    def pypeit_setup(self):

        
        cmd = f"pypeit_setup -r {os.path.abspath(self.options.pypeitdatadir)}/{self.options.objname} -s keck_deimos -c A"
        print('running pypeit_setup')
        print(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stderr = stderr.decode('utf-8').split('\n')

        calib_file,pypeit_file = None,None
        for line in stderr:
            if 'Calibration association file' in line:
                calib_file = line.split()[-1]
            if 'PypeIt input file' in line:
                pypeit_file = line.split()[-1]

        
        if calib_file is None or pypeit_file is None:
            raise RuntimeError('something went wrong!')
        return calib_file,pypeit_file


    def run_pypeit(self,pypeitfile):

        cmd = f"run_pypeit {pypeitfile} -o"
        run(cmd)
        

    def copy_data(self):

        # make directories
        if not os.path.exists(self.options.pypeitdatadir):
            os.mkdir(self.options.pypeitdatadir)
        if not os.path.exists(f"{self.options.pypeitdatadir}/{self.options.objname}"):
            os.mkdir(f"{self.options.pypeitdatadir}/{self.options.objname}")
        if not os.path.exists(self.options.pypeitworkdir):
            os.mkdir(self.options.pypeitworkdir)
        if not os.path.exists(f"{self.options.pypeitworkdir}/{self.options.objname}"):
            os.mkdir(f"{self.options.pypeitworkdir}/{self.options.objname}")

        
        files = glob.glob(f"{self.options.rawdatadir}/*fits")
        import pdb; pdb.set_trace()
        for f in files:
            header = fits.getheader(f)
            print(header['SLMSKNAM'])
            if not self.options.mskname:
                if header['OBJECT'] == self.options.objname or header['SLMSKNAM'] == self.options.objname:
                    os.system(f"cp {f} {self.options.pypeitdatadir}/{self.options.objname}/")
            else:
                if header['OBJECT'] == self.options.objname or header['SLMSKNAM'] == self.options.mskname:
                    os.system(f"cp {f} {self.options.pypeitdatadir}/{self.options.objname}/")
                    
        return
                
    def main(self):
        # copy all the raw data into a folder
        self.copy_data()
        os.chdir(f'{self.options.pypeitworkdir}/{self.options.objname}/')
        
        # pypeit_setup
        calib_file,pypeit_file = self.pypeit_setup()

        # run_pypeit
        #self.run_pypeit(pypeit_file)
        
        # fluxing
        #self.pypeit_sensfunc()
        #self.pypeit_fluxing()
        
        # coadd
        #self.coadd1d()
        
        # telluric
        #self.pypeit_tellfit()

if __name__ == "__main__":

    pg = Py_DEIMOS()
    parser = pg.add_args()
    args = parser.parse_args()
    pg.options = args

    pg.main()
