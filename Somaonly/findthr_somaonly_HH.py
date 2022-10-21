import matplotlib.pyplot as plt
import numpy as np

cms        = [0.5,0.67,0.75,0.9,1.0,1.1,1.25,1.4,1.5,1.75,2.0,2.5,3.0]
iamps      = [0,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.02,0.021, 0.022,0.023,0.024,0.025]
idur       = 1000
idelay     = 10
tstop      = idur+idelay+10. 
dtexp      = -7
somasize   = 10
Ra         = 100.
v_init     = -70 
Ncm        = len(cms)
Ni         = len(iamps)
thresholds = np.zeros(Ncm)

# Default HH values:
ena = 50
ek = -77
el_hh = -54.3
gnabar_hh = 0.12
gkbar_hh = 0.036
gl_hh = 0.0003

hhstring = '_ena'+str(ena)+'_ek'+str(ek)+'_el'+str(el_hh)+'_gnabar'+str(gnabar_hh)+'_gkbar'+str(gkbar_hh)+'_gl'+str(gl_hh)


plotfolder  = 'Results/IStim/Soma%i/' % somasize
plotname    = plotfolder + 'thresholds_somaonlyHH_varycmfactor_%icms_idur%i' % (Ncm,idur)+hhstring+'.png'
outfilename = plotfolder + 'thresholds_somaonlyHH_varycmfactor_%icms_idur%i' % (Ncm,idur)+hhstring+'.txt'

outfile = open(outfilename,'w')

for i in range(Ncm):
    cm = cms[i]
    spiked = False
    for j in range(Ni):
        iamp = iamps[j]
        folder = 'Results/IStim/Soma%i/current_idur%i'%(somasize,idur)+'_iamp'+str(iamp)+'/'
        filename = folder+'somaonly_cm'+str(cm)+'_idur%i_iamp'%idur+str(iamp)+hhstring+'_Ra%i_vinit' %Ra+str(v_init)+'_V.txt' 

        t = []
        V = []
        
        infile = open(filename,'r')
        lines = infile.readlines()
        for line in lines:
            words = line.split()
            if len(words)>0:
                t.append(float(words[0]))
                V.append(float(words[1]))
        infile.close()
        
        vmax = max(V)
        vmin = min(V) 
        deltav = vmax-vmin
        vthr  = -20 # If there is a peak above this value, we count it
        vprev = vthr-40 # A peak never kicks in at initiation, even if I change vthr
        Npeaks = 0
        peaktimes = []
        for m in range (1,len(V)-1):
            if V[m-1]<V[m] and V[m+1]<V[m] and V[m]>vthr:
                peaktimes.append(t[m])
                Npeaks+=1
        if vmax<-20:
            Npeaks = 0
        if len(peaktimes)>0 and peaktimes[-1]<(idelay+0.75*idur):
            Npeaks = 0
        if Npeaks>0:
            thresholds[i]=iamp
            outfile.write('%.2f %.5f\n' % (cm,iamp))
            break 
outfile.close()

plt.figure(figsize=(6,5))
plt.plot(cms,thresholds,'-o')
plt.xlabel('$C_m$ ($\mu$F/cm$^2$)')
plt.ylabel('Spiking threshold (nA)')
plt.title(r'Spiking threshold vs $C_m$, HH one comp')
plt.savefig(plotname)
plt.show()
