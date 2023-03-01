import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

# change the default font family
plt.rcParams.update({'font.family':'Arial'})

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
plt.rc('legend', fontsize=14)

def reldiffs(fother,f1,iother,i1):
    iout   = []
    iout2  = []
    rdout  = []
    rdout2 = []
    N1     = len(f1)
    Nother = len(fother)
    for i in range(Nother):
        ithis = iother[i]
        for j in range(N1):
            ibasic = i1[j]
            if ithis==ibasic:
                falt   = fother[i]
                fbasic = f1[j]
                if fbasic!=0 and falt!=0:
                    iout.append(ithis)
                    rdout.append((fbasic-falt)/float(fbasic))
                    rdout2.append((fbasic-falt)/float(falt))
                break
    iout   = np.array(iout)
    rdout  = np.array(rdout)
    return iout, rdout, rdout2

mylinewidth = 2
defaultwidth = 3

testmodels = [478513437,488462965,478513407]
idur       = 2000 # ms
idelay     = 100
v_init     = -86.5 # mV
Ra         = 150
somasize   = 10  
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
Nmodels    = len(testmodels)
spikedurat = -40

namestringfirst = ''
varyENa = [33,43,53,63,73]
namestringfirstNa = namestringfirst + 'ENa'
plotlabelNa = r'$E_{\mathregular{Na}}$'
varyEK = [-127,-117,-107,-97,-87]
namestringfirstK = namestringfirst + 'EK'
plotlabelK = r'$E_{\mathregular{K}}$'
varyEpas = [-20,-10,0,10,20]   
namestringfirstpas = namestringfirst + 'Epasplus'
plotlabelEpas = []
for i in range(len(varyEpas)):
    Eval = varyEpas[i]
    if Eval>=0:
        Estring = '$E_{\mathregular{L}}$ + %i' % Eval
    else:
        Estring = '$E_{\mathregular{L}}$ - %i' % abs(Eval)
    plotlabelEpas.append(Estring)
varycao = [0.02,0.2,2.0,20.0,200.0]
namestringfirstCa = namestringfirst + 'ECa'
namestringfirstcao = namestringfirst + '_cao'
plotlabelCa = r'$E_{\mathregular{Ca}}$'


plotstringNa  = '_vary_Na'
plotstringK   = '_vary_K'
plotstringCa  = '_vary_Ca'
plotstringpas = '_vary_pas'

i_master = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]
cm = 1.0
    
NI  = len(i_master)
NENa = len(varyENa)

i_master_everywhere_all_Na   = []
Nspikes_everywhere_all_Na    = []
I_Nspikes_everywhere_all_Na  = []

for testmodel in testmodels:
    i_master_everywhere_Na   = []
    Nspikes_everywhere_Na    = []
    I_Nspikes_everywhere_Na  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for E in varyENa:
        Nspikes   = []
        I_Nspikes = []
        
        namestringNa = namestringfirstNa+str(E)
        
        # Set names
        try:
            infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringNa,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
            # Read files
            infile_Nspikes = open(infilename_Nspikes,'r')
        except:
            infilename_Nspikes = infolder+'%i_%s_cmfall'%(testmodel,namestringNa)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
            # Read files
            infile_Nspikes = open(infilename_Nspikes,'r')
    
        lines_Nspikes = infile_Nspikes.readlines()
        Nlines_Nspikes = len(lines_Nspikes)
    
        for i in range(Nlines_Nspikes):
            words_Nspikes = lines_Nspikes[i].split()
            if len(words_Nspikes)>0:
                I_Nspikes.append(float(words_Nspikes[0]))
                Nspikes.append(float(words_Nspikes[1]))
    
        infile_Nspikes.close()
        
        Nspikes_everywhere_Na.append(Nspikes)
        I_Nspikes_everywhere_Na.append(I_Nspikes)
    
    Nspikes_everywhere_all_Na.append(Nspikes_everywhere_Na)
    I_Nspikes_everywhere_all_Na.append(I_Nspikes_everywhere_Na)
    

# Plotting

colors = []
for i in range(NENa):
    colors.append((1.0-i/float(NENa),0,i/float(NENa),1.0-abs(0.5-i/float(NENa))))

plotfolder = 'figures/Comparemodels/'
plotname = plotfolder+'fI_varyEs_Allen_shifts_standing_colorsgradual.png'

## avg and rms:

fig = plt.figure(figsize=(18,18),dpi=300)

gs = gridspec.GridSpec(4, 6)

