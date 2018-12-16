
;-------------------------------------------------------
;  purpose:
;     Routine computes various properties of ice assuming bulk thermodynamic equilibrium. 
;     The user inputs profile data and gets back various profiles plus some scalars.     
;
;  input:
;     z.......altitude (km), fltarr(nz)
;     t.......temp (K), fltarr(nz)
;     p.......pressure (mb), fltarr(nz)
;     h2o.....h2o mixing ratio (ppmv), fltarr(nz)
;
;     vpop....saturation vapor pressure option:
;              1 = use Murphy & Koop [2005]  (this is very close to Marti & Mauersberger [1993])
;              2 = use Mauersberger & Krankowsky [2003], here the expression for T < 169K is used
;              3 = use Marti & Mauersberger [1993]
;
;     Note: the input Z, T, P, & H2O must all have the same dimension
;
;  output:
;     t_ice......frost point temperature (K), fltarr(nz)
;     p_ice......saturation vapor pressure over ice (mb), fltarr(nz)
;     s_ice......saturation ratio WRT ice (unitless), fltarr(nz)
;     h2o_sat....saturation H2O mixing ratio (ppmv), fltarr(nz)
;     v_ice......ice volume density (um3 / cm3), fltarr(nz)
;     m_ice......ice mass density (ng / m3), fltarr(nz)
;     h2o_ice....gas phase equivalent H2O in ice (ppmv), fltarr(nz)
;     ztop.......ice layer top altitude (km)
;     zmax.......ice layer mass density peak altitude (km) (same as SOFIE Zmax, which are based on IR extinction)
;     zbot.......ice layer bottom altitude (km)
;     iwc........column ice abundance (ug/m2 = g/km3) 
;
;  Source:    Mark Hervig, GATS Inc.
;  Revision:  4/3/09
;             9/20/2011,  added rc
;
;             1/28/13, MEH removed T cutoff of 180 (line 83), modified Tice calculation (lines 130-)
;             to span 50 - 1000K (p_sat (or p_ice) vs t calculated on lines 81-).  
;             Note this is abusing the P_sat expressions.
;             
;             1/1/13, MEH, removed lines for capacitance and kelvin terms
;             5/19/15, MEH, removed scale factor option, removed rc
;-------------------------------------------------------------   
 

#pro pmc_0d_model2b,z,p,t,h2o,vpop,t_ice,p_ice,s_ice,h2o_sat,v_ice,m_ice,h2o_ice,Ztop,Zmax,Zbot,iwc,constdz=constdz
;- Constants

  z = input
  t = input
  p = input
  h2o = input
  vpop = input



   Mww = 18.0        ; molec wt. h2o, g/mol
   di  = 0.93        ; density of ice, g/cm3
   R   = 8.314       ; J/mol/K
   Sti = 0.12        ; surface tension of ice in the presence of air, J/m2

;- Housekeeping
   
   nz = n_elements(z)
   
   if (vpop lt 1 or vpop gt 3) then stop,'vpop not valid in pmc_0D_model2b.pro'

   t_ice   = dblarr(nz) 
   p_ice   = dblarr(nz)
   s_ice   = dblarr(nz)
   v_ice   = dblarr(nz)
   m_ice   = dblarr(nz)
   h2o_sat = dblarr(nz) + 999
   h2o_ice = dblarr(nz)   
   
   Zmax = 0.
   Ztop = 0.
   Zbot = 0.
   iwc  = 0.

;- Generate a range of saturation vapor pressure (px) vs. T (tx), for use below

   tx = findgen(300) * 3. + 50.  ; (huge) range of temperatures
          
   if (vpop eq 1) then px = 0.01*exp(9.550426-5723.265/tx+3.53068*alog(tx)-0.00728332*tx) 
   if (vpop eq 2) then px = 0.01*10^(14.88-3059.0/tx)  
   if (vpop eq 3) then px = 0.01*exp(28.868 - 6132.935 / tx)
   
;- Loop over altitude

   for i = 0,nz-1 do begin

    if (t(i) gt 0) then begin

;-   Saturation vapor pressure at T,  Kelvin term if r > 0
     
     if (vpop eq 1) then p_ice(i) = 0.01*exp(9.550426-5723.265/t(i)+3.53068*alog(t(i))-0.00728332*t(i))    
     if (vpop eq 2) then p_ice(i) = 0.01*10^(14.88-3059.0/t(i))
     if (vpop eq 3) then p_ice(i) = 0.01*exp(28.868 - 6132.935 / t(i))      
   
;-   Saturation mixing ratio, etc...

     h2o_sat(i)  = 1d6 *p_ice(i) / p(i)  ; saturation mixing ratio, ppmv
     
     s_ice(i) = h2o(i) / h2o_sat(i)      ; saturation ratio
        
;-   Equilibrium ice properties

     q_xs = h2o(i) - h2o_sat(i)    ; excess h2o mix ratio, ppmv      
     
     if (q_xs gt 0.0) then begin     ; if saturated then go on
     
       n_xs = p(i)*1d2 *q_xs*1d-6/(R*t(i))  ; excess mols h2o per m3 air
       
       v_ice(i) = 1d6 * n_xs * Mww / di   ; ice volume density, microns3 / cm3     
       m_ice(i) = 1e9 * n_xs * Mww        ; ice mass density, ng/m3       
       h2o_ice(i) = q_xs                    ; H2O(ice), ppmv
       
     endif

;-   Find the frost point temperature, t_ice.  Use the fact that
;    a linear relationship exists between 1/T and alog10(p_h2o).
;    Do a linear interpolation between some hi and low temp.

     p_h2o = p(i) * h2o(i) *1d-6  ; h2o partial pressure, mb
     
     p1 = 0 & t1 = 0 & p2 = 0 & t2 = 0
          
     k  = where(px lt p_h2o,n)  ; find the p & t just below p_h2o
     if n gt 0 then begin     
      p1 = px(k(n-1))
      t1 = tx(k(n-1))
     endif
        
     k  = where(px ge p_h2o,n)  ; find the p & t just above p_h2o
     if n gt 0 then begin
      p2 = px(k(0))
      t2 = tx(k(0))
     endif
     
     if (p_h2o ge min(px) and p_h2o le max(px) and p1 gt 0 and p2 gt 0) then begin
              
      dsds  = (alog10(p2) - alog10(p_h2o)) / (alog10(p2) - alog10(p1))
     
      t_ice(i) = 1. / ( 1/t2 - dsds * (1/t2 - 1/t1) )
     
     endif
         
    endif  ; if T > 0

   endfor  ; loop over altitude

;- Find Zmax, Ztop, Zbot, IWC

   k = where(z gt 80 and z lt 95 and m_ice gt 0., nk)
   
   if (nk gt 0) then begin 
     
     l = where(m_ice(k) eq max(m_ice(k)) ) & l = k(l(0))
     
     zmax = z(l)       
     ztop = max(z(k))
     zbot = min(z(k))
     
     if keyword_set(constdz) then dz=abs(z[1]-z[0])
     
     for i = 0,nk-1 do begin 
       if ( z(k(i)) gt zmax-2.) then begin           
         if (not keyword_set(constdz)) then dz  = abs( z(k(i)+1) - z(k(i)-1) )*0.5  ; layer spacing (km)       
         iwc = iwc + m_ice(k(i)) * dz            ; micro-g/m2 = g/km3  
       endif
        
     endfor
       
   endif
    
;- done

;Need to return t_ice,p_ice,s_ice,h2o_sat,v_ice,m_ice,h2o_ice,Ztop,Zmax,Zbot,iwc

return,iwc
