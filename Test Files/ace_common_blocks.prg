
; the following are the collection of common blocks used in the atmospheric chemistry and energetic (ace)
; software

 common ace_common,nbins,nmaj,nei,nst,jmax,lmax,sigs,pe,pi,siga,sec,sigex,sigix,tpot,prob,$
        ener,del,peflux,primary,sigloss,iimax,upflux,downflux,toaflux,$
        wv1,wv2,ssflux,$
       sigabs,sigionx,auger_energy,auger_wvln,$
        zmaj,zz,z,zt,$
        lat,sza,idate,utsec,f107,f107a,ap,$
        first_neutral,first_ssflux,first_pxsect,first_exsect, $
        zcol,tau,flux,photoki,photoi,aprod,aloss,$
        ww,a0,omeg,anu,bb,auto,thi,ak,aj,gams,gamb,ts,tb, ta, eistates,$
        eden,etemp,$
        eiionz,eiionzk,eiexcit,vem5577,vem6300,vem2972,n2a,o1d,o1s
        
       
;C Definitions:
;C SIGS   elastic cross sections for each species, energy; cm2
;C PE     elastic backscatter probabilities for each species, energy
;C PI     inelastic  "
;C SIGA   energy loss cross section for each species, loss, energy; cm2
;C SEC    secondary production xsect for species, Esec, Epri; cm2
;C SIGEX  excitation xsect for each state, species, energy; cm2
;C SIGIX  ionization xsect for each state, species, energy; cm2
;C IIMAX  number of bins for secondary production for each primary energy
;C WW     energy threshold for each excited state, species; eV
;C WW, AO, OMEG, ANU, BB: revised excitation cross section parameters,
;C        from Green & Stolarski (1972) formula (W, A, omega, nu, gamma)
;C AUTO   autoionization coefs (= 0 as autoion. included in ion xsects)
;C THI    energy threshold for each ionized state, species; eV
;C AK, AJ, TS, TA, TB, GAMS, GAMB:  Jackman et al (1977) ioniz. params
;C ENER   energy grid; eV
;C DEL    energy grid spacing; eV
;C NNN    number of excited states for each species
;C NINN   number of ionized states for each species
;C NUM    number of points on elastic data trid for each species
;C EC     data energy grid of elastic xsects and backscatter ratios
;C        for each species; eV
;C CC     elastic xsects on data grid for each species, cm2
;C CE     elastic backscat. probs on data grid for each species; cm2
;C CI     inelastic "
;C
;C Array dimensions:
;C NBINS  number of energy levels
;C NMAJ   number of major species
;C NEI    number of slots for excited and ionized states

    
 ; NMAJ   number of major species
 ; NEI    number of slots for excited and ionized states
 ;ww=dblarr(nei,nmaj)