###
# Na
ax1 = plt.subplot(gs[0, 0:2])
ax2 = plt.subplot(gs[0, 2:4])
ax3 = plt.subplot(gs[0, 4:6])
# K
ax4 = plt.subplot(gs[1, 0:2])
ax5 = plt.subplot(gs[1, 2:4])
ax6 = plt.subplot(gs[1, 4:6])
# L
ax7 = plt.subplot(gs[2, 0:2])
ax8 = plt.subplot(gs[2, 2:4])
ax9 = plt.subplot(gs[2, 4:6])
# Ca
ax10 = plt.subplot(gs[3, 0:2])
ax11 = plt.subplot(gs[3, 2:4])
ax12 = plt.subplot(gs[3, 4:6])

ax1.set_title(r'A',loc='left',fontsize=17)
ax2.set_title(r'B',loc='left',fontsize=17)
ax3.set_title(r'C',loc='left',fontsize=17)
ax4.set_title(r'D',loc='left',fontsize=17)
ax5.set_title(r'E',loc='left',fontsize=17)
ax6.set_title(r'F',loc='left',fontsize=17)
ax7.set_title(r'G',loc='left',fontsize=17)
ax8.set_title(r'H',loc='left',fontsize=17)
ax9.set_title(r'I',loc='left',fontsize=17)
ax10.set_title(r'J',loc='left',fontsize=17)
ax11.set_title(r'K',loc='left',fontsize=17)
ax12.set_title(r'L',loc='left',fontsize=17)

