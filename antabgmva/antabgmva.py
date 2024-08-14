"""
AntabGMVA.py - a tool for managing GMVA metadata.

Author  : Daewon Kim (MPIfR)

Contact : dwkimastro@gmail.com

Version : 24.813

"""
import numpy as np
import matplotlib.pyplot as plt
import copy
from scipy.interpolate import interp1d
from random import randrange, uniform
import time
import logging
import os
import shutil
import warnings
warnings.filterwarnings("ignore")
import matplotlib
from os import listdir
from os.path import isfile, join
matplotlib.rcParams.update({'legend.borderaxespad': 0.3})
matplotlib.rcParams.update({'legend.fontsize': 9.5})
matplotlib.rcParams.update({'legend.framealpha': 0.5})



def genlog():
   '''
   Generating an initial log file.
   
   e.g., logger = genlog()
   
   output: Find a log file in the working directory.
   
   '''
   i = 0
   logname = input("\n###################################\n###################################\nLog file name \n: ")
   logfile = logname+"_"+str(i)+"_LOG"+".txt"
   if logfile in os.listdir():
      print("\nThe file name exists! ..add a higher number to it")
      for j in range(100):
         i=i+1
         logfile = logname+"_"+str(i)+"_LOG"+".txt"
         if logfile in os.listdir():
            continue
         else:
            break

   print('\n-->', logfile)
   Logform = "%(asctime)s :: %(message)s"
   logging.basicConfig(filename = os.getcwd()+"/"+logfile, level = logging.INFO, format = Logform)
   logger = logging.getLogger()
   return logger



def log(*args, logtype='info', sep=' '):
    getattr(logger, logtype)(sep.join(str(a) for a in args))
    print(*args)



def newlog():
   '''
   Generating a new log file.
   
   e.g., logger = newlog()

   output: Find a new log file in the working directory.
   
   '''
   global logger    #% update this variable with new one (essential)
   logger.handlers[0].stream.close()
   logger.removeHandler(logger.handlers[0])
   del(logger)

   i = 0
   global logname    #% by doing so, now you can define this Param. with new one
   logname = input("\n###################################\n###################################\nLog file name \n: ")
   logfile = logname+"_"+str(i)+"_LOG"+".txt"
   if logfile in os.listdir():
      log("The file name exists! ..add higher number to the end")
      for j in range(100):
         i=i+1
         logfile = logname+"_"+str(i)+"_LOG"+".txt"
         if logfile in os.listdir():
            continue
         else:
            break
   print(logfile)
   Logform = "%(asctime)s :: %(message)s"
   logging.basicConfig(filename = os.getcwd()+"/"+logfile, level = logging.INFO, format = Logform)
   logger = logging.getLogger()
   return logger



def writetxt(data, outname):
   """
   Saving data-array as a text file.

   e.g., writetxt(self.tsys#, 'file name')
   
   output: An output text file.
   
   """
   outn = outname
   with open(outn, 'w') as ft6842:
      ft6842.writelines(data)



def allinone():
   """
   Merge all processed ANTAB files into one single Antab file.
   Run it in the 'allinone' folder that the function 'sout' will create.
   Only final versions of your ANTAB files should be present in the folder.

   e.g., allinone()

   output: A single antab file.
   
   """
   log("\n!! - In the 'allinone' folder with only the Final Products - !!")
   prefx = input("\nGive a prefix of the output filename (e.g., 'c211ab', 'c222abcd', 'c221abc') \n: ")
   frefx = input("\nArray name + Observing wavelength (e.g., 'GMVA3mm') \n: ")
   big1 = []   # Gain
   big2 = []   # Tsys
   arg = []
   log(" ")
   for i in listdir():
      arg.append(i)
      log(i)
   log("-----------------------------------------------------\
   \n-> Merge all the above data into one single text file"); time.sleep(0.5)
   for j in arg:
      v1 = open(j)
      v2 = v1.readlines()
      if v2[-1] == '/':
         v2[-1] = '/\n'
      else:
         pass
      big1 = big1 + v2[:1]
      big2 = big2 + v2[1:]
   big3 = big1 + big2
   outn = "ALLINONE_" + prefx + "_" + frefx + ".antab"
   log("\n\n... {} ! \n".format(outn))
   with open(outn, 'w') as ft54:
      ft54.writelines(big3)
   log("\n**DONE** \n..check an output file \
   \n////////////////////////////////////////////////////////////////////////////////")



def linkses(fromnthline=2):
   """
   Merge ANTAB files from consecutive sessions for a single antenna.
   You will be asked to select antab files to be connected.

   <Params>
    fromnthline : First N lines to be skipped.
                  For ANTAB, should be 2 -> Tsys/Gain (default).
                  For WX (weather) data, change it to 1.
                  --> one single line for WX; i.e., 'WEATHER XX /'

   e.g., linkses()

   output: A combined, single ANTAB/WX file for one station.
   
   """
   for i in listdir():
      if os.path.isfile(i):
         log(i)
   files = input("============================== \
   \n\nGive multi-session files of ONE ANTENNA in time order --> alphabetic!) \
   \n(e.g., c211aef.antabfs c211bef.antabfs c211cef.antabfs) \n: ")
   files = files.split()
   l1 = open(files[0])
   l2 = l1.readlines()
   l3 = l2[:-1]
   for j in files[1:]:
      k1 = open(j)
      k2 = k1.readlines()
      k3 = k2[fromnthline:-1]
      l3 = l3 + k3
   l3.append("/\n")
   nm1 = input("\nGive Session codes (e.g., abc, if a/b/c sessions are used) \n: ")
   nm2 = input("\nGive Antenna code (e.g., EF, if it is the Effelsberg station) \n: ")
   nm3 = input("\nObserving frequency? (e.g., 3mm) \n: ")
   outn = nm1+'_'+nm3+"_"+nm2+"_link.dat"
   log("\n\n... {} ! \n".format(outn))
   with open(outn, 'w') as p48:
      p48.writelines(l3)
   log("\n**DONE** \n..check an output file \
   \n////////////////////////////////////////////////////////////////////////////////")



def sout(station, tsysid):
   """
   To sort out the results (i.e., data and figure files with Tsys#).
   It will create a folder for the given station. If there isn't,
   the 'allinone' folder will also be created for merging later.
   The output files are either ~.dat or ~.png. The .dat file with tsysid
   will be copied to the allinone folder and all the others will be moved
   to the station folder.

   <Params>
    station : Station name code (str) for output files (e.g., 'KT').
    tsysid  : Version number of a final Tsys#.dat (int) to be used in AIPS/CASA.

   e.g., sout('KT', 1)

   """
   log("\n------------------------sorting out...")
   aio = 0
   for i in listdir():
      if os.path.isdir(i):
         if i == 'allinone':
            aio = 1
            break
   if aio == 1:
      pass
   else:
      os.mkdir('allinone')
   ###
   sta = 0
   for i in listdir():
      if os.path.isdir(i):
         if i == station.lower():
            sta = 1
            break
   if sta == 1:
      pass
   else:
      os.mkdir(station.lower())
   ###
   thenum = str(tsysid)
   JIC = []
   for i in listdir():
      if os.path.isfile(i):
         if (station.upper() in i) & ('Tsys'+thenum in i) & ('.dat' in i):
            JIC.append(i)
         elif (station.lower() in i) & ('Tsys'+thenum in i) & ('.dat' in i):
            JIC.append(i)
   if len(JIC) == 0:
      log("\nNo data found...")
      return
   elif len(JIC) == 1:
      shutil.copy(JIC[0], 'allinone')
      pass
   else:
      for o,oo in enumerate(JIC, 1):
         print(o,':',oo)
      Neo = input("\n.....Multiple .dat files found! \nGive an Index number of the correct one (see above) \n: ")
      Neo = JIC[int(Neo)-1]
      shutil.copy(Neo, 'allinone')
   for i in listdir():
      if os.path.isfile(i):
         if (station.upper() in i) & ('Tsys' in i):
            shutil.move(i, station.lower())
         elif (station.lower() in i) & ('Tsys' in i):
            shutil.move(i, station.lower())
   log("\n**DONE** \nThe output files has been sorted out! \
   \n////////////////////////////////////////////////////////////////////////////////")



def doublecheck(inputdat=None, fonttit=12, fontaxlab=13, fontleg=11, fontticklab=11):
   """
   Create a plot of input Tsys data. Here the input data can be either
   data in processing (i.e., [self.tsys#,self.colids]) or an external file.
   Here the external file should be the ones generated by this program
   and not raw antab files. This function is basically for double-checking
   the processed datasets to be sure if everything is fine and as expected. 

   <Params>
    inputdat    : Input Tsys data (internal or external; see examples below).
    fonttit     : Fontsize of Figure Title 
    fontaxlab   : Fontsize of Figure Axis labels
    fontleg     : Fontsize of Figure Legend
    fontticklab : Fontsize of Figure Axis-tick labels

   e.g., internal (self.tsys#)     : doublecheck([self.tsys#, self.colids])
   e.g., external ('~~_Tsys#.dat') : doublecheck()

   output: A plot window will show up (no output data).

   """
   if inputdat:
      da2 = inputdat[0]
      da3 = inputdat[1]
      da3 = da3.split()
      A0 = None
      Z0 = None
      A1 = 0
      Z1 = 0
   else:
      log("\nInput data from an external text file.")
      for i in listdir():
         if os.path.isfile(i):
            log(i)
      filego = input("\nWhich output antab file need to be double-checked? \n:")
      da1 = open(filego)
      da2 = da1.readlines()
      if 'INDEX' in da2[1]:
         for j,k in enumerate(da2[1].split(), 0):
            if k.startswith('I'):
               p1 = da2[1].split()[j:-1]
               p2 = ''.join(p1)
               break
         da3 = p2.split('=')[1].split(',')
         da3 = np.asarray([m[1:-1] for m in da3])
      else:
         da3 = input("\nNo INDEX line found. Insert it here (e.g., R1 R2 L1 L2) \n: ")
         da3 = da3.split()
      A0 = 2
      Z0 = -1
      A1 = 2
      Z1 = 1
   antcode = input("\nAntenna code? (e.g., EF: Effelsberg) \n:")
   #
   simpletest = da2[2].split()[1]
   new_t = []
   if simpletest.count(":") == 2:
      for l in da2[A0:Z0]:
         tem_d = l.split()[0]        #% day array
         tem_hms = l.split()[1]       #% hh:mm:ss array
         #% converting all of them to a day with decimal numbers
         div_h = tem_hms.split(':')[0]
         div_m = tem_hms.split(':')[1]
         div_s = tem_hms.split(':')[2]
         dayform = (int(div_h)/24.) + (float(div_m)/60. /24.) + (float(div_s)/60. /60. /24.) + int(tem_d)
         new_t.append(dayform)
   elif simpletest.count(":") == 1:
      for l in da2[A0:Z0]:
         tem_d = l.split()[0]        #% day array
         tem_hm = l.split()[1]       #% hh:mm array
         div_h = tem_hm.split(':')[0]
         div_m = tem_hm.split(':')[1]
         dayform = (int(div_h)/24.) + (float(div_m)/60. /24.) + int(tem_d)
         new_t.append(dayform)
         #% --> actual x-array for interpolation
   new_t = np.asarray(new_t)
   if len(da3) > 8:
      Hor, Ver = 14.5, 10.5
   elif len(da3) == 8:
      Hor, Ver = 13, 10
   elif len(da3) in [7,6,5]:
      Hor, Ver = 10.5, 8.5
   elif len(da3) in [4,3]:
      Hor, Ver = 9, 7
   elif len(da3) in [2,1]:
      Hor, Ver = 7, 8
   # figure id set
   for D in range(1000):
      figid = randrange(0, 1000)
      if plt.fignum_exists(figid):
         del figid
         continue
      else:
         break
   fig_pol=plt.figure(figid, figsize=(Hor, Ver))
   plt.figure(figid)
   plt.rcParams['legend.frameon'] = 'False'
   plt.rcParams['xtick.labelsize'] = 11
   plt.rcParams['ytick.labelsize'] = 11
   for i,j in enumerate(da3,0):
      if len(da3) > 8:
         plt.subplot(4, 4, i+1)
      elif len(da3) in [7,8]:
         plt.subplot(4, 2, i+1)
      elif len(da3) in [5,6]:
         plt.subplot(3, 2, i+1)
      elif len(da3) in [3,4]:
         plt.subplot(2, 2, i+1)
      elif len(da3) in [1,2]:
         plt.subplot(2, 1, i+1)
         #
      k2 = np.genfromtxt(da2, usecols=2+i, unpack=True, dtype=float, skip_header=A1, skip_footer=Z1)
      #
      if (j.startswith('R')) & ('L' not in j):
         ccc = '#1f77b4'
      elif (j.startswith('L')) & ('R' not in j):
         ccc = '#ff7f0e'
      else:
         ccc = 'tab:brown'
      plt.figure(figid)
      plt.plot(new_t, k2, markersize=2, marker='o', linewidth=0.8, label=j+"  *double checking*", color=ccc)
      plt.yticks(fontsize=fontticklab)
      plt.xticks(fontsize=fontticklab)
      plt.legend(loc=2, markerscale=1.4, fontsize=fontleg)
      #vax = int(np.round(max(k2)))
      #vin = int(np.round(min(k2)))
      vav = np.round(np.median(k2), 1)
      vst = np.round(np.std(k2), 1)
      opz1 = np.linspace(plt.ylim()[0], plt.ylim()[1], 7)
      thegap = np.abs(np.abs(opz1[-1])-np.abs(opz1[-2]))
      plt.ylim(opz1[0]-thegap*0.0, opz1[-1]+thegap*1.3)
      plt.title("*{}* - Median={}K, Std={}K".format(antcode,vav,vst), color='r', fontsize=fonttit)
      plt.xlabel("Decimal day", fontsize=fontaxlab)
      plt.ylabel("Tsys [K]", fontsize=fontaxlab)
      plt.minorticks_on()
      plt.tick_params(axis='both', which='major', length=5, direction='in', pad=2, color='k')
      plt.tick_params(axis='both', which='minor', length=3, direction='in', pad=2, color='k')
   plt.figure(figid); plt.tight_layout()
   # plt.show()
   # for 16 panels..
   # plt.subplots_adjust(left=0.045, bottom=0.050, right=0.975, top=0.965, wspace=0.190, hspace=0.345)
   log("\nNO DATA/FIGURE out. This task is just for double checking!")
   log("\n**DONE** \n..check output figure file(s) \
   \n////////////////////////////////////////////////////////////////////////////////")



