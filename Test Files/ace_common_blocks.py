
# the following are the collection of common blocks used in the atmospheric chemistry and energetic (ace)
# software

def initialize():
	global nbins
	nbins = None 

	global nmaj
	nmaj = None 

	global nei
	nei = None 

	global nst
	nst = None 

	global jmax
	jmax = None 

	global lmax
	lmax = None 

	global sigs
	sigs = None 

	global pe
	pe = None 

	global pi
	pi = None 

	global siga
	siga = None 

	global sec
	sec = None 

	global sigex
	sigex = None 

	global sigix
	sigix = None 

	global tpot
	tpot = None 

	global prob
	prob = None 

	global ener
	ener = None 

	global del
	del = None 

	global peflux
	peflux = None 

	global primary
	primary = None 

	global sigloss
	sigloss = None 

	global iimax
	iimax = None 

	global upflux
	upflux = None 

	global downflux
	downflux = None 

	global toaflux
	toaflux = None 

	global wv1
	wv1 = None 

	global wv2
	wv2 = None 

	global ssflux
	ssflux = None 

	global sigabs
	sigabs = None 

	global sigionx
	sigionx = None 

	global auger_energy
	auger_energy = None 

	global auger_wvln
	auger_wvln = None 

	global zmaj
	zmaj = None 

	global zz
	zz = None 

	global z
	z = None 

	global zt
	zt = None 

	global lat
	lat = None 

	global sza
	sza = None 

	global idate
	idate = None 

	global utsec
	utsec = None 

	global f107
	f107 = None 

	global f107a
	f107a = None 

	global ap
	ap = None 

	global first_neutral
	first_neutral = None 

	global first_ssflux
	first_ssflux = None 

	global first_pxsect
	first_pxsect = None 

	global first_exsect
	first_exsect = None 

	global zcol
	zcol = None 

	global tau
	tau = None 

	global flux
	flux = None 

	global photoki
	photoki = None 

	global photoi
	photoi = None 

	global aprod
	aprod = None 

	global aloss
	aloss = None 

	global ww
	ww = None 

	global a0
	a0 = None 

	global omeg
	omeg = None 

	global anu
	anu = None 

	global bb
	bb = None 

	global auto
	auto = None 

	global thi
	thi = None 

	global ak
	ak = None 

	global aj
	aj = None 

	global gams
	gams = None 

	global gamb
	gamb = None 

	global ts
	ts = None 

	global tb
	tb = None 

	global ta
	ta = None 

	global eistates
	eistates = None 

	global eden
	eden = None 

	global etemp
	etemp = None 

	global eiionz
	eiionz = None 

	global eiionzk
	eiionzk = None 

	global eiexcit
	eiexcit = None 

	global vem5577
	vem5577 = None 

	global vem6300
	vem6300 = None 

	global vem2972
	vem2972 = None 

	global n2a
	n2a = None 

	global o1d
	o1d = None 

	global o1s
	o1s = None 

        
       
#C Definitions:
#C SIGS   elastic cross sections for each species, energy# cm2
#C PE     elastic backscatter probabilities for each species, energy
#C PI     inelastic  "
#C SIGA   energy loss cross section for each species, loss, energy# cm2
#C SEC    secondary production xsect for species, Esec, Epri# cm2
#C SIGEX  excitation xsect for each state, species, energy# cm2
#C SIGIX  ionization xsect for each state, species, energy# cm2
#C IIMAX  number of bins for secondary production for each primary energy
#C WW     energy threshold for each excited state, species# eV
#C WW, AO, OMEG, ANU, BB: revised excitation cross section parameters,
#C        from Green & Stolarski (1972) formula (W, A, omega, nu, gamma)
#C AUTO   autoionization coefs (= 0 as autoion. included in ion xsects)
#C THI    energy threshold for each ionized state, species# eV
#C AK, AJ, TS, TA, TB, GAMS, GAMB:  Jackman et al (1977) ioniz. params
#C ENER   energy grid# eV
#C DEL    energy grid spacing# eV
#C NNN    number of excited states for each species
#C NINN   number of ionized states for each species
#C NUM    number of points on elastic data trid for each species
#C EC     data energy grid of elastic xsects and backscatter ratios
#C        for each species# eV
#C CC     elastic xsects on data grid for each species, cm2
#C CE     elastic backscat. probs on data grid for each species# cm2
#C CI     inelastic "
#C
#C Array dimensions:
#C NBINS  number of energy levels
#C NMAJ   number of major species
#C NEI    number of slots for excited and ionized states

    
# NMAJ   number of major species
# NEI    number of slots for excited and ionized states
#ww=dblarr(nei,nmaj)