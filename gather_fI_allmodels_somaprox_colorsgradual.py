import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

# change the default font family
plt.rcParams.update({'font.family':'Arial'})

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)

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
                break
    iout   = np.array(iout)
    rdout  = np.array(rdout)
    return iout, rdout

mylinewidth = 2
defaultwidth = 4

idur       = 1000 # ms
idelay     = 100
v_init     = -86.5 # mV
Ra         = 150
somasize   = 10 
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
spikedurat = -40

varymech = 'Na'
varyE_bool = True
varyE = 53 
varyg = 'None' 

plotstring = '_vary'
if varyE_bool==True:
    plotstring = plotstring + 'E'+str(varyE)
else:
    plotstring = plotstring + 'g'+str(varyg)

if varymech=='Na':
    folderstring = 'VaryNa/' 
    plotstring   = plotstring + '_Na'
elif varymech=='pas':
    folderstring = 'VaryPas/'
    plotstring   = plotstring + '_Pas'
elif varymech=='Kd':
    folderstring = 'VaryKd/'
    plotstring   = plotstring + '_Kd'
elif varymech=='Kv2like':
    folderstring = 'VaryKv2like/'
    plotstring   = plotstring + '_Kv2like'
elif varymech=='Kv3_1':
    folderstring = 'VaryKv3_1/'
    plotstring   = plotstring + '_Kv3_1'
elif varymech=='SK':
    folderstring = 'VarySK/'
    plotstring   = plotstring + '_SK'
elif varymech=='K_T':
    folderstring = 'VaryK_T/'
    plotstring   = plotstring + '_K_T'
elif varymech=='Im_v2':
    folderstring = 'VaryIm_v2/'
    plotstring   = plotstring + '_Im_v2'

changestring =''
if varyE_bool==True:
    changestring = changestring+'_E'+str(varyE)+'_gdf'
else:
    changestring = changestring+'_Edf_g'+str(varyg)

i_master = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]
cms = [0.1,0.5,0.75,1.0,1.25,1.5,1.99]
    
NI  = len(i_master)
Ncm = len(cms)

Nspikes_sprx          = []
I_Nspikes_sprx        = []

i_master_onecomp         = []
Nspikes_onecomp          = []
avg_AP_ampl_onecomp      = []
rms_AP_ampl_onecomp      = []
avg_AP_mins_onecomp      = []
rms_AP_mins_onecomp      = []
avg_AP_halfwidth_onecomp = []
rms_AP_halfwidth_onecomp = []
avg_ISI_onecomp          = []
rms_ISI_onecomp          = []
I_Nspikes_onecomp        = []
I_AP_ampl_onecomp        = []
I_AP_mins_onecomp        = []
I_AP_halfwidth_onecomp   = []
I_ISI_onecomp            = []


for cm in cms:
    Nspikes   = []
    I_Nspikes = []
    
    infolder = 'Ball-and-stick models/BAS_somaHH_dendpassive/Results/IStim/Soma%i/dendlen%i/denddiam'% (somasize,dendlen)+str(denddiam)+'/'
    
    ## Somaprox
    Nspikes   = []
    I_Nspikes = []
    
    infolder_sprx = infolder+'VaryNa/'
    infilename_Nspikes = infolder_sprx+'basHHdpas_csprx'+str(cm)+'_idur%i_varyiamp'% (idur) +'_E50_manual_Nspikes_vs_I.txt'
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
    
    Nspikes_sprx.append(Nspikes)
    I_Nspikes_sprx.append(I_Nspikes)
    #################### Soma only, Hodgkin-Huxley #########################################
    Nspikes   = []
    I_Nspikes = []

    # Default HH values:
    ena = 50
    ek = -77
    el_hh = -54.3
    gnabar_hh = 0.12
    gkbar_hh = 0.036
    gl_hh = 0.0003

    infolder_shh = 'Somaonly/Results/IStim/Soma%i/' % somasize
    hhstring = '_ena'+str(ena)+'_ek'+str(ek)+'_el'+str(el_hh)+'_gnabar'+str(gnabar_hh)+'_gkbar'+str(gkbar_hh)+'_gl'+str(gl_hh)
    infilename_Nspikes = infolder_shh+'somaonlyHH_idur%i_varyiamp'% (idur)+'_manual_cm'+str(cm)+hhstring+'_Nspikes_vs_I.txt'
    # Read files
    infile_Nspikes = open(infilename_Nspikes,'r')
    lines_Nspikes  = infile_Nspikes.readlines()
    Nlines_Nspikes = len(lines_Nspikes)

    for i in range(Nlines_Nspikes):
        words_Nspikes = lines_Nspikes[i].split()
        if len(words_Nspikes)>0:
            I_Nspikes.append(float(words_Nspikes[0]))
            Nspikes.append(float(words_Nspikes[1]))

    infile_Nspikes.close()
    
    Nspikes_onecomp.append(Nspikes)
    I_Nspikes_onecomp.append(I_Nspikes)


