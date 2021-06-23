import requests
import re
import time
import math
import matplotlib
import matplotlib.pyplot as plt
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def main ():
 driver = webdriver.Chrome(ChromeDriverManager().install())
 exo = open("C:\\Users\\ThinkPad\\Documents\\Exoplanets.txt","r+")
 specexo = exo.readlines()

 pnamestd = open("Planets and Square Root of Standard Deviations.txt", mode='w+', encoding='utf-8')
 pnamestd.write('Planet;Sqrt(Std Dev) in minutes;Number of Data Points\n')

 for i in range (358, 365):
  csexo = specexo[i] #planet link
  pname = specexo[i] #planet name
  pname = pname.replace('/','~')
  csexo = csexo.replace(' ','&')
  csexo = csexo.replace('EPIC&218916923&b', 'EPIC%20218916923&b')
  csexo = csexo.replace('EPIC&228735255&b', 'EPIC%20228735255&b')
  csexo = csexo.replace('WD&1145+017&b','WD%201145%2B017&b')
  csexo = csexo.replace('55&C','55%20C')
  csexo = csexo.replace('KOI&','KOI%20')
  csexo = csexo.replace('TOI&00392.01','TOI%20%2000392.01')
  csexo = csexo.replace('TOI&00624.01','TOI%20%2000624.01')
  csexo = csexo.replace('TOI&00627.01','TOI%20%2000627.01')
  csexo = csexo.replace('TOI&00294.01','TOI%2000294.01')
  csexo = csexo.replace('TOI&00469.01','TOI%2000469.01')
  csexo = csexo.replace('TOI&00498.01','TOI%2000498.01')
  csexo = csexo.replace('TOI&00503.01','TOI%2000503.01')
  csexo = csexo.replace('TOI&00522.01','TOI%2000522.01')
  csexo = csexo.replace('TOI&01012.01','TOI%2001012.01')
  csexo = csexo.replace('TOI&01164.01','TOI%2001164.01')
  csexo = csexo.replace('TOI&1','TOI%201')
  for x in range (len(csexo)):
   if x == 0:
    csexo = 'http://var2.astro.cz/ETD/etd.php?STARNAME='+csexo
  for x in range (len(csexo)):
   if x == len(csexo)-2:
    csexo = csexo[:x]+'PLANET='+csexo[x:]
  pname = pname[:-1]
  print (pname)
  driver.set_page_load_timeout(40)
  driver.get(csexo)
  driver.find_element(By.PARTIAL_LINK_TEXT,'Show data as ASCII table separated by semicolon').click()
  econtent = requests.get(driver.current_url).text
  exosoup = BeautifulSoup(econtent, "lxml")
  exostring = str(exosoup)
  with open('./{}.txt'.format(pname), mode='w', encoding='utf-8') as file:
   file.write(exostring)
  
  pnamef = open(pname+'.txt', mode='r', encoding='utf-8')
  c = 0
  Epvalues = [] #initializes Epvalues, the collection of epoch values
  OCvalues = [] #initializes OCvalue, the collection of O-C values
  while True:
   c+=1
   pline = pnamef.readline() #a line in a given text file
   sccounter = 0 #semicolon counter
   Epstart = 0 #nth character in pline that is the 3th semicolon (to record Epoch value's start character)
   OCstart = 0 #nth character in pline that is the 4th semicolon (to record O-C value's start character)
   OCend = 0 #nth character in pline that is the 5th semicolon (to record O-C value's end character)
   count = 0 #random variable that helps prevent confusion in the program with OCend and OCstart
   for i in range(0,len(pline)): #this section takes care of finding the O-C values
     if pline[i] == ';':
      sccounter+=1
      if sccounter == 3 and count == 0:
       Epstart = i
       count+=1
      if sccounter == 4 and count == 1:
       OCstart = i
       count+=1
      if sccounter == 5 and count == 2:
       OCend = i
       count+=1
   if not pline:
     break
   Epval = pline[Epstart+1:OCstart]
   if len(Epval) != 0 and Epval != 'Epoch':
    Epvalues.append(float(Epval))
   OCval = pline[OCstart+1:OCend]
   if len(OCval) != 0 and OCval != 'O-C':
    OCvalues.append(float(OCval)*1440)

  print('The mean of O-C values for ', pname, ' is ', round(findmean(OCvalues),1))
  print('The standard deviation of O-C values for ', pname, ' is ', round(findstd(OCvalues),1), '\n')  

  pandstd = pname
  if len(OCvalues) < 5:
   pandstd = pandstd + ';Not enough data points!;' + str(len(OCvalues)) + '\n'
  else:   
   pandstd = pandstd + ';' + str(findstd(OCvalues)) + ';' + str(len(OCvalues)) + '\n'

  pnamestd.write(pandstd)

  #plt.ion()
  plt.scatter(Epvalues, OCvalues, c='blue')
  
  plt.title('O-C (min) vs Epoch for ' + pname)
  plt.xlabel('Epoch')
  plt.ylabel('O-C (min)')
  #plt.errorbar(Epvalues, OCvalues, yerr = 0.000001, fmt='o')
  plt.show()
  plt.close('O-C (min) vs Epoch')
  plt.savefig(pname+'.png')

 time.sleep(2) 
 driver.quit()
 exo.close()
 pnamestd.close()

def findmean (OCvalues):
 OCmean = 0
 for i in OCvalues:
  OCmean+=i
 if len(OCvalues) == 0:
  OCmean = OCmean/1
 else: 
  OCmean = OCmean/len(OCvalues) #arithmetic mean of O-C values
 return OCmean
 
def findstd (OCvalues):
 OCstd = 0
 OCsqrdmmmean = 0 #used as a step in calculating OCstd (mean of the differences squared)
 OCmean = findmean(OCvalues)
 for i in OCvalues:
  OCsqrdmmmean+=((i-OCmean)**2)
 if len(OCvalues) == 0:
  OCstd = math.sqrt(OCsqrdmmmean)
 else:
  OCstd = math.sqrt(OCsqrdmmmean/len(OCvalues)) #standard deviation of O-C values
 return OCstd

main()
