import numpy


pro localpe,localpe_idate,localpe_lat,localpe_hour,localpe_zz,localpe_ener,localpe_pespec,localpe_del,demo=demo

# This is the photoelectron local calculation written jointly by the Aeronomy Group at 
# Virginia Tech in April of 2010-January 2013

# as of this date, the code is not validated, but has been shown to be approximately correct
# user should be cautioned

import ace_common_blocks.py
 # common blocks used for all atmospheric chemistry & energetics (ace) software
ace_common_blocks.initialize()# see this file for definitions
 
idate=localpe_idate
lat=localpe_lat
hour=localpe_lat

#JMAX    number of altitude levels
#LMAX    number of wavelength intervals for solar flux
#NMAJ    number of major species
#NEI     number of states produced by electron impact
#NBINS   number of energetic electron energy bins
#NST     number of states produced by photoionization/dissociation
#TAU     optical depth, dimensionless
#SIGABS  photoabsorption cross sections, O, O2, N2# cm2
#ZCOL    slant column density for species O, O2, N2, altitude# cm-2
#WV1   wavelength array, upper bound# Angstroms
#WV2   wavelength array, lower bound# Angstroms
#ZMAJ    density array for species O, O2, N2, altitude# cm-3
# PROB    branching ratios for each state, species, & wavelength bin:
#         O+ states: 4S, 2Do, 2Po, 4Pe, 2Pe
#         O2+ states: X, a+A, b, dissoc.
#         N2+ states: X, A, B, C, F, dissoc.
#TPOT    ionization potentials for each species, state# eV


pespec=numpy.zeroes(jmax,nbins)
aprod=pespec
aloss=aprod
sion=numpy.zeroes(nmaj,jmax)
 
# main loop over altitude (then primary energy) for photoelectron calculation
for iz in range(0, jmax):

    thermalcasc=numpy.zeroes(nbins)   
# start with highest bin that has production in it
firstbin=nbins-1
indp=(primary[iz).nonzero()	#
indp = indp[0]
*] > 0.,n_indp = len(indp)
if n_indp > 0: firstbin=indp[len(indp)-1]
     iener=firstbin,2,-1 
# ADD FUNCTIONALITY
        if iener == firstbin :
# now look at highest energy production where production comes only from
# primary
    prod=primary[iz,iener]/del[iener]
    loss=0.
            
    # loss to thermals
    ee=8.618e-5*etemp[iz]
    dag=ener[iener]-ener[(iener-1)>0]
    l2thermals=(eden[iz] * 3.37e-12*(((ener[iener]-ee)/(ener[iener]-0.53*ee))**2.36)/(ener[iener]**0.94)/(eden[iz]**0.03))>0.
    loss = loss + l2thermals/dag
            
         imaj=0,nmaj-1 do loss=loss+zmaj[imaj,iz]*sigloss[imaj,iener]
# ADD FUNCTIONALITY             
            if loss > 0.: pespec(iz,iener) = prod / loss
            aprod[iz,iener]=prod
            aloss[iz,iener]=loss
            
            #calculate all the cascade production in all lower bins as a result of this energy bin
            cascprod=numpy.zeroes(nmaj,nbins)
                for ilower in range(0, iener):
                    icasc=iener-ilower
                     imaj=0,nmaj-1 do cascprod[imaj,icasc]=cascprod[imaj,icasc]+zmaj[imaj,iz]*pespec[iz,iener]*siga[imaj,ilower,iener]
# ADD FUNCTIONALITY                               
               
                             else begin

                                prod=primary[iz,iener]/del[iener]+thermalcasc[iener]
            
                                for imaj in range(0, nmaj):
                                    prod=prod+cascprod[imaj,iener]
                                         iupper=nbins-1,iener,-1 
# ADD FUNCTIONALITY                                            prod=prod+zmaj[imaj,iz]*pespec[iz,iupper]*sec[imaj,iener,iupper]
                                            sion[imaj,iz]=sion[imaj,iz] + zmaj[imaj,iz]*pespec[iz,iupper]*sec[imaj,iener,iupper]
                                                
                                            
           
                                                loss=0.
            
                                                    # loss to thermals
                                                ee=8.618e-5*etemp[iz]
                                                dag=ener[iener]-ener[(iener-1)>0]
                                                d1=(ener[iener]-ee)>0.
                                                d2=(ener[iener]-0.53*ee)>0.
                                                l2thermals=(  eden[iz] * 3.37e-12 * ((d1/d2)**2.36)   /  (ener[iener]**0.94)  /  (eden[iz]**0.03)       >0.  )
                                                loss = loss + l2thermals/dag
            
                                                     imaj=0,nmaj-1 do loss=loss+zmaj[imaj,iz]*sigloss[imaj,iener]
# ADD FUNCTIONALITY             
                                                if loss > 0.: pespec(iz,iener) = prod / (loss>1e-34) # 1e-34 to make sure we don't get floating point errors
                                                aprod[iz,iener]=prod
                                                aloss[iz,iener]=loss

                                            # if iz eq 105 & iener eq 35 then print,zz[iz],ener[iener],eden[iz],etemp[iz],l2thermals,l2thermals/dag,loss

                                                #calculate all the cascade production in all lower bins as a result of this energy bin
                                                #cascprod=numpy.zeroes(nmaj,nbins)
                                                    for ilower in range(0, iener):
                                                        icasc=iener-1-ilower
                                                         imaj=0,nmaj-1 do cascprod[imaj,icasc]=cascprod[imaj,icasc]+zmaj[imaj,iz]*pespec[iz,iener]*siga[imaj,ilower,iener]
# ADD FUNCTIONALITY                                                           
             
                                if iener > 1: thermalcasc[iener-1]=l2thermals*pespec[iz,iener] * del[iener]/del[iener-1]  
                            
                                    endelse
                        #

               # loop over energy
            #loop over altitude
   
            localpe_zz=zz
            localpe_ener=ener
            localpe_pespec=pespec
            localpe_del=del
#stop
return
end
