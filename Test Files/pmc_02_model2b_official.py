# -*- coding: utf-8 -*-
"""
Created on Mon May 21 20:00:50 2018

@author: Scott
"""

# =============================================================================
# #-------------------------------------------------------
# #  purpose:
# #     Routine computes various properties of ice assuming bulk thermodynamic equilibrium. 
# #     The user inputs profile data and gets back various profiles plus some scalars.     
# #
# #  input:
# #     z.......altitude (km), fltarr(nz)
# #     t.......temp (K), fltarr(nz)
# #     p.......pressure (mb), fltarr(nz)
# #     h2o.....h2o mixing ratio (ppmv), fltarr(nz)
# #
# #     vpop....saturation vapor pressure option:
# #              1 = use Murphy & Koop [2005]  (this is very close to Marti & Mauersberger [1993])
# #              2 = use Mauersberger & Krankowsky [2003], here the math.expression for T < 169K is used
# #              3 = use Marti & Mauersberger [1993]
# #
# #     Note: the input Z, T, P, & H2O must all have the same dimension
# #
# #  output:
# #     t_ice......frost point temperature (K), fltarr(nz)
# #     p_ice......saturation vapor pressure over ice (mb), fltarr(nz)
# #     s_ice......saturation ratio WRT ice (unitless), fltarr(nz)
# #     h2o_sat....saturation H2O mixing ratio (ppmv), fltarr(nz)
# #     v_ice......ice volume density (um3 / cm3), fltarr(nz)
# #     m_ice......ice mass density (ng / m3), fltarr(nz)
# #     h2o_ice....gas phase equivalent H2O in ice (ppmv), fltarr(nz)
# #     ztop.......ice layer top altitude (km)
# #     zmax.......ice layer mass density peak altitude (km) (same as SOFIE zmax, which are based on IR extinction)
# #     zbot.......ice layer bottom altitude (km)
# #     iwc........column ice abundance (ug/m2 = g/km3) 
# #
# #  Source:    Mark Hervig, GATS Inc.
# #  Revision:  4/3/09
# #             9/20/2011,  added rc
# #
# #             1/28/13, MEH removed T cutoff of 180 (line 83), modified Tice calculation (lines 130-)
# #             to span 50 - 1000K (p_sat (or p_ice) vs t calculated on lines 81-).  
# #             Note this is abusing the P_sat math.expressions.
# #             
# #             1/1/13, MEH, removed lines for capacitance and kelvin terms
# #             5/19/15, MEH, removed scale factor option, removed rc
# #-------------------------------------------------------------   
# =============================================================================

# Use these for math functionality - GF
import numpy

#pro pmc_0d_model2b,z,p,t,h2o,vpop,t_ice,p_ice,s_ice,h2o_sat,v_ice,m_ice,h2o_ice,ztop,zmax,zbot,iwc,constdz=constdz

