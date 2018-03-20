'''
Created on 20 mars 2018

@author: christophemorisset
'''

import subprocess
from shutil import copy2
from .utils import fill_from_file, write_cols

fort1_str = """MODEL DESIGNATION:                                           [NAME]
{0[NAME]}
CONTINUOUS STAR FORMATION (>0) OR FIXED MASS (<=0):          [ISF]
{0[ISF]}
TOTAL STELLAR MASS [1E6 M_SOL] IF 'FIXED MASS' IS CHOSEN:    [TOMA]
{0[TOMA]}
SFR [SOLAR MASSES PER YEAR] IF 'CONT. SF' IS CHOSEN:         [SFR]
{0[SFR]}
NUMBER OF INTERVALS FOR THE IMF (KROUPA=2):                  [NINTERV]
{0[NINTERV]}
IMF EXPONENTS (KROUPA=1.3,2.3):                              [XPONENT]
{0[XPONENT][0]},{0[XPONENT][1]}
MASS BOUNDARIES FOR IMF (KROUPA=0.1,0.5,100) [SOLAR MASSES]: [XMASLIM]
{0[XMASLIM][0]},{0[XMASLIM][1]},{0[XMASLIM][2]}
SUPERNOVA CUT-OFF MASS [SOLAR MASSES]:                       [SNCUT]
{0[SNCUT]}
BLACK HOLE CUT-OFF MASS [SOLAR MASSES]:                      [BHCUT]
{0[BHCUT]}
METALLICITY + TRACKS:                                        [IZ]
GENEVA STD: 11=0.001;  12=0.004; 13=0.008; 14=0.020; 15=0.040
GENEVA HIGH:21=0.001;  22=0.004; 23=0.008; 24=0.020; 25=0.040
PADOVA STD: 31=0.0004; 32=0.004; 33=0.008; 34=0.020; 35=0.050
PADOVA AGB: 41=0.0004; 42=0.004; 43=0.008; 44=0.020; 45=0.050
GENEVA V00: 51=0.001;  52=0.002; 53=0.008; 54=0.014; 55=0.040
GENEVA v40: 61=0.001;  62=0.002; 63=0.008; 64=0.014; 65=0.040
{0[IZ]}
WIND MODEL (0: MAEDER; 1: EMP.; 2: THEOR.; 3: ELSON):        [IWIND]
{0[IWIND]}
INITIAL TIME [1.E6 YEARS]:                                   [TIME1]
{0[TIME1]}
TIME SCALE: LINEAR (=0) OR LOGARITHMIC (=1)                  [JTIME]
{0[JTIME]}
TIME STEP [1.e6 YEARS] (ONLY USED IF JTIME=0):               [TBIV]  
{0[TBIV]}
NUMBER OF STEPS        (ONLY USED IF JTIME=1):               [ITBIV]
{0[ITBIV]}
LAST GRID POINT [1.e6 YEARS]:                                [TMAX]
{0[TMAX]}
SMALL (=0) OR LARGE (=1) MASS GRID; 
ISOCHRONE ON  LARGE GRID (=2) OR FULL ISOCHRONE (=3):        [JMG]
{0[JMG]}
LMIN, LMAX (ALL=0):                                          [LMIN,LMAX]
{0[LMIN]}
TIME STEP FOR PRINTING OUT THE SYNTHETIC SPECTRA [1.e6YR]:   [TDEL]
{0[TDEL]}
ATMOSPHERE: 1=PLA, 2=LEJ, 3=LEJ+SCH, 4=LEJ+SMI, 5=PAU+SMI:   [IATMOS]
{0[IATMOS]}
METALLICITY OF THE HIGH RESOLUTION MODELS                    [ILIB]
(1=0.001, 2= 0.008, 3=0.020, 4=0.040):
{0[ILIB]}
LIBRARY FOR THE UV LINE SPECTRUM: (1=SOLAR, 2=LMC/SMC)       [ILINE]
{0[ILINE]}
RSG FEATURE: MICROTURB. VEL (1-6), SOL/NON-SOL ABUND (0,1)   [IVT,IRSG]
{0[IVT]},{0[IRSG]}
OUTPUT FILES (NO<0, YES>=0)                                  [IO1,...]
{0[IO1]},{0[IO2]},{0[IO3]},{0[IO4]},{0[IO5]},{0[IO6]},{0[IO7]},{0[IO8]},{0[IO9]},{0[IO10]},{0[IO11]},{0[IO12]},{0[IO13]},{0[IO14]},{0[IO15]}
******************************************************************
  OUTPUT FILES:         1    SYNTHESIS.QUANTA
                        2    SYNTHESIS.SNR
                        3    SYNTHESIS.HRD
                        4    SYNTHESIS.POWER
                        5    SYNTHESIS.SP
                        6    SYNTHESIS.YIELDS
                        7    SYNTHESIS.SPECTRUM
                        8    SYNTHESIS.LINE
                        9    SYNTHESIS.COLOR
                       10    SYNTHESIS.WIDTH
                       11    SYNTHESIS.FEATURES
                       12    SYNTHESIS.OVI
                       13    SYNTHESIS.HIRES
                       14    SYNTHESIS.WRLINES
                       15    SYNTHESIS.IFASPEC
"""