###################################################################################
###################################################################################
logger = genlog()
plt.ion()
###################################################################################
###################################################################################



class gentab():
   """
   The main function package for ALL GMVA stations.
   For VLBA (i.e., ~~cal.vlba), process it first with the function `vlbaout`.
   Using the functions below, examine the data and create your final ANTAB file.

   <Sub-functions>
    readant  : Reading data in antab file.
    overview : Overview Tsys measurements.
    showsys  : Plot raw Tsys curve (textout available).
    intpsys  : Plot & interpolate Tsys measurements (textout available).
    smthsys  : Plot & smooth Tsys outliers (textout available).
    cpifsys  : Plot & copy-and-paste Good Tsys-IF to Bad Tsys-IF (textout available).

   e.g., ef = gentab('EF')

   output: self + (antcode, sepaPol, colnum, colids, sesn, bands, HDa, HDb)

   Products from gentab: .dat and .png files of a single ANTAB file.
   
   """
   def __init__(self, antcode):
      self.antcode = antcode
      self.bands = None
      self.sepaPol = None
      self.colnum = None
      self.colids = None
      self.sesn = None
      self.HDa = None
      self.HDb = None
      self.tsys1 = None    # raw
      self.tsys2 = None    # interpolated
      self.tsys3 = None    # smoothed
      self.tsys4 = None    # c&p
      self.inich = None
      self.tarr = None
      self.cpfrom = []
      self.cpto = []
      #self.logger = None
      log("\n###################################\n###################################\nFirst, you need to understand observing setting of your data!")
      log("\n***Open up the antab file you want to work on, and answer the questions below***")
      ost1 = input("\n________________________________________________________________________________\
      \nAntab files separated by RCP and LCP? (e.g., yes/y or no/n; default = no) \n: ")
      self.sepaPol = ost1
      if ost1 == '':
         self.sepaPol = 'no'
      ost2 = input("\n________________________________________________________________________________\
      \nHow many Tsys columns are there?  -->  including all RCP and LCP \n(e.g., 16 or 8 or 4 or 2;  ...  **NOTE** e.g., 'R1:n' or 'R1|L1' --> one column) \n: ")
      ost2 = int(ost2)
      self.colnum = ost2
      ost3 = input("\n________________________________________________________________________________\
      \nSelect a number below for the Tsys order(IDs)            [***Must-Be-Given***] \
      \n\n 1 - R1 R2 R3 R4 R5 R6 R7 R8 L1 L2 L3 L4 L5 L6 L7 L8 \
      \n 2 - R1:8 L1:8 \
      \n 3 - R1:2 L1:2 R3:4 L3:4 R5:6 L5:6 R7:8 L7:8 \
      \n 4 - R1 L1 R2 L2 R3 L3 R4 L4 \
      \n 5 - R1L1 R2L2 R3L3 R4L4 R5L5 R6L6 R7L7 R8L8  --> (e.g., ALMA) \
      \n 6 - Custom (manual input) \
      \n\n**For Single polarization  -->  either  R1 R2 ..  or  L1 L2 .. \
      \n**For Separated RCP/LCP    -->  R1 R2 .. L1 L2 .. \
      \n**Normally, RCP ('R') comes first \
      \n**Each Tsys column must begin with either 'R' or 'L' (uppercase) \n: ")
      if ost3 == '1':
         ost3 = 'R1 R2 R3 R4 R5 R6 R7 R8 L1 L2 L3 L4 L5 L6 L7 L8'
      elif ost3 == '2':
         ost3 = 'R1:8 L1:8'
      elif ost3 == '3':
         ost3 = 'R1:2 L1:2 R3:4 L3:4 R5:6 L5:6 R7:8 L7:8'
      elif ost3 == '4':
         ost3 = 'R1 L1 R2 L2 R3 L3 R4 L4'
      elif ost3 == '5':
         ost3 = 'R1L1 R2L2 R3L3 R4L4 R5L5 R6L6 R7L7 R8L8'
      elif ost3 == '6':
         ost3 = input("\nGive it like the examples above \n: ")
      self.colids = ost3
      ost4 = input("\n________________________________________________________________________________\
      \nGive session ID (e.g., a or b or c or d ...)   --> consider it as a prefix \n: ")
      self.sesn = ost4
      ost5 = input("\n________________________________________________________________________________\
      \nObserving frequency? (e.g., 3mm or 7mm or ...) \n: ")
      self.bands = ost5
      hd1 = input("\n________________________________________________________________________________\
      \nMake a GAIN line without POLY \n--> e.g., GAIN EF ELEV DPFU=0.XX,0.XX FREQ=xxxx \n--> FREQ can be omitted (optional) \
      \n                                          **Skip for now --> press Enter** \n: ")
      hd2 = input("\n________________________________________________________________________________\
      \nMake a POLY line \n--> e.g., POLY=0.5190,-0.0382429,,0.00510852 or POLY=1.0 \
      \n                                          **Skip for now --> press Enter** \n: ")
      hda = hd1 + ' ' + hd2 + ' /\n'
      hd3 = input("\n________________________________________________________________________________\
      \nMake a TSYS line without INDEX \n--> e.g., TSYS EF FT=1.0 TIMEOFF=0 \n--> FT and TIMEOFF can be omitted (optional) \
      \n                                          **Skip for now --> press Enter** \n: ")
      hd4 = input("\n________________________________________________________________________________\
      \nSelect a number below for the INDEX line \
      \n                                          **Skip for now --> press Enter** \
      \n 1 - INDEX='R1','R2','R3','R4','R5','R6','R7','R8','L1','L2','L3','L4','L5','L6','L7','L8' \
      \n 2 - INDEX='R1:8','L1:8' \
      \n 3 - INDEX='R1:2','L1:2','R3:4','L3:4','R5:6','L5:6','R7:8','L7:8' \
      \n 4 - INDEX='R1','L1','R2','L2','R3','L3','R4','L4' \
      \n 5 - INDEX='R1|L1','R2|L2','R3|L3','R4|L4','R5|L5','R6|L6','R7|L7','R8|L8' \
      \n 6 - Custom (manual input) \n\n: ")
      if hd4 == '1':
         hd4 = "INDEX='R1','R2','R3','R4','R5','R6','R7','R8','L1','L2','L3','L4','L5','L6','L7','L8'"
      elif hd4 == '2':
         hd4 = "INDEX='R1:8','L1:8'"
      elif hd4 == '3':
         hd4 = "INDEX='R1:2','L1:2','R3:4','L3:4','R5:6','L5:6','R7:8','L7:8'"
      elif hd4 == '4':
         hd4 = "INDEX='R1','L1','R2','L2','R3','L3','R4','L4'"
      elif hd4 == '5':
         hd4 = "INDEX='R1|L1','R2|L2','R3|L3','R4|L4','R5|L5','R6|L6','R7|L7','R8|L8'"
      elif hd4 == '6':
         hd4 = input("\nGive it like the examples above \n: ")
      hdb = hd3 + ' ' + hd4 + ' /\n'
      self.HDa = hda
      self.HDb = hdb
      #######
      log("\n\n===================================================================== \
      \nNOTICE: If you have made a wrong input among the above information, \
      \n        No worries, find it as below: e.g., self + parameter first, \
      \n        Then, re-define it as you wish (e.g., self.HDa = '~~~~~~'). \
      \n=====================================================================\n"); time.sleep(0.6)
      #######
      log("\n**DONE** \n..check self + antcode, sepaPol, colnum, colids, sesn, bands, HDa, HDb \
      \n////////////////////////////////////////////////////////////////////////////////")



   def readant(self):
      """
      Reading raw antab file to extract Tsys data.
      This function works for most of the GMVA antab formats.
      Confirmed stations: VLBA, GBT, KVN, ALMA, NOEMA, GLT,
                          Effelsberg (EF), 
                          Pico Veleta (PV), 
                          Onsala (ON), 
                          Metsahovi (MH), 
                          Yebes (YS).
      But, it should work with any ANTABs in the same format as above.

      e.g., self.readant()
      
      output: self.tsys1
      
      """
      if (self.sepaPol == 'yes') | (self.sepaPol == 'y') | (self.sepaPol == 'YES') | (self.sepaPol == 'Y') | (self.sepaPol == 'Yes'):
         log("\n!!! RCP and LCP are divided into separate Antab files !!!\n")
         for i in listdir():
            if os.path.isfile(i):
               log(i)
         rcpfil = input("\n________________________________________________________________________________\
         \nGive RCP antab file (e.g., c232a_Nn-rcp.asc; ..if None, just Enter) \n: ")
         lcpfil = input("\n________________________________________________________________________________\
         \nGive LCP antab file (e.g., c232a_Nn-lcp.asc; ..if None, just Enter) \n: ")
         colA = input("\n________________________________________________________________________________\
         \nDay (DD) column index? (i.e., normally 0 --> 1st column from left) \n: ")
         colB = input("\n________________________________________________________________________________\
         \nTime (HH:MM) column index? (i.e., normally 1 --> 2nd column from left) \n: ")
         colC = input("\n________________________________________________________________________________\
         \nTsys (K) column indices for both RCP & LCP? \
         \n(normally starts from 2; e.g., for single --> 2 / multiple --> 2,3,4,5) \n: ")
         SINGP = 0
         if len(colC) >= 2:
            colC = colC.split(',')
         log("\nCombined data column order --> 'R1 R2 .. L1 L2 ..' or 'R~ L~'  (i.e., RCP first!) \
         \nNOTE: this must be the same as self.colids (if different, modify self.colids!)"); time.sleep(3)
         if rcpfil == '':
            log("\nNo RCP data..."); time.sleep(2)
            SINGP = 1
         elif lcpfil == '':
            log("\nNo LCP data..."); time.sleep(2)
            SINGP = 2
         if SINGP == 0:
            log("\nBoth RCP & LCP found!"); time.sleep(1)
            rd1 = open(rcpfil)
            rd2 = rd1.readlines()
            rd11 = open(lcpfil)
            rd22 = rd11.readlines()
            rd3 = []
            for i,j in enumerate(rd2, 0):
               if len(j) >= 2:
                  if (j[0] == '!') | (j[0] == '/'):
                     continue
                  elif (j[0] == ' ') & (j[1].isdigit()):
                     TEMR = ''
                     TEML = ''
                     for z in colC:
                        TEMR = TEMR + ' ' + rd2[i].split()[int(z)]
                        TEML = TEML + ' ' + rd22[i].split()[int(z)]
                     TEMR = TEMR[1:]
                     TEML = TEML[1:]
                     rd3.append(rd2[i].split()[int(colA)] + ' ' + rd2[i].split()[int(colB)] + ' ' + TEMR + ' ' + TEML + ' \n')
                     continue
                  elif j[0].isdigit():
                     TEMR = ''
                     TEML = ''
                     for z in colC:
                        TEMR = TEMR + ' ' + rd2[i].split()[int(z)]
                        TEML = TEML + ' ' + rd22[i].split()[int(z)]
                     TEMR = TEMR[1:]
                     TEML = TEML[1:]
                     rd3.append(rd2[i].split()[int(colA)] + ' ' + rd2[i].split()[int(colB)] + ' ' + TEMR + ' ' + TEML + ' \n')
                     continue
         elif (SINGP == 1) | (SINGP == 2):
            log("\nOnly single Pol. present.."); time.sleep(1)
            if SINGP == 1:
               sn1 = open(lcpfil)
               sn2 = sn1.readlines()
            elif SINGP == 2:
               sn1 = open(rcpfil)
               sn2 = sn1.readlines()
            rd3 = []
            for i,j in enumerate(sn2, 0):
               if len(j) >= 2:
                  if (j[0] == '!') | (j[0] == '/'):
                     continue
                  elif (j[0] == ' ') & (j[1].isdigit()):
                     TEMP = ''
                     for z in colC:
                        TEMP = TEMP + ' ' + sn2[i].split()[int(z)]
                     TEMP = TEMP[1:]
                     rd3.append(sn2[i].split()[int(colA)] + ' ' + sn2[i].split()[int(colB)] + ' ' + TEMP + ' \n')
                     continue
                  elif j[0].isdigit():
                     TEMP = ''
                     for z in colC:
                        TEMP = TEMP + ' ' + sn2[i].split()[int(z)]
                     TEMP = TEMP[1:]
                     rd3.append(sn2[i].split()[int(colA)] + ' ' + sn2[i].split()[int(colB)] + ' ' + TEMP + ' \n')
                     continue
      else:
         for i in listdir():
            if os.path.isfile(i):
               log(i)
         rawfil = input("\nGive antab file (e.g., c232aef.antabfs or a_3mm_BR_vlbaout.antab) \n: ")
         rd1 = open(rawfil)
         rd2 = rd1.readlines()
         rd3 = []
         for j in rd2:
            if len(j) >= 2:
               if j[0].isdigit():
                  if '!' in j:
                     for u,uu in enumerate(j.split()):
                        if uu == '!':
                           cutline = u
                     mdform = ' '.join(j.split()[:cutline]) + ' \n'
                  else:
                     mdform = ' '.join(j.split()) + ' \n'
                  rd3.append(mdform)
                  continue
               elif (j[0] == ' ') & (j[1].isdigit()):
                  if '!' in j:
                     for u,uu in enumerate(j.split()):
                        if uu == '!':
                           cutline = u
                     mdform = ' '.join(j.split()[:cutline]) + ' \n'
                  else:
                     mdform = ' '.join(j.split()) + ' \n'
                  rd3.append(mdform)
                  continue
               else:
                  continue
         for k in rd3:
            if len(k.split()) <= 3:
               log("\n!!! There is something wrong with this data; this can happen with **GLT** \
               \n    (either several time bins with no Tsys data --and/or-- single Tsys column)")
               mvn = input("\n--> Please check the Antab file and answer the following question. \n(Press Enter to move on)")
               whatdelmt = input("\n\nAssuming RCL/LCP columns are tied into a single column with a delimeter,,, \n--> What is the delimeter here? (e.g., / or , or any symbol) \n: ")
               log("\n====================================================================== \n(1) The single column with dual data will be divided into two columns! \n    (..later set 'R' & 'L' in INDEX properly) \n\n(2) Any empty bins will be filled with '0' values! \n======================================================================"); time.sleep(3)
               newlist = []
               for l in rd3:
                  if len(l.split()) == 3:
                     newline = l.split()[:2] + l.split()[-1].split(whatdelmt)
                     newline = ' '.join(newline) + ' \n'
                     newlist.append(newline)
                  elif len(l.split()) == 2:
                     newline = l.split()
                     newline.append('0')
                     newline.append('0')
                     newline = ' '.join(newline) + ' \n'
                     newlist.append(newline)
                  else:
                     newlist.append(l)
               del rd3
               rd3 = newlist
               break
      self.tsys1 = rd3
      log("\n**DONE** \n..check self + tsys1 \
      \n////////////////////////////////////////////////////////////////////////////////")



   def overview(self):
      """
      Initial check of the data to find any suspicous.
      Either Tsys is: 999 or >=9999 or 0 or Negative.

      e.g., self.overview()

      output: self.inich
      
      """
      self.inich = []
      dv1 = self.colids.split()
      for i,j in enumerate(dv1,0):
         eachtsys = np.genfromtxt(self.tsys1, usecols=2+i, unpack=True, invalid_raise=False, missing_values='', usemask=False, dtype=float)
         aa = 0
         bb = 0
         cc = 0
         dd = 0
         for k in eachtsys:
            if (k == 999) or (k == 999.0):
               if aa == 0:
                  log("-> 999 found!!")
                  aa = 1
                  continue
               else:
                  continue
            elif k >= 9999:
               if bb == 0:
                  log("-> higher than 9999 found!!")
                  bb = 1
                  continue
               else:
                  continue
            elif k == 0:
               if cc == 0:
                  log("-> 0 found!!")
                  cc = 1
                  continue
               else:
                  continue
            elif k < 0:
               if dd == 0:
                  log("-> negative value found!!")
                  dd = 1
                  continue
               else:
                  continue
         if (aa == 1) | (bb == 1) | (cc == 1) | (dd == 1):
            self.inich.append(1)
         else:
            self.inich.append(0)
      log('\n***********************************RESULTS***********************************')
      for i,j in enumerate(self.inich,0):
         if j == 1:
            log("\n--> {} with something Wrong! (check further with 'showsys')".format(dv1[i]))
         else:
            log("\n--> {} seems Fine. (BUT at least check the plot with 'showsys')".format(dv1[i]))
      log("\n**DONE** \n..check self + inich (for each IF, 0: Fine / 1: Unreasonable found) \
      \n////////////////////////////////////////////////////////////////////////////////")



   def showsys(self, fonttit=12, fontaxlab=13, fontleg=11, fontticklab=11, autosav=False, datout=False, Ymax=None, Ymin=None):
      """
      Generate Tsys plot for visual inspection.

      <Params>
       fonttit     : Fontsize of Figure Title 
       fontaxlab   : Fontsize of Figure Axis labels
       fontleg     : Fontsize of Figure Legend
       fontticklab : Fontsize of Figure Axis-tick labels
       autosav     : If True, save the result as output figure (.png)
       datout      : If True, save the result as output text file (.dat)
       Ymax        : Set Y-axis limit (=Maximum)
       Ymin        : Set Y-axis limit (=Minimum)

      e.g., self.showsys(fonttit=10, fontaxlab=12, fontleg=11, fontyticklab=11, fontxticklab=11, autosav=False)
            or just 'self.showsys()' with default parameter setting.

      output: self.tarr (and .png/.dat files).
      
      """
      simpletest = self.tsys1[0].split()[1]
      new_t = []
      if simpletest.count(":") == 2:
         for l in self.tsys1:
            tem_d = l.split()[0]        #% day array
            tem_hms = l.split()[1]       #% hh:mm:ss array
            #% converting all of them to a day with decimal numbers
            div_h = tem_hms.split(':')[0]
            div_m = tem_hms.split(':')[1]
            div_s = tem_hms.split(':')[2]
            dayform = (int(div_h)/24.) + (float(div_m)/60. /24.) + (float(div_s)/60. /60. /24.) + int(tem_d)
            new_t.append(dayform)
      elif simpletest.count(":") == 1:
         for l in self.tsys1:
            tem_d = l.split()[0]        #% day array
            tem_hm = l.split()[1]       #% hh:mm array
            div_h = tem_hm.split(':')[0]
            div_m = tem_hm.split(':')[1]
            dayform = (int(div_h)/24.) + (float(div_m)/60. /24.) + int(tem_d)
            new_t.append(dayform)
            #% --> actual x-array for interpolation
      new_t = np.asarray(new_t)
      self.tarr = new_t
      if self.colnum > 8:
         Hor, Ver = 14.5, 10.5
      elif self.colnum == 8:
         Hor, Ver = 13, 10
      elif self.colnum in [7,6,5]:
         Hor, Ver = 10.5, 8.5
      elif self.colnum in [4,3]:
         Hor, Ver = 9, 7
      elif self.colnum in [2,1]:
         Hor, Ver = 7, 6
      # figure id set
      for D in range(1000):
         figid = randrange(0, 1000)
         if plt.fignum_exists(figid):
            del figid
            continue
         else:
            break
      fig_pol=plt.figure(figid, figsize=(Hor, Ver))
      plt.figure(figid)
      plt.rcParams['legend.frameon'] = 'False'
      plt.rcParams['xtick.labelsize'] = 11
      plt.rcParams['ytick.labelsize'] = 11
      for i,j in enumerate(self.colids.split(),0):
         if self.colnum > 8:
            plt.subplot(4, 4, i+1)
         elif self.colnum in [7,8]:
            plt.subplot(4, 2, i+1)
         elif self.colnum in [5,6]:
            plt.subplot(3, 2, i+1)
         elif self.colnum in [3,4]:
            plt.subplot(2, 2, i+1)
         elif self.colnum in [1,2]:
            plt.subplot(2, 1, i+1)
         #
         k2 = np.genfromtxt(self.tsys1, usecols=2+i, unpack=True, invalid_raise=False, missing_values='', usemask=False, dtype=float)
         #
         if (j.startswith('R')) & ('L' not in j):
            ccc = '#1f77b4'
         elif (j.startswith('L')) & ('R' not in j):
            ccc = '#ff7f0e'
         elif ('R' in j) & ('L' in j):
            ccc = 'tab:brown'
         plt.figure(figid)
         plt.plot(new_t, k2, markersize=2, marker='o', linewidth=0.8, label=j, color=ccc)
         plt.yticks(fontsize=fontticklab)
         plt.xticks(fontsize=fontticklab)
         plt.legend(loc=2, markerscale=1.4, fontsize=fontleg)
         #vax = int(np.round(max(k2)))
         #vin = int(np.round(min(k2)))
         vav = np.round(np.median(k2), 1)
         vst = np.round(np.std(k2), 1)
         if Ymax:
            if Ymin:
               plt.ylim([Ymin, Ymax])
            else:
               plt.ylim([plt.ylim()[0], Ymax])
         if Ymin:
            if Ymax:
               plt.ylim([Ymin, Ymax])
            else:
               plt.ylim([Ymin, plt.ylim()[1]])
         else:
            opz1 = np.linspace(plt.ylim()[0], plt.ylim()[1], 7)
            thegap = np.abs(np.abs(opz1[-1])-np.abs(opz1[-2]))
            plt.ylim(opz1[0]-thegap*0.0, opz1[-1]+thegap*1.3)
         plt.title("*{}* - Median={}K, Std={}K".format(self.antcode,vav,vst), color='r', fontsize=fonttit)
         plt.xlabel("Decimal day", fontsize=fontaxlab)
         plt.ylabel("Tsys [K]", fontsize=fontaxlab)
         plt.minorticks_on()
         plt.tick_params(axis='both', which='major', length=5, direction='in', pad=2, color='k')
         plt.tick_params(axis='both', which='minor', length=3, direction='in', pad=2, color='k')
      plt.figure(figid); plt.tight_layout()
      # plt.show()
      # for 16 panels..
      # plt.subplots_adjust(left=0.045, bottom=0.050, right=0.975, top=0.965, wspace=0.190, hspace=0.345)
      if autosav == False:
         log("\nautosav is set 'False', thus no output '~.png' file.")
      elif autosav == True:
         plt.figure(figid)
         ffnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys1.png"
         i = 0
         if ffnam in os.listdir():
            log("\nSaving Figure as .png..... the file name exists!  -->  Add a higher number to it")
            for j in range(1000):
               i=i+1
               mfnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys1"+"_"+str(i)+".png"
               if mfnam in os.listdir():
                  continue
               else:
                  break
            plt.savefig(mfnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(mfnam))
         else:
            plt.savefig(ffnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(ffnam))
      if datout == False:
         log("\ndatout is set 'False', thus no output '~.dat' file.")
      elif datout == True:
         outtotext = copy.deepcopy(self.tsys1)
         outtotext.append("/\n")
         outtotext.insert(0, self.HDb)
         outtotext.insert(0, self.HDa)
         outn = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys1.dat"
         log("\n\n... {} ! \n".format(outn))
         with open(outn, 'w') as p31:
            p31.writelines(outtotext)
      log("\n**DONE** \n..check self + tarr and the output files! \
      \n////////////////////////////////////////////////////////////////////////////////")



   def intpsys(self, whichdat=1, fonttit=12, fontaxlab=13, fontleg=11, fontticklab=11, modsize=9, autosav=False, datout=False, update=True):
      """
      Applying linear interpolation to the Tsys data.
      Modification of the cutoff thresholds can be set (will be asked).

      <Param>
       whichdat: 1 - Data raw
                 2 - Data linear interpolated
                 3 - Data smoothed by n-sigma cut
                 4 - Data IF copied
       fonttit     : Fontsize of Figure Title 
       fontaxlab   : Fontsize of Figure Axis labels
       fontleg     : Fontsize of Figure Legend
       fontticklab : Fontsize of Figure Axis-tick labels
       modsize     : Symbol size of modified Tsys values
       autosav     : If True, save the result as output figure (.png)
       datout      : If True, save the result as output text file (.dat)
       update      : If True, save the result in self.tsys2 (--> whichdat=2).
                     Normally, you don't need to set it False (default=True).
                     If False, the result will not be stored. This could be useful,
                     when you want to do some test runs with the result from intpsys
                     (i.e., self-update with 'whichdat=2'). In that case, make sure
                     to set 'datout = False'. Then, turn it 'True' when you are 
                     confident with the result.

      e.g., self.intpsys(whichdat=1)

      output: self.tsys2 (and .png/.dat files)

      """
      if whichdat == 1:
         datbox = self.tsys1        # raw data
      elif whichdat == 2:
         datbox = self.tsys2        # linear interpolated
      elif whichdat == 3:
         datbox = self.tsys3        # smoothing with n-sigma
      elif whichdat == 4:
         datbox = self.tsys4        # copying neighboring IF
      #
      if datbox:
         pass
      else:
         log("\n\n...No data found! (check the 'whichdat' parameter)"); time.sleep(1.5)
         return
      if whichdat == 2:
         log("\n***** Given data selection (whichdat), it is self-updating ***** \n - If this is a test run, you should set 'update=False' \n - If you are satisfying with the result, then now re-run with 'update=True'"); time.sleep(0.5)
      if self.tarr is None:
         log("\n...run 'showsys' first!"); time.sleep(1.5)
         return
      else:
         pass
      new_t = self.tarr
      notice = input("\n******************************************************************************** \n********************************************************************************\
      \n...Erroneous can be... \n -->  0 \n -->  Negative \n -->  999.0 \n -->  >[User input] \n -->  (optional) Between A and B \
      \n\n(Press Enter and move on!) \n")
      if self.colnum > 8:
         Hor, Ver = 14.5, 10.5
      elif self.colnum == 8:
         Hor, Ver = 13, 10
      elif self.colnum in [7,6,5]:
         Hor, Ver = 10.5, 8.5
      elif self.colnum in [4,3]:
         Hor, Ver = 9, 7
      elif self.colnum in [2,1]:
         Hor, Ver = 7, 6
      # figure id set
      for D in range(1000):
         figid = randrange(0, 1000)
         if plt.fignum_exists(figid):
            del figid
            continue
         else:
            break
      plt.ioff()
      fig_pol=plt.figure(figid, figsize=(Hor, Ver))
      plt.figure(figid)
      plt.rcParams['legend.frameon'] = 'False'
      plt.rcParams['xtick.labelsize'] = 11
      plt.rcParams['ytick.labelsize'] = 11
      SAVE = []
      LEGEN = self.colids
      numcols = len(LEGEN.split())
      for i in range(numcols):
         if (LEGEN.split()[i].startswith('R')) & ('L' not in LEGEN.split()[i]):
            ccc = '#1f77b4'
            theguys = 'r'
         elif (LEGEN.split()[i].startswith('L')) & ('R' not in LEGEN.split()[i]):
            ccc = '#ff7f0e'
            theguys = '#2ca02c'
         elif ('R' in LEGEN.split()[i]) & ('L' in LEGEN.split()[i]):
            ccc = 'tab:brown'
            theguys = 'limegreen'
         LAB = LEGEN.split()[i]
         if self.colnum > 8:
            plt.subplot(4, 4, i+1)
         elif self.colnum in [7,8]:
            plt.subplot(4, 2, i+1)
         elif self.colnum in [5,6]:
            plt.subplot(3, 2, i+1)
         elif self.colnum in [3,4]:
            plt.subplot(2, 2, i+1)
         elif self.colnum in [1,2]:
            plt.subplot(2, 1, i+1)
         TEMPLATE = np.zeros(np.shape(datbox), int)
         tsysset = np.genfromtxt(datbox, usecols=2+i, dtype='float')
         numrows = len(tsysset)
         shouldbebelow = input("\n*Tsys column *{}* Cut-out above THIS threshold!* \nGive input or just Enter (default: 9999) \n: ".format(LEGEN.split()[i]))
         if shouldbebelow == '':
            thiscut = 9999.0
         else:
            thiscut = float(shouldbebelow)
         manualbtw = input("\n*Tsys column *{}* Cut-out Between A and B?* \n(yes/y or no/n/Enter; default = no) \n: ".format(LEGEN.split()[i]))
         if (manualbtw == 'yes') or (manualbtw == 'y'):
            btwA = input("\nTsys column *{}* Between A (HIGH) and B \n--> A (HIGH) is: ".format(LEGEN.split()[i]))
            btwB = input("\nTsys column *{}* Between A and B (LOW) \n--> B (LOW) is: ".format(LEGEN.split()[i]))         
         for j in range(numrows):
            if tsysset[j] == 999.0:
               TEMPLATE[j] = 1
               continue
            elif tsysset[j] >= thiscut:
               TEMPLATE[j] = 1
               continue
            elif tsysset[j] <= 0:
               TEMPLATE[j] = 1
               continue
            #
            elif (manualbtw == 'yes') or (manualbtw == 'y'):
               if float(btwB) <= tsysset[j] <= float(btwA):
                  TEMPLATE[j] = 1
                  continue
         #% x & y array to be used for interpolation
         JUDGE = np.nonzero(TEMPLATE)[0]
         if len(JUDGE) == 0:
            SAVE.append(tsysset)
            pass
         else:
            if TEMPLATE[0] == 1:
               for kk,k in enumerate(TEMPLATE, 0):
                  if k == 1:
                     continue
                  elif k == 0:
                     # Assume the closest measurement to the FIRST timestamp
                     Front = tsysset[kk]
                     tsysset[0] = Front
                     TEMPLATE[0] = 0
                     break
            if TEMPLATE[-1] == 1:
               for kk,k in enumerate(TEMPLATE[::-1], 0):
                  if k == 1:
                     continue
                  elif k == 0:
                     # Assume the closest measurement to the LAST timestamp
                     End = tsysset[::-1][kk]
                     tsysset[-1] = End
                     TEMPLATE[-1] = 0
                     break
            YES = np.where(TEMPLATE == 0)[0]    # good tsys for INTERPOLATION
            NO = np.nonzero(TEMPLATE)[0]      # bad tsys (after checking the first/last values)
            selected_time = new_t[YES]
            selected_tsys = tsysset[YES]
            #=================================
            #% Linear interpolation
            linv = interp1d(selected_time, selected_tsys, kind='linear')
            LPDONE = np.asarray([round(z, 1) for z in linv(new_t)])
            SAVE.append(LPDONE)
            del LPDONE
         #% now PLOTTING
         plt.figure(figid)
         plt.plot(new_t, SAVE[-1], markersize=2, marker='o', linewidth=0.8, alpha=1.0, zorder=0, color=ccc, label=LAB)
         plt.yticks(fontsize=fontticklab)
         plt.xticks(fontsize=fontticklab)
         if len(JUDGE) >= 1:
            plt.plot(new_t[JUDGE], SAVE[-1][JUDGE], linewidth=0, marker='*', markersize=modsize, color=theguys, label='Lin-Intp')
            log("\nInterpolation has been performed!!")
         else:
            log("\nNo interpolation needed.")
         log("\n------------------------------------")
         log("{} Number of Erroneous Tsys --> {} !".format(LAB,len(JUDGE)))
         log("------------------------------------"); time.sleep(0.1)
         #% basic statistical properties
         vav = np.round(np.median(SAVE[-1]), 1)
         vst = np.round(np.std(SAVE[-1]), 1)
         #% plot layout
         opz1 = np.linspace(plt.ylim()[0], plt.ylim()[1], 7)
         thegap = np.abs(np.abs(opz1[-1])-np.abs(opz1[-2]))
         plt.ylim(opz1[0]-thegap*0.0, opz1[-1]+thegap*1.3)
         plt.legend(loc=2, fontsize=fontleg, numpoints=1, markerscale=1.4, labelspacing=0.1, handletextpad=0.5, borderaxespad=0.2, handlelength=1.0, handleheight=0.5, ncol=2, columnspacing=1.2)
         plt.title("*{}* - Median={}K, Std={}K".format(self.antcode,vav,vst), color='r', fontsize=fonttit)
         plt.xlabel("Decimal day", fontsize=fontaxlab)
         plt.ylabel("Tsys [K]", fontsize=fontaxlab)
         plt.tick_params(axis='both', which='major', length=5, direction='in', pad=2, color='k')
         plt.tick_params(axis='both', which='minor', length=3, direction='in', pad=2, color='k')
         plt.minorticks_on()
         plt.tight_layout()
      #% for output results
      plt.figure(figid)
      plt.show()
      plt.ion()
      td,tmh = np.genfromtxt(self.tsys1, usecols=(0,1), unpack=True, invalid_raise=False, missing_values='', usemask=False, dtype=str)
      outdat = []
      for v in range(len(td)):
         newlin = td[v] + " " + tmh[v]
         for y in range(len(SAVE)):
            if y == len(SAVE)-1:
               newlin = newlin + " " + str(SAVE[y][v]) + " \n"
            else:
               newlin = newlin + " " + str(SAVE[y][v])
         outdat.append(newlin)
         del newlin
         continue
      if update == True:
         self.tsys2 = outdat
         log("\nupdate is set 'True', self.tsys2 has been updated!")
      else:
         log("\nupdate is set 'False', keep using previous data in self.tsys2.")
      if autosav == False:
         log("\nautosav is set 'False', thus no output .png file.")
      elif autosav == True:
         plt.figure(figid)
         ffnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys2.png"
         i = 0
         if ffnam in os.listdir():
            log("\nSaving Figure as .png..... the file name exists!  -->  Add a higher number to it")
            for j in range(1000):
               i=i+1
               mfnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys2"+"_"+str(i)+".png"
               if mfnam in os.listdir():
                  continue
               else:
                  break
            plt.savefig(mfnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(mfnam))
         else:
            plt.savefig(ffnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(ffnam))
      if datout == False:
         log("\ndatout is set 'False', thus no output .dat file.")
      elif datout == True:
         if update == False:
            log("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \ndatout is set True, but 'update=False' now. \nThis means that you keep using previous intpsys result. \nTo export the current result, run this again with 'update=True'. \n\nNo output text file made. \n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); time.sleep(1.5)
            return
         outtotext = copy.deepcopy(self.tsys2)
         outtotext.append("/\n")
         outtotext.insert(0, self.HDb)
         outtotext.insert(0, self.HDa)
         outn = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys2.dat"
         log("\n\n... {} ! \n".format(outn))
         with open(outn, 'w') as p32:
            p32.writelines(outtotext)
      log("\n**DONE** \n..check self + tsys2 and the output files! \
      \n////////////////////////////////////////////////////////////////////////////////")



   def smthsys(self, whichdat=1, siglev=5, fonttit=12, fontaxlab=13, fontleg=11, fontticklab=11, modsize=9, autosav=False, datout=False, update=True):
      """
      To smooth out the curve by removing some outliers.
      Specific IFs/time ranges can be selected.

      <Param>
       whichdat: 1 - Data raw
                 2 - Data linear interpolated
                 3 - Data smoothed by n-sigma cut
                 4 - Data IF copied
       siglev      : n-sigma = e.g., 2 --> median +- 2*std   (default=5).
       fonttit     : Fontsize of Figure Title 
       fontaxlab   : Fontsize of Figure Axis labels
       fontleg     : Fontsize of Figure Legend
       fontticklab : Fontsize of Figure Axis-tick labels
       modsize     : Symbol size of modified Tsys values
       autosav     : If True, save the result as output figure (.png).
       datout      : If True, save the result as output text file (.dat).
       update      : If True, save the result in self.tsys3 (--> whichdat=3).
                     Normally, you don't need to set it False (default=True).
                     If False, the result will not be stored. This could be useful,
                     when you want to do some test runs with the result from smthsys
                     (i.e., self-updating with 'whichdat=3'). In that case, make sure
                     to set 'datout = False'. Then, turn it 'True' when you are 
                     confident with the result.

      e.g., self.smthsys(whichdat=2)

      output: self.tsys3 (and .png/.dat files)

      """
      if whichdat == 1:
         datbox = self.tsys1        # raw data
      elif whichdat == 2:
         datbox = self.tsys2        # linear interpolated
      elif whichdat == 3:
         datbox = self.tsys3        # smoothing with n-sigma
      elif whichdat == 4:
         datbox = self.tsys4        # copying neighboring IF
      #
      if datbox:
         pass
      else:
         log("\n\n...No data found! (check the 'whichdat' parameter)"); time.sleep(1.5)
         return
      if whichdat == 3:
         log("\n***** Given data selection (whichdat), it is self-updating ***** \n - If this is a test run, you should set 'update=False' \n - If you are satisfying with the result, then now re-run with 'update=True'"); time.sleep(0.5)
      if self.tarr is None:
         log("\n...run 'showsys' first!"); time.sleep(1.5)
         return
      else:
         pass
      new_t = self.tarr
      for i in range(int(1e4)):
         ifselection = input("\nApply to all IFs (1) or only selected IFs/times (2)? \n(Give 1 or 2; just Enter --> 1 as default) \n: ")
         if (ifselection == '') or (ifselection == '1'):
            for u in range(1000):
               tset = input("\nFor ALL IFs, specific time range? (y or n; Enter --> n for the whole time range) \n: ")
               if (tset == 'y') | (tset == 'n') | (tset == ''):
                  break
               else:
                  log("\n...wrong input, re-try!")
                  continue
            if (tset == 'n') | (tset == ''):
               log("\nConsider full time range!")
               forvlines = [new_t[0], new_t[-1]]
            else:
               timing = input("Give a time range (e.g., 114.4 114.6   --> from 114.4 to 114.6; Decimal day) \n: ")
               timing = timing.split()
               forvlines = [float(timing[0]), float(timing[1])]
            break
         elif ifselection == '2':
            log("\nAmong IFs below...")
            for m,n in enumerate(self.colids.split(), 1):
               log("  {} - {}".format(m,n))
            ifset = input("\nSelect IFs to be smoothed (e.g., 2 3 5 --> Index numbers printed above) \n: ")
            ifset = ifset.split()
            THEIFS = []
            for h in ifset:
               THEIFS.append(self.colids.split()[int(h)-1])
            break
         else:
            log("\nWrong input. Give a valid input (Retry).")
            continue
      if self.colnum > 8:
         Hor, Ver = 14.5, 10.5
      elif self.colnum == 8:
         Hor, Ver = 13, 10
      elif self.colnum in [7,6,5]:
         Hor, Ver = 10.5, 8.5
      elif self.colnum in [4,3]:
         Hor, Ver = 9, 7
      elif self.colnum in [2,1]:
         Hor, Ver = 7, 6
      # figure id set
      for D in range(1000):
         figid = randrange(0, 1000)
         if plt.fignum_exists(figid):
            del figid
            continue
         else:
            break
      plt.ioff()
      fig_pol=plt.figure(figid, figsize=(Hor, Ver))
      plt.figure(figid)
      plt.rcParams['legend.frameon'] = 'False'
      plt.rcParams['xtick.labelsize'] = 11
      plt.rcParams['ytick.labelsize'] = 11
      SAVE = []
      LEGEN = self.colids
      numcols = len(LEGEN.split())
      for i in range(numcols):
         if (LEGEN.split()[i].startswith('R')) & ('L' not in LEGEN.split()[i]):
            ccc = '#1f77b4'
            theguys = 'r'
         elif (LEGEN.split()[i].startswith('L')) & ('R' not in LEGEN.split()[i]):
            ccc = '#ff7f0e'
            theguys = '#2ca02c'
         elif ('R' in LEGEN.split()[i]) & ('L' in LEGEN.split()[i]):
            ccc = 'tab:brown'
            theguys = 'limegreen'
         LAB = LEGEN.split()[i]
         if self.colnum > 8:
            plt.subplot(4, 4, i+1)
         elif self.colnum in [7,8]:
            plt.subplot(4, 2, i+1)
         elif self.colnum in [5,6]:
            plt.subplot(3, 2, i+1)
         elif self.colnum in [3,4]:
            plt.subplot(2, 2, i+1)
         elif self.colnum in [1,2]:
            plt.subplot(2, 1, i+1)
         tsysset = np.genfromtxt(datbox, usecols=2+i, dtype='float')
         if ifselection == '2':
            log("\n..IF-selection is applied..")
            if LEGEN.split()[i] in THEIFS:
               for u in range(1000):
                  tset = input("\nFor {}, specific time range? (y or n; Enter --> n) \n: ".format(LEGEN.split()[i]))
                  if (tset == 'y') | (tset == 'n') | (tset == ''):
                     break
                  else:
                     log("\n...wrong input, re-try!")
                     continue
               if (tset == 'n') | (tset == ''):
                  log("\nConsider full time range!")
                  forvlines = [new_t[0], new_t[-1]]
                  TEMPLATE = np.zeros(np.shape(datbox), int)
                  numrows = len(tsysset)
                  for j in range(numrows):
                     if np.median(tsysset)-(siglev*np.std(tsysset)) <= tsysset[j] <= np.median(tsysset)+(siglev*np.std(tsysset)):
                        continue
                     else:
                        TEMPLATE[j] = 1
                        continue
                  #% x & y array to be used for interpolation
                  JUDGE = np.nonzero(TEMPLATE)[0]
                  if len(JUDGE) == 0:   # if there is no outlier.
                     SAVE.append(tsysset)
                     pass
                  else:
                     if TEMPLATE[0] == 1:
                        for kk,k in enumerate(TEMPLATE, 0):
                           if k == 1:
                              continue
                           elif k == 0:
                              # Assume the closest measurement to the FIRST timestamp
                              Front = tsysset[kk]
                              tsysset[0] = Front
                              TEMPLATE[0] = 0
                              break
                     if TEMPLATE[-1] == 1:
                        for kk,k in enumerate(TEMPLATE[::-1], 0):
                           if k == 1:
                              continue
                           elif k == 0:
                              # Assume the closest measurement to the LAST timestamp
                              End = tsysset[::-1][kk]
                              tsysset[-1] = End
                              TEMPLATE[-1] = 0
                              break
                     YES = np.where(TEMPLATE == 0)[0]    # good tsys for INTERPOLATION
                     NO = np.nonzero(TEMPLATE)[0]      # bad tsys (after checking the first/last values)
                     selected_time = new_t[YES]
                     selected_tsys = tsysset[YES]
                     #% Linear interpolation
                     linv = interp1d(selected_time, selected_tsys, kind='linear')
                     LPDONE = np.asarray([round(z, 1) for z in linv(new_t)])
                     SAVE.append(LPDONE)
                     del LPDONE
               else:   # time range selected
                  timing = input("Give a time range (e.g., 114.4 114.6  --> from 114.4 to 114.6; Decimal day) \n: ")
                  timing = timing.split()
                  forvlines = [float(timing[0]), float(timing[1])]
                  theindice = np.where((new_t >= float(timing[0])) & (new_t <= float(timing[1])))[0]
                  cutT = new_t[theindice]
                  cutD = tsysset[theindice]
                  TEMPLATE = np.zeros(np.shape(cutD), int)
                  numrows = len(cutD)
                  for j in range(numrows):
                     if np.median(cutD)-(siglev*np.std(cutD)) <= cutD[j] <= np.median(cutD)+(siglev*np.std(cutD)):
                        continue
                     else:
                        TEMPLATE[j] = 1
                        continue
                  JUDGE = np.nonzero(TEMPLATE)[0]
                  if len(JUDGE) == 0:   # if there is no outlier.
                     SAVE.append(tsysset)
                     pass
                  else:
                     if TEMPLATE[0] == 1:
                        for kk,k in enumerate(TEMPLATE, 0):
                           if k == 1:
                              continue
                           elif k == 0:
                              # Assume the closest measurement to the FIRST timestamp
                              Front = cutD[kk]
                              cutD[0] = Front
                              TEMPLATE[0] = 0
                              break
                     if TEMPLATE[-1] == 1:
                        for kk,k in enumerate(TEMPLATE[::-1], 0):
                           if k == 1:
                              continue
                           elif k == 0:
                              # Assume the closest measurement to the LAST timestamp
                              End = cutD[::-1][kk]
                              cutD[-1] = End
                              TEMPLATE[-1] = 0
                              break
                     YES = np.where(TEMPLATE == 0)[0]    # good tsys for INTERPOLATION
                     NO = np.nonzero(TEMPLATE)[0]      # bad tsys (after checking the first/last values)
                     selected_time = cutT[YES]
                     selected_tsys = cutD[YES]
                     #% Linear interpolation
                     linv = interp1d(selected_time, selected_tsys, kind='linear')
                     LPDONE = np.asarray([round(z, 1) for z in linv(cutT)])
                     combtsys = []
                     AS = 0
                     for o,p in enumerate(tsysset, 0):
                        if AS < len(theindice):
                           if o == theindice[AS]:
                              combtsys.append(LPDONE[AS])
                              AS += 1
                              continue
                           else:
                              combtsys.append(p)
                        else:
                           combtsys.append(p)
                     combtsys = np.asarray(combtsys)
                     SAVE.append(combtsys)
                     JUDGE = JUDGE + theindice[0]
                     del LPDONE
            #===========================
            else:
               TEMPLATE = np.zeros(np.shape(datbox), int)
               JUDGE = np.nonzero(TEMPLATE)[0]
               SAVE.append(tsysset)
         ###########################
         else:
            theindice = np.where((new_t >= forvlines[0]) & (new_t <= forvlines[1]))[0]
            cutT = new_t[theindice]
            cutD = tsysset[theindice]
            TEMPLATE = np.zeros(np.shape(cutD), int)
            numrows = len(cutD)
            for j in range(numrows):
               if np.median(cutD)-(siglev*np.std(cutD)) <= cutD[j] <= np.median(cutD)+(siglev*np.std(cutD)):
                  continue
               else:
                  TEMPLATE[j] = 1
                  continue
            JUDGE = np.nonzero(TEMPLATE)[0]
            if len(JUDGE) == 0:   # if there is no outlier.
               SAVE.append(tsysset)
               pass
            else:
               if TEMPLATE[0] == 1:
                  for kk,k in enumerate(TEMPLATE, 0):
                     if k == 1:
                        continue
                     elif k == 0:
                        # Assume the closest measurement to the FIRST timestamp
                        Front = cutD[kk]
                        cutD[0] = Front
                        TEMPLATE[0] = 0
                        break
               if TEMPLATE[-1] == 1:
                  for kk,k in enumerate(TEMPLATE[::-1], 0):
                     if k == 1:
                        continue
                     elif k == 0:
                        # Assume the closest measurement to the LAST timestamp
                        End = cutD[::-1][kk]
                        cutD[-1] = End
                        TEMPLATE[-1] = 0
                        break
               YES = np.where(TEMPLATE == 0)[0]    # good tsys for INTERPOLATION
               NO = np.nonzero(TEMPLATE)[0]      # bad tsys (after checking the first/last values)
               selected_time = cutT[YES]
               selected_tsys = cutD[YES]
               #% Linear interpolation
               linv = interp1d(selected_time, selected_tsys, kind='linear')
               LPDONE = np.asarray([round(z, 1) for z in linv(cutT)])
               combtsys = []
               AS = 0
               for o,p in enumerate(tsysset, 0):
                  if AS < len(theindice):
                     if o == theindice[AS]:
                        combtsys.append(LPDONE[AS])
                        AS += 1
                        continue
                     else:
                        combtsys.append(p)
                  else:
                     combtsys.append(p)
               combtsys = np.asarray(combtsys)
               SAVE.append(combtsys)
               JUDGE = JUDGE + theindice[0]
               del LPDONE
         #% now PLOTTING
         plt.figure(figid)
         plt.plot(new_t, SAVE[-1], markersize=2, marker='o', linewidth=0.8, alpha=1.0, zorder=0, color=ccc, label=LAB)
         plt.yticks(fontsize=fontticklab)
         plt.xticks(fontsize=fontticklab)
         if len(JUDGE) >= 1:
            plt.plot(new_t[JUDGE], SAVE[-1][JUDGE], linewidth=0, marker='*', markersize=modsize, color=theguys, label='Lin-Intp'+' w. '+str(siglev)+r'-$\sigma$'+' smth')
            if forvlines[0] <= new_t[0]:
               forvlines[0] = new_t[0]
            if forvlines[1] >= new_t[-1]:
               forvlines[1] = new_t[-1]
            plt.axvline(forvlines[0], color='m', alpha=0.7, linestyle='--', linewidth=2, zorder=0)
            plt.axvline(forvlines[1], color='m', alpha=0.7, linestyle='--', linewidth=2, zorder=0)
            log("\nInterpolation has been performed!!")
         else:
            log("\nNo interpolation needed.")
         log("\n------------------------------------")
         log("{} Number of Erroneous Tsys --> {} !".format(LAB,len(JUDGE)))
         log("------------------------------------")
         #% basic statistical properties
         vav = np.round(np.median(SAVE[-1]), 1)
         vst = np.round(np.std(SAVE[-1]), 1)
         #% plot layout
         opz1 = np.linspace(plt.ylim()[0], plt.ylim()[1], 7)
         thegap = np.abs(np.abs(opz1[-1])-np.abs(opz1[-2]))
         plt.ylim(opz1[0]-thegap*0.0, opz1[-1]+thegap*1.3)
         plt.legend(loc=2, fontsize=fontleg, numpoints=1, markerscale=1.4, labelspacing=0.1, handletextpad=0.5, borderaxespad=0.2, handlelength=1.0, handleheight=0.5, ncol=2, columnspacing=1.2)
         plt.title("*{}* - Median={}K, Std={}K".format(self.antcode,vav,vst), color='r', fontsize=fonttit)
         plt.xlabel("Decimal day", fontsize=fontaxlab)
         plt.ylabel("Tsys [K]", fontsize=fontaxlab)
         plt.tick_params(axis='both', which='major', length=5, direction='in', pad=2, color='k')
         plt.tick_params(axis='both', which='minor', length=3, direction='in', pad=2, color='k')
         plt.minorticks_on()
         plt.tight_layout()
      #% for output results
      plt.figure(figid)
      plt.show()
      plt.ion()
      td,tmh = np.genfromtxt(self.tsys1, usecols=(0,1), unpack=True, invalid_raise=False, missing_values='', usemask=False, dtype=str)
      outdat = []
      for v in range(len(td)):
         newlin = td[v] + " " + tmh[v]
         for y in range(len(SAVE)):
            if y == len(SAVE)-1:
               newlin = newlin + " " + str(SAVE[y][v]) + " \n"
            else:
               newlin = newlin + " " + str(SAVE[y][v])
         outdat.append(newlin)
         del newlin
         continue
      if update == True:
         self.tsys3 = outdat
         log("\nupdate is set 'True', self.tsys3 has been updated!")
      else:
         log("\nupdate is set 'False', keep using previous data in self.tsys3.")
      if autosav == False:
         log("\nautosav is set 'False', thus no output .png file.")
      elif autosav == True:
         plt.figure(figid)
         ffnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys3.png"
         i = 0
         if ffnam in os.listdir():
            log("\nSaving Figure as .png..... the file name exists!  -->  Add a higher number to it")
            for j in range(1000):
               i=i+1
               mfnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys3"+"_"+str(i)+".png"
               if mfnam in os.listdir():
                  continue
               else:
                  break
            plt.savefig(mfnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(mfnam))
         else:
            plt.savefig(ffnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(ffnam))
      if datout == False:
         log("\ndatout is set 'False', thus no output .dat file.")
      elif datout == True:
         if update == False:
            log("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \ndatout is set True, but 'update=False' now. \nThis means that you keep using previous intpsys result. \nTo export the current result, run this again with 'update=True'. \n\nNo output text file made. \n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); time.sleep(1.5)
            return
         outtotext = copy.deepcopy(self.tsys3)
         outtotext.append("/\n")
         outtotext.insert(0, self.HDb)
         outtotext.insert(0, self.HDa)
         outn = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys3.dat"
         log("\n\n... {} ! \n".format(outn))
         with open(outn, 'w') as p32:
            p32.writelines(outtotext)
      log("\n**DONE** \n..check self + tsys3 and the output files! \
      \n////////////////////////////////////////////////////////////////////////////////")



   def cpifsys(self, whichdat=1, reon=False, fonttit=12, fontaxlab=13, fontleg=11, fontticklab=11, autosav=False, datout=False, update=True):
      """
      Copy and paste (CP) between IFs.
      A single run of this function will handle one IF.
      For doing it again from the beginning with new input data, set 'reon=True'.
      If there are multiple IFs to be CPed, do the self-update ('whichdat=4').
      In this case, you don't need the test runs. So, just keep 'update=True'.

      <Param>
       whichdat: 1 - Data raw
                 2 - Data linear interpolated
                 3 - Data smoothed by n-sigma cut
                 4 - Data IF copied (repeatable for update)
       reon        : Remove records (i.e., plot-legend) saved from previous runs.
                     If you kept self-updating (whichdat=4) a few times and want to 
                     initialize it, set reon=True & whichdat=* (here * is the number
                     you used at the first run of cpifsys (e.g., 1 or 2 or 3).
       fonttit     : Fontsize of Figure Title 
       fontaxlab   : Fontsize of Figure Axis labels
       fontleg     : Fontsize of Figure Legend
       fontticklab : Fontsize of Figure Axis-tick labels
       autosav     : If True, save the result as output figure (.png).
       datout      : If True, save the result as output text file (.dat).
       update      : If True, save the result in self.tsys4 (--> whichdat=4).
                     Normally, you don't need to set it False (default=True).
                     If False, the result will not be stored. This could be useful,
                     when you want to do some test runs with the result from cpifsys
                     (i.e., self-updating with 'whichdat=4'). In that case, make sure
                     to set 'datout = False'. Then, turn it 'True' when you are 
                     confident with the result.

      e.g., self.cpifsys(whichdat=3)

      output: self.tsys4, self.cpfrom, self.cpto (and .png/.dat files)

      """
      if whichdat == 1:
         datbox = self.tsys1        # raw data
      elif whichdat == 2:
         datbox = self.tsys2        # linear interpolated
      elif whichdat == 3:
         datbox = self.tsys3        # smoothing with n-sigma
      elif whichdat == 4:
         datbox = self.tsys4        # copying neighboring IF
      #
      if datbox:
         pass
      else:
         log("\n\n...No data found! (check the 'whichdat' parameter)"); time.sleep(1.5)
         return
      if whichdat == 4:
         log("\n***** Given data selection (whichdat), it is self-updating ***** \n - For cpifsys, normally you don't need test runs and thus just let 'update=True'.")
      if self.tarr is None:
         log("\n...run 'showsys' first!"); time.sleep(1.5)
         return
      else:
         pass
      new_t = self.tarr
      if reon:
         log("\n!!! Initialize the cpifsys records and re-run from the beginning !!!"); time.sleep(2)
         self.tsys4 = None
         self.cpfrom = []
         self.cpto = []
      else:
         pass
      log("\nAmong -->", self.colids)
      idfrom = input("\nID of an IF to be *COPIED*? (e.g., R1 or R1:2; see output figures) \n:")
      idto = input("\nID of an IF to be *PASTED*? (e.g., L1 or L1:2; see output figures) \n:")
      if idfrom not in self.cpfrom:
         self.cpfrom.append(idfrom)
      if idto not in self.cpto:
         self.cpto.append(idto)
      #
      if self.colnum > 8:
         Hor, Ver = 14.5, 10.5
      elif self.colnum == 8:
         Hor, Ver = 13, 10
      elif self.colnum in [7,6,5]:
         Hor, Ver = 10.5, 8.5
      elif self.colnum in [4,3]:
         Hor, Ver = 9, 7
      elif self.colnum in [2,1]:
         Hor, Ver = 7, 6
      # figure id set
      for D in range(1000):
         figid = randrange(0, 1000)
         if plt.fignum_exists(figid):
            del figid
            continue
         else:
            break
      plt.ioff()
      fig_pol=plt.figure(figid, figsize=(Hor, Ver))
      plt.figure(figid)
      plt.rcParams['legend.frameon'] = 'False'
      plt.rcParams['xtick.labelsize'] = 11
      plt.rcParams['ytick.labelsize'] = 11
      SAVE = []
      LEGEN = self.colids
      numcols = len(LEGEN.split())
      for i in range(numcols):
         if LEGEN.split()[i] in self.cpfrom:
            ccc = 'm'
            extralegd = ' - COPIED'
         elif LEGEN.split()[i] in self.cpto:
            ccc = 'r'
            extralegd = ' - PASTED'
         else:
            if (LEGEN.split()[i].startswith('R')) & ('L' not in LEGEN.split()[i]):
               ccc = '#1f77b4'
            elif (LEGEN.split()[i].startswith('L')) & ('R' not in LEGEN.split()[i]):
               ccc = '#ff7f0e'
            elif ('R' in LEGEN.split()[i]) & ('L' in LEGEN.split()[i]):
               ccc = 'tab:brown'
         LAB = LEGEN.split()[i]
         plt.figure(figid)
         if self.colnum > 8:
            plt.subplot(4, 4, i+1)
         elif self.colnum in [7,8]:
            plt.subplot(4, 2, i+1)
         elif self.colnum in [5,6]:
            plt.subplot(3, 2, i+1)
         elif self.colnum in [3,4]:
            plt.subplot(2, 2, i+1)
         elif self.colnum in [1,2]:
            plt.subplot(2, 1, i+1)
         #
         if LAB == idto:
            for j,k in enumerate(LEGEN.split(), 0):
               if k == idfrom:
                  tsysset = np.genfromtxt(datbox, usecols=2+j, dtype='float')
            log("\n------------------------------------")
            log("{} Single IF has been copied/pasted !".format(LAB))
            log("------------------------------------"); time.sleep(0.1)
         else:
            tsysset = np.genfromtxt(datbox, usecols=2+i, dtype='float')
         #
         SAVE.append(tsysset)
         #% now PLOTTING
         if ccc == 'm':
            plt.plot(new_t, SAVE[-1], markersize=2, marker='o', linewidth=0.8, alpha=1.0, zorder=0, color=ccc, label=LAB+extralegd)
         elif ccc == 'r':
            plt.plot(new_t, SAVE[-1], markersize=2, marker='o', linewidth=0.8, alpha=1.0, zorder=0, color=ccc, label=LAB+extralegd)
         else:
            plt.plot(new_t, SAVE[-1], markersize=2, marker='o', linewidth=0.8, alpha=1.0, zorder=0, color=ccc, label=LAB)
         plt.yticks(fontsize=fontticklab)
         plt.xticks(fontsize=fontticklab)
         #% basic statistical properties
         vav = np.round(np.median(SAVE[-1]), 1)
         vst = np.round(np.std(SAVE[-1]), 1)
         #% plot layout
         opz1 = np.linspace(plt.ylim()[0], plt.ylim()[1], 7)
         thegap = np.abs(np.abs(opz1[-1])-np.abs(opz1[-2]))
         plt.ylim(opz1[0]-thegap*0.0, opz1[-1]+thegap*1.3)
         plt.legend(loc=2, fontsize=fontleg, numpoints=1, markerscale=1.4, labelspacing=0.1, handletextpad=0.5, borderaxespad=0.2, handlelength=1.0, handleheight=0.5, ncol=2, columnspacing=1.2)
         plt.title("*{}* - Median={}K, Std={}K".format(self.antcode,vav,vst), color='r', fontsize=fonttit)
         plt.xlabel("Decimal day", fontsize=fontaxlab)
         plt.ylabel("Tsys [K]", fontsize=fontaxlab)
         plt.tick_params(axis='both', which='major', length=5, direction='in', pad=2, color='k')
         plt.tick_params(axis='both', which='minor', length=3, direction='in', pad=2, color='k')
         plt.minorticks_on()
         plt.tight_layout()
      #% for output results
      plt.figure(figid)
      plt.show()
      plt.ion()
      td,tmh = np.genfromtxt(self.tsys1, usecols=(0,1), unpack=True, invalid_raise=False, missing_values='', usemask=False, dtype=str)
      outdat = []
      for v in range(len(td)):
         newlin = td[v] + " " + tmh[v]
         for y in range(len(SAVE)):
            if y == len(SAVE)-1:
               newlin = newlin + " " + str(SAVE[y][v]) + " \n"
            else:
               newlin = newlin + " " + str(SAVE[y][v])
         outdat.append(newlin)
         del newlin
         continue
      if update == True:
         self.tsys4 = outdat
         log("\nupdate is set 'True', self.tsys4 has been updated!")
      else:
         log("\nupdate is set 'False', keep using previous data in self.tsys4.")
      if autosav == False:
         log("\nautosav is set 'False', thus no output .png file.")
      elif autosav == True:
         plt.figure(figid)
         ffnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys4.png"
         i = 0
         if ffnam in os.listdir():
            log("\nSaving Figure as .png..... the file name exists!  -->  Add a higher number to it")
            for j in range(1000):
               i=i+1
               mfnam = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys4"+"_"+str(i)+".png"
               if mfnam in os.listdir():
                  continue
               else:
                  break
            plt.savefig(mfnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(mfnam))
         else:
            plt.savefig(ffnam, format='png', dpi=150, transparent=False)
            log("\n\n... {} ! \n".format(ffnam))
      if datout == False:
         log("\ndatout is set 'False', thus no output .dat file.")
      elif datout == True:
         if update == False:
            log("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \ndatout is set True, but 'update=False' now. \nThis means that you keep using previous intpsys result. \nTo export the current result, run this again with 'update=True'. \n\nNo output text file made. \n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); time.sleep(1.5)
            return
         outtotext = copy.deepcopy(self.tsys4)
         outtotext.append("/\n")
         outtotext.insert(0, self.HDb)
         outtotext.insert(0, self.HDa)
         outn = self.sesn+'_'+self.bands+"_"+self.antcode+"_Tsys4.dat"
         log("\n\n... {} ! \n".format(outn))
         with open(outn, 'w') as p32:
            p32.writelines(outtotext)
      log("\nMore IFs to be C&P?, run 'cpifsys' again with 'whichdat=4' & 'update=True'.")
      log("\n**DONE** \n..check self + tsys4, cpfrom, cpto and the output files! \
      \n////////////////////////////////////////////////////////////////////////////////")



class vlbaout():
   """
   For '~~cal.vlba', there are tons of all sorts of VLBA metadata.
   You only need Tsys measurements from this file and this class do that.
   Answer what 'vlbaout' asks and find output ANTABs in your working directory.
   Afterwards, you are ready to go through `gentab` for further processing.

   e.g., vlba = vlbaout()

   output: self + (sesn, bands, allbands, antcodes, tsys1, HDtsys, HDgain)

   Products from vlbaout: separate ANTAB files of the individual VLBA antennas.

   """
   def __init__(self):
      self.sesn = None
      self.bands = None
      self.allbands = None
      self.antcodes = None
      self.tsys1 = None
      self.HDtsys = None
      self.HDgain = None
      for i in listdir():
         if os.path.isfile(i):
            log(i)
      log("\n###################################\n###################################")
      log("\n***For VLBA, just follow the steps below***")
      ost1 = input("\n________________________________________________________________________________\
      \nGive the *~cal.vlba* file name (e.g., xxxxacal.vlba) \n: ")
      l1 = open(ost1)
      l2 = l1.readlines()
      ost2 = input("\n________________________________________________________________________________\
      \nGive session ID (e.g., a or b or c or ...) \n: ")
      self.sesn = ost2
      kp1 = []
      for i in l2:
         if 'Tsys information for' in i:
            kp1.append(i.split()[5])
      self.antcodes = kp1
      for j,k in enumerate(l2,0):
         if 'Tsys information for'+' '+kp1[0] in k:
            fromhere = j
            continue
         if 'Tsys information for'+' '+kp1[-1] in k:
            for j1,k1 in enumerate(l2[j:],j):
               if (k1.startswith('/')) and (len(k1.split()) == 1):
                  tohere = j1
                  break
      kp0 = l2[fromhere:tohere+1]
      kp2 = []
      for z in kp0:
         if len(z.split()) > 5:
            if (z.startswith('!')) and (z.split()[4] == 'RCP'):
               if z.split()[2] not in kp2:
                  kp2.append(z.split()[2])
            elif (z.startswith('!')) and (z.split()[4] == 'LCP'):
               if z.split()[2] not in kp2:
                  kp2.append(z.split()[2])
         else:
            continue
      self.allbands = kp2
      log('\nThe following bands are found.')
      log(kp2)
      ost3 = input("\n________________________________________________________________________________\
      \nObserving frequency? (e.g., 3mm or 7mm or ...) \n: ")
      self.bands = ost3
      outn = self.sesn+'_'+'all'+"_"+"VLBA"+"_raw.dat"
      tap = 0
      for i in listdir():
         if os.path.isfile(i):
            if i == outn:
               log("\n\nThe output *raw* data file already exists...!\n")
               tap = 1
               break
      if tap == 0:
         log("\n\n... {} ! \n".format(outn))
         with open(outn, 'w') as p71:
            p71.writelines(kp0)
      print('\n====Filtering out!====')
      ################
      tsysongoing = []
      A = 0
      for i,j in enumerate(kp0, 0):
         if (j.startswith('T')) and (j.split()[0]=='TSYS') and (j.split()[-1]=='/'):
            cup = []
            log("\n...working on... ", self.antcodes[A]); time.sleep(0.6)
            A += 1
            breakindex = None
            moveon = None
            for i1,j1 in enumerate(kp0[i:],i):
               if moveon:
                  break
               if breakindex:
                  if i1 != breakindex-1:
                     continue
                  else:   # when it has arrived at the other band point
                     breakindex = None
                     continue
               else:   # for the first Tsys group of the band of your interest.
                  if len(j1.split()) >= 3:
                     if (j1.startswith('!')) and (j1.split()[2] == ost3):
                        for i2,j2 in enumerate(kp0[i1:],i1):
                           if (len(j2.split()) == 1) and (j2 == '/\n'):
                              tsysongoing.append(cup)
                              del cup
                              moveon = i2
                              break
                           cup.append(j2)
                           if len(kp0[i2+1].split()) >= 3:
                              if (kp0[i2+1].startswith('!')) and (kp0[i2+1].split()[2] in kp2):
                                 if kp0[i2+1].split()[2] != ost3:
                                    breakindex = i2+1
                                    break
                  elif (len(j1.split()) == 1) and (j1 == '/\n'):
                     tsysongoing.append(cup)
                     del cup
                     break
         else:   # only when new VLBA station begins..
            continue
      ##############
      print('\n')
      nodat = []
      for q,w in enumerate(tsysongoing, 0):
         if len(w) == 0:
            log("\n!! No {} data found at --> {} !!".format(ost3, kp1[q])); time.sleep(1.0)
            nodat.append(kp1[q])
      tsysgo = []
      for t in tsysongoing:   # final filtering
         cup2 = []
         for tt in t:
            if tt.startswith('!'):
               continue
            else:
               if '!' in tt:
                  for u,uu in enumerate(tt.split()):
                     if uu == '!':
                        cutline = u
                  tt = ' '.join(tt.split()[:cutline]) + '\n'
               cup2.append(tt)
         tsysgo.append(cup2)
         del cup2
      self.tsys1 = tsysgo
      log("\n\n===================================================================== \
      \nNOTICE: To stop this run, just Press CTRL+C or keep pressing ENTER. \
      \n        But, for any wrong inputs for the headers appearing below, \
      \n        you can modify them later with output text files anyway. \
      \n=====================================================================\n\n"); time.sleep(0.6)
      #
      log("Check the output file ``{}`` and set the INDEX properly (below) \n".format(outn))
      #
      hd2 = input("\n________________________________________________________________________________\
      \nGive a common INDEX line for all VLBA stations          [To skip, press Enter] \n\n(for example) \n INDEX='R1','L1','R2','L2','R3','L3','R4','L4' \n INDEX='R1:2','L1:2','R3:4','L3:4','R5:6','L5:6','R7:8','L7:8' \n\n: ")
      lct1 = []
      lct2 = []
      for i in kp0:
         if len(i.split()) > 1:
            if (i.startswith('T')) & (i.split()[0]=='TSYS'):
               log('\n!!!!!!!!!!!!!!!!!!!!!!!!! NEW ANTENNA !!!!!!!!!!!!!!!!!!!!!!!!!')
               log(i)
               if i.split()[1] in nodat:
                  log("\n...no it's empty at this band, SKIP IT! \n"); time.sleep(2)
                  lct1.append('None')
                  lct2.append('None')
                  continue
               else:
                  hd1 = input("\n________________________________________________________________________________\
                        \n**{}**                                  (skip and do it later? then just Enter) \nMake a TSYS line (e.g., TSYS BR timeoff=0 FT=1.0) \n: ".format(i.split()[1]))
                  hdb = hd1 + ' ' + hd2 + ' /\n'
                  lct1.append(hdb)
                  hd3 = input("\n________________________________________________________________________________\
                        \n**{}**                                  (skip and do it later? then just Enter) \nMake a GAIN line without POLY \n--> e.g., GAIN KP ALTAZ DPFU=0.XX,0.XX FREQ=XX,XX \n--> FREQ can be omitted (optional) \
                        \n--> Check the 'vlba_gains_xxxxxx.key' file for this! \n: ".format(i.split()[1]))
                  hd4 = input("\n________________________________________________________________________________\
                        \n**{}**                                  (skip and do it later? then just Enter) \nMake a POLY line \n--> e.g., POLY=0.5190,-0.0382429,,0.00510852 or POLY=1.0 \
                        \n--> Check the 'vlba_gains_xxxxxx.key' file for this!*** \n: ".format(i.split()[1]))
                  hda = hd3 + ' ' + hd4 + ' /\n'
                  lct2.append(hda)
      self.HDtsys = lct1
      self.HDgain = lct2
      bwc = []
      for y in tsysgo:   # are there multiple bandwidth in this band?
         for x in y:
            if x[0].isdigit():
               cp1 = len(x.split()) - 2
               if cp1 in bwc:
                  continue
               else:
                  bwc.append(cp1)
      if len(bwc) != 1:
         log("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n ...# of Tsys columns varies in this band (e.g., more than one bandwidth). \n ...Check the output raw data carefully and answer the following question. \n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); time.sleep(1.5)
         log("\n*Number of Tsys columns:", bwc)
         CHOICE = input("\nAmong printed above, which one is the correct one? \n(if you need all of them, then just type 'pass') \n: ")
         if CHOICE == 'pass':
            pass
         else:
            tsysgo2 = []
            for v in tsysgo:
               tsyselm = []
               for vv in v:
                  if vv[0].isdigit():
                     if len(vv.split()) == int(CHOICE) + 2:
                        tsyselm.append(vv)
                  else:
                     continue
               tsysgo2.append(tsyselm)
               del tsyselm
            del tsysgo
            tsysgo = tsysgo2
            self.tsys1 = tsysgo2
      for p,s in enumerate(kp1, 0):
         if s in nodat:
            log("\n****************************No data, so SKIP {}****************************".format(s))
            continue
         else:
            log("\nExporting {} ... done!".format(s))
            outtotext = copy.deepcopy(tsysgo[p])
            outtotext.append("/\n")
            outtotext.insert(0, lct1[p])
            outtotext.insert(0, lct2[p])
            outn = self.sesn+'_'+self.bands+"_"+s+"_vlbaout.antab"
            log("\n... {} !".format(outn))
            with open(outn, 'w') as p63:
               p63.writelines(outtotext)
      log("\n\n**DONE** \nFine output Text files for each VLBA station in the working directory! \
      \n..check self + sesn, bands, allbands, antcodes, tsys1, HDtsys, HDgain \
      \n////////////////////////////////////////////////////////////////////////////////")



def wxgen(skipvlba=False):
   """
   To generate a single 'All-in-One' WX data file.
   This new function is the same as 'allinone', but for WX datasets.

   <Param>
    skipvlba : True, if you do not have VLBA data (e.g., c222acal.vlba).
               Default: False (means you have VLBA in your data).

   e.g., wxgen() or wxgen(skipvlba=True)

   output: Single WX file in the working directory.

   """
   if skipvlba == False:
      VLBAONLY = []
      emptyones = []
      for i1 in listdir():
         if os.path.isfile(i1):
            log(i1)
      log('\n********************** \nLets begin with VLBA.. \n**********************'); time.sleep(1)
      q1 = input("\nGive VLBA wx-files (e.g., c222acal.vlba) \n: ")
      o1 = open(q1.split()[0])
      o2 = o1.readlines()
      x1 = 0
      antlist = []
      linehead = []
      log("   ")
      for i2 in o2:
         if "Weather information for " in i2:
            x1 += 1
            log(x1, i2)
            antlist.append(i2.split()[5])
            linehead.append("WEATHER {} /\n".format(i2.split()[5]))
      q2 = input("\nCorrect? (press Enter) \n")
      for i3 in range(len(antlist)):
         log('\n......working on *{}*'.format(antlist[i3]))
         newlab = 0
         for i5,j5 in enumerate(o2, 0):
            if "Weather information for " + antlist[i3] in j5:
               goindex = 0; newbegin = None; newend = None
               for i6,j6 in enumerate(o2[i5+1:],i5+1):
                  if j6.split()[0][0].startswith('*'):
                     if goindex == 0:
                        if "Weather information for " in j6:
                           log('\n** No data found at {}! **\n'.format(antlist[i3])); time.sleep(2)
                           emptyones.append(i3)
                           break
                        else:
                           continue
                     else:
                        newend = i6
                        break
                  elif j6.split()[0][0].isdigit():
                     if goindex == 0:
                        newbegin = i6
                        goindex = 1
                        continue
                     else:
                        if i6 == len(o2)-1:
                           newend = i6 + 1
                           break
                        else:
                           continue
               if goindex == 0:
                  VLBAONLY.append(None)
                  continue
               else:
                  VLBAONLY.append(o2[newbegin:newend])
      MERGe = []
      for i3 in range(len(antlist)):
         if i3 in emptyones:
            continue
         else:
            MERGe.append(linehead[i3])
            MERGe = MERGe + VLBAONLY[i3]
            MERGe.append("/ \n")
      outnam = input("\nGive output file name (e.g., C222A_VLBA.WX) \n:")
      log("\n\n... {} ! \n".format(outnam))
      with open(outnam, 'w') as rd12:
         rd12.writelines(MERGe)
      # /////////////////////////////////////////////////////// new era
      for i in range(1000):
         GORTOP = input("\nCombine other WX data (e.g., EU ants.) into the VLBA data? (y or n) \n:")
         if GORTOP == 'y':
            break
         elif GORTOP == 'n':
            log("\nThat's it! (only VLBA)")
            return
         else:
            log("\n...wrong input! Give either y or n.")
            continue
      OTHERANT = []
      for k0 in range(1000):
         log('\n\n====================================')
         for k1 in listdir():
            if os.path.isfile(k1):
               if k1 not in OTHERANT:
                  log(k1)
         log('====================================')
         log("\n*Selected below*\n-->", OTHERANT)
         NEXTANT = input("\nOne-by-one, select all the other WX files \n(type 'done' if all are given) \n(type 're' if you gave a wrong input) \n:")
         if NEXTANT == 'done':
            break
         elif NEXTANT == '':
            log("\n...wrong input! Re-try (e.g., WX.c222aef.log)"); time.sleep(1.5)
            continue
         elif NEXTANT == 're':
            del OTHERANT[-1]
            continue
         else:
            OTHERANT.append(NEXTANT)
            del NEXTANT
            continue
      for z in OTHERANT:
         u1 = open(z)
         u2 = u1.readlines()
         newhd = 'WEATHER ' + u2[0].split()[1].upper() + ' /\n'
         u3 = u2[1:-1]
         MERGe.append(newhd)
         MERGe = MERGe + u3
         MERGe.append("/ \n")
      outnam = input("\nGive output file name (e.g., C222A_ALLANT.WX) \n:")
      log("\n\n... {} ! \n".format(outnam))
      with open(outnam, 'w') as rd13:
         rd13.writelines(MERGe)
      log("\nFinished!"); time.sleep(1)
   # ............................................... without VLBA
   else:   # e.g., skipvlba=True
      OTHERANT = []
      MERGe = []
      for k0 in range(1000):
         log('\n\n====================================')
         for k1 in listdir():
            if os.path.isfile(k1):
               if k1 not in OTHERANT:
                  log(k1)
         log('====================================')
         log("\n*Selected below*\n-->", OTHERANT)
         NEXTANT = input("\nOne-by-one, select all WX files you want to combine - *without VLBA* \n(type 'done' if all are given) \n(type 're' if you gave a wrong input) \n:")
         if NEXTANT == 'done':
            break
         elif NEXTANT == '':
            log("\n...wrong input! Re-try (e.g., WX.c222aef.log)"); time.sleep(1.5)
            continue
         elif NEXTANT == 're':
            del OTHERANT[-1]
            continue
         else:
            OTHERANT.append(NEXTANT)
            del NEXTANT
            continue
      for z in OTHERANT:
         u1 = open(z)
         u2 = u1.readlines()
         newhd = 'WEATHER ' + u2[0].split()[1].upper() + ' /\n'
         u3 = u2[1:-1]
         MERGe.append(newhd)
         MERGe = MERGe + u3
         MERGe.append("/ \n")
      outnam = input("\nGive output file name (e.g., C222A_NONVLBA.WX) \n:")
      log("\n\n... {} ! \n".format(outnam))
      with open(outnam, 'w') as rd13:
         rd13.writelines(MERGe)
      log("\nFinished!"); time.sleep(1)