# Plotting
colors = []
deltaN = 1.0/(Ncm+1)
startt = 1.0-deltaN
print('1.0/(Ncm+1):',deltaN)
print('Ncm/(Ncm+1):',Ncm/(Ncm+1.))
for i in range(Ncm):
    colors.append((1.0-i/float(Ncm),0,i/float(Ncm),1.0-abs(0.5-i/float(Ncm))))

plotfolder = 'Comparemodels/All/'
plotname_all = plotfolder+'fI_allmodels_somaprox_colorsgradual.png'

fig = plt.figure(figsize=(15,15),dpi=300)
gs = gridspec.GridSpec(3, 4)
ax1 = plt.subplot(gs[0, 0:2])
ax2 = plt.subplot(gs[0, 2:4])
ax3 = plt.subplot(gs[1, 0:2])
ax4 = plt.subplot(gs[1, 2:4])
ax5 = plt.subplot(gs[2, 0:2])
ax6 = plt.subplot(gs[2, 2:4])

ax1.set_title(r'A',loc='left',fontsize=18)
ax2.set_title(r'B',loc='left',fontsize=18)
ax3.set_title(r'C',loc='left',fontsize=18)
ax4.set_title(r'D',loc='left',fontsize=18)
ax5.set_title(r'E',loc='left',fontsize=18)
ax6.set_title(r'F',loc='left',fontsize=18)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)
plt.rc('legend', fontsize=16)

ax1.set_title('One compartment HH neuron',fontsize=18)
for i in range(Ncm):
    if cms[i]==1.0:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    ax1.plot(I_Nspikes_onecomp[i], Nspikes_onecomp[i],color=colors[i],label=r'%.2f$c_\mathregular{m}$' % cms[i], linewidth=thelinewidth)
ax1.set_ylabel('$f$ (Hz)',fontsize=16)

ax2.set_title('Ball-and-stick HH neuron',fontsize=18)
for i in range(Ncm):
    if cms[i]==1.0:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    if np.sum(Nspikes_sprx[i])!=0:
        ax2.plot(I_Nspikes_sprx[i], Nspikes_sprx[i],color=colors[i],label=r'%.2f$c_\mathregular{m}$' % cms[i], linewidth=thelinewidth)

# Allen:

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

varymech = 'Na' # 'Kd' # 'NaV' # 'SK' # 'Im_v2' # 'Kv2like' # 'pas' #
varyE_bool = True
varyE = 53
varyg = 'None'

plotstring = '_vary'
if varyE_bool==True:
    plotstring = plotstring + 'E'+str(varyE)
else:
    plotstring = plotstring + 'g'+str(varyg)

if varymech=='Na':
    folderstring = 'VaryNa/' 
    plotstring   = plotstring + '_Na'
elif varymech=='pas':
    folderstring = 'VaryPas/'
    plotstring   = plotstring + '_Pas'
elif varymech=='Kd':
    folderstring = 'VaryKd/'
    plotstring   = plotstring + '_Kd'
elif varymech=='Kv2like':
    folderstring = 'VaryKv2like/'
    plotstring   = plotstring + '_Kv2like'
elif varymech=='Kv3_1':
    folderstring = 'VaryKv3_1/'
    plotstring   = plotstring + '_Kv3_1'
elif varymech=='SK':
    folderstring = 'VarySK/'
    plotstring   = plotstring + '_SK'
elif varymech=='K_T':
    folderstring = 'VaryK_T/'
    plotstring   = plotstring + '_K_T'
elif varymech=='Im_v2':
    folderstring = 'VaryIm_v2/'
    plotstring   = plotstring + '_Im_v2'

changestring =''
if varyE_bool==True:
    changestring = changestring+'_E'+str(varyE)+'_gdf'
else:
    changestring = changestring+'_Edf_g'+str(varyg)

i_master = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]
    
NI  = len(i_master)

Nspikes_sprx_all      = []
I_Nspikes_sprx_all    = []

for testmodel in testmodels:
    Nspikes_sprx_allen          = []
    I_Nspikes_sprx_allen        = []
    infolder      = 'Allen_test_changecapacitance/figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        ############# SOMAPROX ##################################
        Nspikes   = []
        I_Nspikes = []
        
        # Set names
        infilename_Nspikes = infolder+'%i_cmsprx'%testmodel+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
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
        
        Nspikes_sprx_allen.append(Nspikes)
        I_Nspikes_sprx_allen.append(I_Nspikes)
    Nspikes_sprx_all.append(Nspikes_sprx_allen)
    I_Nspikes_sprx_all.append(I_Nspikes_sprx_allen)
        

# Plotting

## avg and rms:

ax3.set_title('Allen model 1',fontsize=18)
ax4.set_title('Allen model 2',fontsize=18)
ax5.set_title('Allen model 3',fontsize=18)
I_Nspikes_sprx_this0 = I_Nspikes_sprx_all[0]
I_Nspikes_sprx_this1 = I_Nspikes_sprx_all[1]
I_Nspikes_sprx_this2 = I_Nspikes_sprx_all[2]
Nspikes_sprx_this0  = Nspikes_sprx_all[0]
Nspikes_sprx_this1  = Nspikes_sprx_all[1]
Nspikes_sprx_this2  = Nspikes_sprx_all[2]
for i in range(Ncm):
    if cms[i]==1.0:
        thelinewidth=defaultwidth
    else:
        thelinewidth=mylinewidth
    print('i:',i, 'Ncm:',Ncm)
    if np.sum(Nspikes_sprx_this0[i])!=0:
        ax3.plot(I_Nspikes_sprx_this0[i], Nspikes_sprx_this0[i],color=colors[i],
label=r'%.2f$c_\mathregular{m}$' % cms[i], linewidth=thelinewidth)
    if np.sum(Nspikes_sprx_this1[i])!=0:
        ax4.plot(I_Nspikes_sprx_this1[i], Nspikes_sprx_this1[i],color=colors[i],
label=r'%.2f$c_\mathregular{m}$' % cms[i], linewidth=thelinewidth)
    if np.sum(Nspikes_sprx_this2[i])!=0:
        ax5.plot(I_Nspikes_sprx_this2[i], Nspikes_sprx_this2[i],color=colors[i],
label=r'%.2f$c_\mathregular{m}$' % cms[i], linewidth=thelinewidth)


lastdiff = []
print('Nspikes_onecomp[5]:',Nspikes_onecomp[5])
print('Nspikes_onecomp[3]:',Nspikes_onecomp[3])
print('I_Nspikes_onecomp[5]:',I_Nspikes_onecomp[5])
print('I_Nspikes_onecomp[3]:',I_Nspikes_onecomp[3])
im, rd1 = reldiffs(Nspikes_onecomp[5],Nspikes_onecomp[3],I_Nspikes_onecomp[5],I_Nspikes_onecomp[3]) 
if len(rd1)>0:
    lastdiff.append(rd1[-1])
im, rd1 = reldiffs(Nspikes_sprx[5],Nspikes_sprx[3],I_Nspikes_sprx[5],I_Nspikes_sprx[3]) 
if len(rd1)>0:
    lastdiff.append(rd1[-1])
im, rd1 = reldiffs(Nspikes_sprx_this0[5],Nspikes_sprx_this0[3],I_Nspikes_sprx_this0[5],I_Nspikes_sprx_this0[3]) 
if len(rd1)>0:
    lastdiff.append(rd1[-1])
im, rd1 = reldiffs(Nspikes_sprx_this1[5],Nspikes_sprx_this1[3],I_Nspikes_sprx_this1[5],I_Nspikes_sprx_this1[3]) 
if len(rd1)>0:
    lastdiff.append(rd1[-1])
im, rd1 = reldiffs(Nspikes_sprx_this2[5],Nspikes_sprx_this2[3],I_Nspikes_sprx_this2[5],I_Nspikes_sprx_this2[3]) 
if len(rd1)>0:
    lastdiff.append(rd1[-1])

barWidth = 0.5
br1  = np.arange(len(lastdiff))

ax6.bar(br1, lastdiff,width=barWidth,label=r'$1.5c_m$',color=colors[5])
plt.xticks(br1,['OC','BAS','A1','A2','A3'])
ax6.set_xlabel('Combination',fontsize=14)
ax6.set_ylabel(r'Relative difference at max. common current',fontsize=14)
ax6.set_title(r'Difference from default',fontsize=18)

ax1.legend(loc='lower right')
ax2.legend(loc='lower right')
ax3.legend(loc='lower right')
ax4.legend(loc='lower right',ncol=2)
ax5.legend(loc='lower right')
ax6.legend(loc='upper right')
ax1.set_xlabel(r'$I$ (nA)',fontsize=16)
ax1.set_ylabel(r'$f$ (Hz)',fontsize=16)
ax2.set_xlabel(r'$I$ (nA)',fontsize=16)
ax2.set_ylabel(r'$f$ (Hz)',fontsize=16)
ax3.set_xlabel(r'$I$ (nA)',fontsize=16)
ax3.set_ylabel(r'$f$ (Hz)',fontsize=16)
ax4.set_xlabel(r'$I$ (nA)',fontsize=16)
ax4.set_ylabel(r'$f$ (Hz)',fontsize=16)
ax5.set_xlabel(r'$I$ (nA)',fontsize=16)
ax5.set_ylabel(r'$f$ (Hz)',fontsize=16)

fig.tight_layout()
plt.savefig(plotname_all)


plt.show()