fort1_dic = {'NAME': 'test1',
             'ISF': -1,
             'TOMA': 1.0,
             'SFR': 1.0,
             'NINTERV': 2,
             'XPONENT': (1.3, 2.3),
             'XMASLIM': (0.1, 0.5, 100),
             'SNCUT': 8.0,
             'BHCUT': 120.,
             'IZ': 25,
             'IWIND': 0,
             'TIME1': 0.01,
             'JTIME': 0,
             'TBIV': 0.1,
             'ITBIV': 100,
             'TMAX': 5.2,
             'JMG': 3,
             'LMIN': 0,
             'TDEL': 1.0,
             'IATMOS': 5,
             'ILIB': 4,
             'ILINE': 1,
             'IVT': 3,
             'IRSG': 0,
             'IO1': 1,
             'IO2': 1,
             'IO3': 1,
             'IO4': 1,
             'IO5': 1,
             'IO6': 1,
             'IO7': 1,
             'IO8': 1,
             'IO9': 1,
             'IO10': 1,
             'IO11': 1,
             'IO12': -1,
             'IO13': -1,
             'IO14': 1,
             'IO15': -1,
             }

class pyStb99(object):
    
    def __init__(self, name):
        
        self.fort1_str = fort1_str
        self.fort1_dic = fort1_dic
        self.set_value('NAME', name)
        self.stb_dir = '/Users/christophemorisset/TOOLS/Starburst99/Stb99_V7.0.1'
    
    def set_value(self, key, value):
        
        if key in self.fort1_dic:
            self.fort1_dic[key] = value
            
    def print_fort1(self):
        
        with open('{}/fort.1'.format(self.stb_dir), 'w') as f:
            f.write(self.fort1_str.format(self.fort1_dic))

    def run_stb99(self):
        to_run = 'cd {}; ./galaxy'.format(self.stb_dir)
        print('RUNNING {}'.format(to_run))
        stdin = None
        stdout = subprocess.PIPE
        proc = subprocess.Popen(to_run, shell=True, stdout=stdout, stdin=stdin)
        proc.communicate()

    def stb99_cloudy(self):
        
        copy2('{}/fort.92'.format(self.stb_dir), '{}.stb99'.format(self.fort1_dic['NAME']))
        try:
            to_run = "echo 'compile star \"{}.stb99\"' | cloudy.exe".format(self.fort1_dic['NAME'])
            print('RUNNING {}'.format(to_run))
            stdin = None
            stdout = subprocess.PIPE
            proc = subprocess.Popen(to_run, shell=True, stdout=stdout, stdin=stdin)
            proc.communicate()
        except:
            raise NameError('Problem in generating cloudy .stb99 file')
    
def merge_files(files, tab_metals, outfile):
    """
    Be sure that files and tab_metals are coherent
    """
    n_metal = len(tab_metals)
    #reading the ages and lambdas tables from the 1rst ascii file
    with open('{0}.ascii'.format(files[0])) as f1:
        for i in range(4):
            foo = f1.readline()
        # numer of ages in the ascii files
        n_ages = int(f1.readline())
        # number of lambdas
        n_lam = int(f1.readline())
        for i in range(4):
            foo = f1.readline()
        tab_ages = fill_from_file(n_ages, f1)
        tab_lambdas = fill_from_file(n_lam, f1)
    
    with open(outfile, 'w') as fout:
        fout.write('  20060612\n')
        fout.write('  2\n')
        fout.write('  2\n')
        fout.write('  Age\n')
        fout.write('  Metal\n')
        fout.write('  {0}\n'.format(n_ages*n_metal))
        fout.write('  {0}\n'.format(n_lam))
        fout.write('  lambda\n')
        fout.write('  1.00000000e+00\n')
        fout.write('  F_lambda\n')
        fout.write('  1.00000000e+00\n')
        
        #writing the ages and metallicities
        for metal in tab_metals:
            for age in tab_ages:
                fout.write('{0} {1}\n'.format(age, metal))
        #writing the lambdas
        write_cols(tab_lambdas, 5, fout)
        for fil in files:
            f1 = open('{0}.ascii'.format(fil))
            for i in range(10):
                foo = f1.readline()
            tab_ages = fill_from_file(n_ages, f1)
            tab_lambdas = fill_from_file(n_lam, f1)
            #reading and writing the fluxes from the different files
            tab_flux = fill_from_file(n_lam * n_ages, f1)
            write_cols(tab_flux, 5, fout)
    

if __name__ == '__main__':
    pass