ax1.set_title(r'Varying $E_{\mathregular{Na}}$, Allen model 1',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_Na[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_Na[0]
for j in range(NENa):
    if varyENa[j]==53:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax1.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%i mV' % (plotlabelNa,varyENa[j]), linewidth=thelinewidth)
ax1.set_xlabel('$I$ (nA)',fontsize=14)
ax1.set_ylabel('$f$ (Hz)',fontsize=14)
ax1.legend(loc='lower right',ncol=1)

ax2.set_title(r'Varying $E_{\mathregular{Na}}$, Allen model 2',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_Na[1]
Nspikes_everywhere_this   = Nspikes_everywhere_all_Na[1]
for j in range(NENa):
    if varyENa[j]==53:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax2.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%i mV' % (plotlabelNa,varyENa[j]), linewidth=thelinewidth)
ax2.set_xlabel('$I$ (nA)',fontsize=14)
ax2.set_ylabel('$f$ (Hz)',fontsize=14)
ax2.legend(loc='lower right',ncol=1)

ax3.set_title(r'Varying $E_{\mathregular{Na}}$, Allen model 3',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_Na[2]
Nspikes_everywhere_this   = Nspikes_everywhere_all_Na[2]
for j in range(NENa):
    if varyENa[j]==53:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax3.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%i mV' % (plotlabelNa,varyENa[j]), linewidth=thelinewidth)
ax3.set_xlabel('$I$ (nA)',fontsize=14)
ax3.set_ylabel('$f$ (Hz)',fontsize=14)
ax3.legend(loc='lower right',ncol=1)

### Do the same for K: #################################################################

NEK = len(varyEK)

i_master_everywhere_all_K   = []
Nspikes_everywhere_all_K    = []
I_Nspikes_everywhere_all_K  = []

for testmodel in testmodels:
    i_master_everywhere_K   = []
    Nspikes_everywhere_K    = []
    I_Nspikes_everywhere_K  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for E in varyEK:
        Nspikes   = []
        I_Nspikes = []
        
        namestringK = namestringfirstK+str(E)
        
        # Set names
        try:
            infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringK,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
            # Read files
            infile_Nspikes = open(infilename_Nspikes,'r')
        except:
            infilename_Nspikes = infolder+'%i_%s_cmfall'%(testmodel,namestringK)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
            # Read files
            infile_Nspikes = open(infilename_Nspikes,'r')
    
        lines_Nspikes = infile_Nspikes.readlines()
        Nlines_Nspikes = len(lines_Nspikes)
    
        for i in range(Nlines_Nspikes):
            words_Nspikes = lines_Nspikes[i].split()
            if len(words_Nspikes)>0:
                I_Nspikes.append(float(words_Nspikes[0]))
                Nspikes.append(float(words_Nspikes[1]))
    
        infile_Nspikes.close()
        
        Nspikes_everywhere_K.append(Nspikes)
        I_Nspikes_everywhere_K.append(I_Nspikes)
        
    Nspikes_everywhere_all_K.append(Nspikes_everywhere_K)
    I_Nspikes_everywhere_all_K.append(I_Nspikes_everywhere_K)


ax4.set_title(r'Varying $E_{\mathregular{K}}$, Allen model 1',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_K[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_K[0]
for j in range(NEK):
    if varyEK[j]==-107:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax4.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%i mV' % (plotlabelK,varyEK[j]), linewidth=thelinewidth)
ax4.set_xlabel('$I$ (nA)',fontsize=14)
ax4.set_ylabel('$f$ (Hz)',fontsize=14)
ax4.legend(loc='lower right',ncol=1)

ax5.set_title(r'Varying $E_{\mathregular{K}}$, Allen model 2',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_K[1]
Nspikes_everywhere_this   = Nspikes_everywhere_all_K[1]
for j in range(NEK):
    if varyEK[j]==-107:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax5.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%i mV' % (plotlabelK,varyEK[j]), linewidth=thelinewidth)
ax5.set_xlabel('$I$ (nA)',fontsize=14)
ax5.set_ylabel('$f$ (Hz)',fontsize=14)
ax5.legend(loc='lower right',ncol=1)

ax6.set_title(r'Varying $E_{\mathregular{K}}$, Allen model 3',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_K[2]
Nspikes_everywhere_this   = Nspikes_everywhere_all_K[2]
for j in range(NEK):
    if varyEK[j]==-107:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax6.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%i mV' % (plotlabelK,varyEK[j]), linewidth=thelinewidth)
ax6.set_xlabel('$I$ (nA)',fontsize=14)
ax6.set_ylabel('$f$ (Hz)',fontsize=14)
ax6.legend(loc='lower right',ncol=1)

################ Do the same for Epas: #####################################
NEpas = len(varyEpas)

i_master_everywhere_all_pas   = []
Nspikes_everywhere_all_pas    = []
I_Nspikes_everywhere_all_pas  = []

for testmodel in testmodels:
    i_master_everywhere_pas   = []
    Nspikes_everywhere_pas    = []
    I_Nspikes_everywhere_pas  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for E in varyEpas:
        Nspikes   = []
        I_Nspikes = []
        
        namestringpas = namestringfirstpas+str(E)
        
        # Set names
        try:
            infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringpas,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
            # Read files
            infile_Nspikes = open(infilename_Nspikes,'r')
        except:
            infilename_Nspikes = infolder+'%i_%s_cmfall'%(testmodel,namestringpas)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
            # Read files
            infile_Nspikes = open(infilename_Nspikes,'r')
    
        lines_Nspikes = infile_Nspikes.readlines()
        Nlines_Nspikes = len(lines_Nspikes)
    
        for i in range(Nlines_Nspikes):
            words_Nspikes = lines_Nspikes[i].split()
            if len(words_Nspikes)>0:
                I_Nspikes.append(float(words_Nspikes[0]))
                Nspikes.append(float(words_Nspikes[1]))
    
        infile_Nspikes.close()
        
        Nspikes_everywhere_pas.append(Nspikes)
        I_Nspikes_everywhere_pas.append(I_Nspikes)
    Nspikes_everywhere_all_pas.append(Nspikes_everywhere_pas)
    I_Nspikes_everywhere_all_pas.append(I_Nspikes_everywhere_pas)

# Plotting

ax7.set_title(r'Varying $E_{\mathregular{L}}$, Allen model 1',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_pas[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_pas[0]
for j in range(NEpas):
    if varyEpas[j]==0:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax7.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s mV' % plotlabelEpas[j], linewidth=thelinewidth)
ax7.set_xlabel('$I$ (nA)',fontsize=14)
ax7.set_ylabel('$f$ (Hz)',fontsize=14)
ax7.legend(loc='lower right',ncol=1)

ax8.set_title(r'Varying $E_{\mathregular{L}}$, Allen model 2',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_pas[1]
Nspikes_everywhere_this   = Nspikes_everywhere_all_pas[1]
for j in range(NEpas):
    if varyEpas[j]==0:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax8.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s mV' % plotlabelEpas[j], linewidth=thelinewidth)
ax8.set_xlabel('$I$ (nA)',fontsize=14)
ax8.set_ylabel('$f$ (Hz)',fontsize=14)
ax8.legend(loc='upper left',ncol=1)

ax9.set_title(r'Varying $E_{\mathregular{L}}$, Allen model 3',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_pas[2]
Nspikes_everywhere_this   = Nspikes_everywhere_all_pas[2]
for j in range(NEpas):
    if varyEpas[j]==0:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax9.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s mV' % plotlabelEpas[j], linewidth=thelinewidth)
ax9.set_xlabel('$I$ (nA)',fontsize=14)
ax9.set_ylabel('$f$ (Hz)',fontsize=14)
ax9.legend(loc='upper left',ncol=1)

############################ Ca ############################
R = 8.314   # JK-1mol-1
F = 9.648e4 # Cmol-1
T = 307.15  # K
prefactor = 1000*R*T/(2.0*F)
cai0 = 1e-4 # mM
NECa = len(varycao)
ECa0 = np.zeros(NECa)

for i in range(NECa):
    ECa0[i] = prefactor*np.log(varycao[i]/cai0)

i_master_everywhere_all_Ca   = []
Nspikes_everywhere_all_Ca    = []
I_Nspikes_everywhere_all_Ca  = []

for testmodel in testmodels:
    i_master_everywhere_Ca   = []
    Nspikes_everywhere_Ca    = []
    I_Nspikes_everywhere_Ca  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cao in varycao:
        Nspikes   = []
        I_Nspikes = []
        
        namestringcao = namestringfirstcao+str(cao)
        
        # Set names
        infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringcao,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
        # Read files
        infile_Nspikes = open(infilename_Nspikes,'r')
    
        lines_Nspikes = infile_Nspikes.readlines()
        Nlines_Nspikes = len(lines_Nspikes)
    
        for i in range(Nlines_Nspikes):
            words_Nspikes = lines_Nspikes[i].split()
            if len(words_Nspikes)>0:
                I_Nspikes.append(float(words_Nspikes[0]))
                Nspikes.append(float(words_Nspikes[1]))
    
        infile_Nspikes.close()
        
        Nspikes_everywhere_Ca.append(Nspikes)
        I_Nspikes_everywhere_Ca.append(I_Nspikes)
    Nspikes_everywhere_all_Ca.append(Nspikes_everywhere_Ca)
    I_Nspikes_everywhere_all_Ca.append(I_Nspikes_everywhere_Ca)

# Plotting

ax10.set_title(r'Varying $E_{\mathregular{Ca}}(t=0)$, Allen model 1',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_Ca[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_Ca[0]
for j in range(NECa):
    if varycao[j]==2:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax10.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%.1f mV' % (plotlabelCa,ECa0[j]), linewidth=thelinewidth)
ax10.set_xlabel('$I$ (nA)',fontsize=14)
ax10.set_ylabel('$f$ (Hz)',fontsize=14)
ax10.legend(loc='lower right',ncol=1)

ax11.set_title(r'Varying $E_{\mathregular{Ca}}(t=0)$, Allen model 2',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_Ca[1]
Nspikes_everywhere_this   = Nspikes_everywhere_all_Ca[1]
for j in range(NECa):
    if varycao[j]==2:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax11.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%.1f mV' % (plotlabelCa,ECa0[j]), linewidth=thelinewidth)
ax11.set_xlabel('$I$ (nA)',fontsize=14)
ax11.set_ylabel('$f$ (Hz)',fontsize=14)
ax11.legend(loc='lower right',ncol=1)

ax12.set_title(r'Varying $E_{\mathregular{Ca}}(t=0)$, Allen model 3',fontsize=15)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_Ca[2]
Nspikes_everywhere_this   = Nspikes_everywhere_all_Ca[2]
for j in range(NECa):
    if varycao[j]==2:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ### Everywhere:
    ax12.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%s=%.1f mV' % (plotlabelCa,ECa0[j]), linewidth=thelinewidth)
ax12.set_xlabel('$I$ (nA)',fontsize=14)
ax12.set_ylabel('$f$ (Hz)',fontsize=14)
ax12.legend(loc='lower right',ncol=1)

# Plotting
ax1.set_xlabel('$I$ (nA)',fontsize=16)
ax1.set_ylabel('$f$ (Hz)',fontsize=16)
ax2.set_xlabel('$I$ (nA)',fontsize=16)
ax2.set_ylabel('$f$ (Hz)',fontsize=16)
ax3.set_xlabel('$I$ (nA)',fontsize=16)
ax3.set_ylabel('$f$ (Hz)',fontsize=16)
ax4.set_xlabel('$I$ (nA)',fontsize=16)
ax4.set_ylabel('$f$ (Hz)',fontsize=16)
ax5.set_xlabel('$I$ (nA)',fontsize=16)
ax5.set_ylabel('$f$ (Hz)',fontsize=16)
ax6.set_xlabel('$I$ (nA)',fontsize=16)
ax6.set_ylabel('$f$ (Hz)',fontsize=16)

fig.tight_layout()

plt.savefig(plotname)

plt.show()