def pmc_02_model2b(z,p,t,h2o,vpop, constdz = None):

  # All lists/vectors must be numpy arrays in order for where/non-zero
  #     to function properly. This reformats in case user does not - GF
  z = numpy.asarray(z)
  p = numpy.asarray(p)
  t = numpy.asarray(t)
  h2o = numpy.asarray(h2o)



  # Constants
  Mww = 18.0        # molec wt. h2o, g/mol
  di  = 0.93        # density of ice, g/cm3
  R   = 8.314       # J/mol/K
  Sti = 0.12        # surface tension of ice in the presence of air, J/m2

  #- Housekeeping 
  nz = len(z)
   
  if ((vpop < 1) | (vpop > 3)):
    print('vpop not valid in pmc_0D_model2b.pro')
    exit()

  t_ice   = numpy.zeros(nz) 
  p_ice   = numpy.zeros(nz)
  s_ice   = numpy.zeros(nz)
  v_ice   = numpy.zeros(nz)
  m_ice   = numpy.zeros(nz)
  h2o_sat = numpy.full(nz, 999)
  h2o_ice = numpy.zeros(nz)   
   
  zmax = 0
  ztop = 0
  zbot = 0
  iwc  = 0

  #- Generate a range of saturation vapor pressure (px) vs. T (tx), for use below
  tx = numpy.arange(300)*3 + 50  # (huge) range of temperatures

  if (vpop == 1):
    px = 0.01*numpy.exp(9.550426-(5723.265/tx)+(3.53068*numpy.log(tx))-(0.00728332*tx))  
  if (vpop == 2):
    px = 0.01*10**(14.88-(3059.0/tx))    
  if (vpop == 3):
    px = 0.01*numpy.exp(28.868 - (6132.935 / tx))
 
  #- Loop over altitude
  for i in range(0, nz):

    if (t[i] > 0):
      
      #-   Saturation vapor pressure at T,  Kelvin term if r > 0
      if (vpop == 1):
        p_ice[i] = 0.01*numpy.exp(9.550426-(5723.265/t[i])+(3.53068*numpy.log(t[i]))-(0.00728332*t[i]))    
      if (vpop == 2):
        p_ice[i] = 0.01*(10**(14.88-(3059.0/t[i])))
      if (vpop == 3):
        p_ice[i] = 0.01*numpy.exp(28.868 - (6132.935/t[i]))      
   
      #-   Saturation mixing ratio, etc...
      h2o_sat[i]  = (10**6)*p_ice[i]/p[i]  # saturation mixing ratio, ppmv
      s_ice[i] = h2o[i]/h2o_sat[i]      # saturation ratio
        
      #-  Equilibrium ice properties
      q_xs = h2o[i] - h2o_sat[i]    # excess h2o mix ratio, ppmv      
       
      if (q_xs > 0):     # if saturated then go on
        n_xs = p[i]*(10**2)*q_xs*(10**(-6))/(R*t[i])  # excess mols h2o per m3 air         
        v_ice[i] = (10**6)*n_xs*Mww/di   # ice volume density, microns3 / cm3     
        m_ice[i] = (10**9)*n_xs*Mww        # ice mass density, ng/m3       
        h2o_ice[i] = q_xs                    # H2O(ice), ppmv

      #-   Find the frost point temperature, t_ice.  Use the fact that
      #    a linear relationship exists between 1/T and math.log10(p_h2o).
      #    Do a linear interpolation between some hi and low temp.

      p_h2o = p[i]*h2o[i]*(10**(-6))  # h2o partial pressure, mb
     
      p1 = 0
      t1 = 0
      p2 = 0 
      t2 = 0
          
      #k  = (px < p_h2o).nonzero()  # find the p & t just below p_h2o
      k = (px < p_h2o).nonzero()
      k = k[0] # this is needed to get the result from .nonzero() - GF
      n = len(k)
      if n > 0:     
        p1 = px[k[n-1]]
        t1 = tx[k[n-1]] 
      #k  = (px >= p_h2o).nonzero()  # find the p & t just above p_h2o
      k  = (px >= p_h2o).nonzero()  # find the p & t just above p_h2o
      k  = k[0]
      n = len(k)
      if n > 0:
        p2 = px[k[0]]
        t2 = tx[k[0]]
      if ((p_h2o >= min(px)) & (p_h2o <= max(px)) & (p1 > 0) & (p2 > 0)): 
        dsds  = (numpy.log10(p2) - numpy.log10(p_h2o))/(numpy.log10(p2) - numpy.log10(p1))
        t_ice[i] = 1/((1/t2)-(dsds*((1/t2) - (1/t1))))

#- Find zmax, ztop, zbot, IWC
  k = ((z > 80) & (z < 95) & (m_ice > 0)).nonzero()
  k = k[0]
  nk = len(k)
  if (nk > 0): 
    l = (m_ice[k] == max(m_ice[k])).nonzero()
    l = l[0] 
    l = k[l[0]]
    zmax = z[l]       
    ztop = max(z[k])
    zbot = min(z[k])
   
    if constdz is not None:
      dz=abs(z[1]-z[0])
   
    for i in range(0, nk):
      if ( z[k[i]] > zmax-2):           
        if (constdz is None): 
          dz  = abs( z[k[i]+1] - z[k[i]-1])*0.5  # layer spacing (km)       
        iwc = iwc + m_ice[k[i]]*dz            # micro-g/m2 = g/km3  
      

  return {
    'iwc': iwc, 
    't_ice': t_ice, 
    'p_ice' : p_ice, 
    's_ice' : s_ice, 
    'h2o_sat':h2o_sat, 
    'v_ice':v_ice, 
    'm_ice':m_ice, 
    'h2o_ice': h2o_ice, 
    'ztop':ztop,
    'zmax':zmax,
    'zbot':zbot
    }
