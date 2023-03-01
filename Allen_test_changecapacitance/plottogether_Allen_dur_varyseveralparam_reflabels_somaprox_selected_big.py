import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

def reldiffs(fother,f1,iother,i1):
    iout   = []
    rdout  = []
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

# change the default font family
plt.rcParams.update({'font.family':'Arial'})

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
plt.rc('legend', fontsize=16)

mylinewidth = 2
defaultwidth = 3

fig = plt.figure(figsize=(20,12),dpi=300)

gs = gridspec.GridSpec(2, 6)

ax1 = plt.subplot(gs[0, 0:2])
ax2 = plt.subplot(gs[0, 2:4])
ax3 = plt.subplot(gs[0, 4:6])
ax4 = plt.subplot(gs[1, 0:2])
ax5 = plt.subplot(gs[1, 2:4])
ax6 = plt.subplot(gs[1, 4:6])

fig.suptitle(r'Spike duration at -40 mV vs $I$, Allen model 1',fontsize=20)

ax1.set_title(r'A',loc='left',fontsize=18)
ax2.set_title(r'B',loc='left',fontsize=18)
ax3.set_title(r'C',loc='left',fontsize=18)
ax4.set_title(r'D',loc='left',fontsize=18)
ax5.set_title(r'E',loc='left',fontsize=18)
ax6.set_title(r'F',loc='left',fontsize=18)

plotname = 'figures/Comparemodels/varyseveraltogether_durs_reflabels_somaprox_selected_big.png'
colors = ['k','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:grey','tab:olive','tab:cyan']

testmodel  = 478513437
idur       = 2000 # ms
idelay     = 100
v_init     = -86.5 # mV
Ra         = 150
somasize   = 10
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
spikedurat = -40

varymech = 'None' # 'Na' # 'K' # 'pas'
namestring = ''
if varymech=='Na':
    varyE = 50 #[40,50,53,60,70] 
    namestring = namestring + 'ENa'+str(varyE)
elif varymech=='K':
    varyE = -107 
    namestring = namestring + 'EK'+str(varyE)
elif varymech=='pas': 
    varyE = -77 
    namestring = namestring + 'EK'+str(varyE)
elif varymech=='None':
    varyE = 'None'
varygbool = True # False # 
varyIh       = False
vary_NaV     = True # False # 
vary_Kd      = False
vary_Kv2like = False  
vary_Kv3_1   = False
vary_K_T     = False
vary_Im_v2   = False
vary_SK      = False
vary_Ca_HVA  = True # False # 
vary_Ca_LVA  = False
vary_gpas    = False 

cms        = [1.0,1.5,1.5]
varygs     = [1.0,1.5,3.0]
varycao    = [2.0,20.0,20.0]
varyENas   = [53,63,63]
varyEKs    = [-107,-107,-107]
varyEpases = [0,0,0]
combos     = ['Default','Combination 1', 'Combination 2']

R = 8.314   # JK-1mol-1
F = 9.648e4 # Cmol-1
T = 307.15  # K
prefactor = 1000*R*T/(2.0*F)
cai0 = 1e-4 # mM

NECa = len(varycao)
ECa0 = np.zeros(NECa)

for i in range(NECa):
    ECa0[i] = prefactor*np.log(varycao[i]/cai0)

idelay = 100  # ms 
afteri = 100  # ms  

tstop_i = idur+afteri+idelay

i_master = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]

NI  = len(i_master)
Ng = len(varygs)

i_master_everywhere = []

infolder      = 'figures/%i/' % (testmodel)
vrestfolder   = infolder 

I_default = []
f_default = []
I_1 = []
f_1 = []
I_2 = []
f_2 = []
I_3 = []
f_3 = []
I_4 = []
f_4 = []
I_5 = []
f_5 = []

### ax1
ax1.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Na}}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_everywhere_Na_Kv2l_SK       = []
I_dur_everywhere_Na_Kv2l_SK     = []
dur_sprx_Na_Kv2l_SK             = []
I_dur_sprx_Na_Kv2l_SK           = []
for k in range(Ng):
    cm = cms[k]
    changedg = varygs[k]
    varyENa  = varyENas[k] 
    varyEK   = varyEKs[k] 
    varyEpas = varyEpases[k] 
    namestring = 'ENa'+str(varyENa)+'_gKv2like'+str(changedg)+'p'+'_gSK'+str(changedg)+'p'
    plotlabel = r'$c_\mathregular{m}$=%.1f, ' % (cm)
    g = changedg
    plotlabel = plotlabel + r'$E_{\mathregular{Na}}$=%i, ' % varyENa
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{Kv2like}}$=%.1f, ' % g
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{SK}}$=%.1f' % g
    
    ## Somaprox
    dur_sprx   = []
    I_dur_sprx = []
    
    infilename_dur = infolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_sdurat%s_vs_I.txt' % str(spikedurat)
    
    # Read files
    infile_dur = open(infilename_dur,'r')
    
    lines_dur = infile_dur.readlines()
    Nlines_dur = len(lines_dur)
    
    for i in range(Nlines_dur):
        words_dur = lines_dur[i].split()
        if len(words_dur)>0:
            I_dur_sprx.append(float(words_dur[0]))
            dur_sprx.append(float(words_dur[1]))
    
    infile_dur.close()
    
    if cm==1.0:
        thelinewidth = defaultwidth
        I_default = I_dur_sprx
        f_default = dur_sprx
    else:
        thelinewidth = mylinewidth
        I_1 = I_dur_sprx
        f_1 = dur_sprx

    ax1.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax2

ax2.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_cao_SK         = []
I_dur_sprx_cao_SK       = []
for k in range(Ng):
    cm       = cms[k]
    cao      = varycao[k] 
    changedg = varygs[k]
    varyENa  = varyENas[k] 
    varyEK   = varyEKs[k] 
    varyEpas = varyEpases[k] 
    varyECa0 = ECa0[k]
    namestring = '_cao'+str(cao)+'_gSK'+str(changedg)+'p'
    plotlabel = r'$c_\mathregular{m}$=%.1f, ' % (cm)
    g = changedg
    plotlabel = plotlabel + r'$E_{\mathregular{Ca}}(0)$=%.2f, ' % varyECa0
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{SK}}$=%.1f' % g
    
    ## Somaprox
    dur_sprx   = []
    I_dur_sprx = []
    
    infilename_dur = infolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_sdurat%s_vs_I.txt' % str(spikedurat)
    
    # Read files
    infile_dur = open(infilename_dur,'r')
    
    lines_dur = infile_dur.readlines()
    Nlines_dur = len(lines_dur)
    
    for i in range(Nlines_dur):
        words_dur = lines_dur[i].split()
        if len(words_dur)>0:
            I_dur_sprx.append(float(words_dur[0]))
            dur_sprx.append(float(words_dur[1]))
    
    infile_dur.close()
    
    if cm==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
        I_2 = I_dur_sprx
        f_2 = dur_sprx
    ax2.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax3

ax3.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA         = []
I_dur_sprx_Na_CaHVA       = []
for k in range(Ng):
    cm = cms[k]
    thiscao  = varycao[k]
    changedg = varygs[k]
    varyENa  = varyENas[k] 
    varyEK   = varyEKs[k] 
    varyEpas = varyEpases[k] 
    varyECa0 = ECa0[k]
    namestring = '_cao'+str(thiscao)+'_gKv2like'+str(changedg)+'p'+'_gSK'+str(changedg)+'p'
    plotlabel = r'$c_\mathregular{m}$=%.1f, ' % (cm)
    g = changedg
    plotlabel = plotlabel + r'$E_{\mathregular{Ca}}(0)$=%.2f' % varyECa0
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{Kv2like}}$=%.1f, ' % g
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{SK}}$=%.1f' % g
    
    ## Somaprox
    dur_sprx   = []
    I_dur_sprx = []
    
    infilename_dur = infolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_sdurat%s_vs_I.txt' % str(spikedurat)
    
    # Read files
    infile_dur = open(infilename_dur,'r')
    
    lines_dur = infile_dur.readlines()
    Nlines_dur = len(lines_dur)
    
    for i in range(Nlines_dur):
        words_dur = lines_dur[i].split()
        if len(words_dur)>0:
            I_dur_sprx.append(float(words_dur[0]))
            dur_sprx.append(float(words_dur[1]))
    
    infile_dur.close()
    
    if cm==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
        I_3 = I_dur_sprx
        f_3 = dur_sprx
    ax3.plot(I_dur_sprx, dur_sprx,color=colors[k],label='%s' % combos[k], linewidth=thelinewidth)

## ax4

ax4.set_title(r'Vary $c_\mathregular{m}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA         = []
I_dur_sprx_Na_CaHVA       = []
for k in range(Ng):
    cm = cms[k]
    thiscao  = varycao[k]
    changedg = varygs[k]
    varyENa  = varyENas[k] 
    varyEK   = varyEKs[k] 
    varyEpas = varyEpases[k] 
    varyECa0 = ECa0[k]
    namestring = '_gKv2like'+str(changedg)+'p'+'_gSK'+str(changedg)+'p'
    plotlabel = r'$c_\mathregular{m}$=%.1f, ' % (cm)
    g = changedg
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{Kv2like}}$=%.1f, ' % g
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{SK}}$=%.1f' % g
    
    ## Somaprox
    dur_sprx   = []
    I_dur_sprx = []
    
    infilename_dur = infolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_sdurat%s_vs_I.txt' % str(spikedurat)
    
    # Read files
    infile_dur = open(infilename_dur,'r')
    
    lines_dur = infile_dur.readlines()
    Nlines_dur = len(lines_dur)
    
    for i in range(Nlines_dur):
        words_dur = lines_dur[i].split()
        if len(words_dur)>0:
            I_dur_sprx.append(float(words_dur[0]))
            dur_sprx.append(float(words_dur[1]))
    
    infile_dur.close()
    
    if cm==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
        I_4 = I_dur_sprx
        f_4 = dur_sprx
    
    ax4.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax5

ax5.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$, $E_{\mathregular{Na}}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA         = []
I_dur_sprx_Na_CaHVA       = []
for k in range(Ng):
    cm = cms[k]
    thiscao  = varycao[k]
    changedg = varygs[k]
    varyENa  = varyENas[k] 
    varyEK   = varyEKs[k] 
    varyEpas = varyEpases[k] 
    varyECa0 = ECa0[k]
    namestring = '_cao'+str(thiscao)+'ENa'+str(varyENa)+'_gKv2like'+str(changedg)+'p'+'_gSK'+str(changedg)+'p'
    plotlabel = r'$c_\mathregular{m}$=%.1f, ' % (cm)
    g = changedg
    plotlabel = plotlabel + r'$E_{\mathregular{Ca}}(0)$=%.2f' % varyECa0
    plotlabel = plotlabel + r'$E_{\mathregular{Na}}$=%i' % varyENa
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{Kv2like}}$=%.1f, ' % g
    plotlabel = plotlabel + r'$\bar{g}_{\mathregular{SK}}$=%.1f' % g
    
    ## Somaprox
    dur_sprx   = []
    I_dur_sprx = []
    
    infilename_dur = infolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_sdurat%s_vs_I.txt' % str(spikedurat)
    
    # Read files
    infile_dur = open(infilename_dur,'r')
    
    lines_dur = infile_dur.readlines()
    Nlines_dur = len(lines_dur)
    
    for i in range(Nlines_dur):
        words_dur = lines_dur[i].split()
        if len(words_dur)>0:
            I_dur_sprx.append(float(words_dur[0]))
            dur_sprx.append(float(words_dur[1]))
    
    infile_dur.close()
    
    if cm==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
        I_5 = I_dur_sprx
        f_5 = dur_sprx
    
    ax5.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)


Is = [I_1,I_2,I_3,I_4,I_5]
fs = [f_1,f_2,f_3,f_4,f_5]
lastdiff1 = []
for i in range(5):
    im, rd1 = reldiffs(fs[i],f_default,Is[i],I_default) 
    if len(rd1)>0:
        lastdiff1.append(rd1[-1])

barWidth = 0.5
br1 = np.arange(len(lastdiff1))
br2 = [x+barWidth for x in br1]

ax6.bar(br1, lastdiff1, width=barWidth,color='tab:red')

ax6.axhline(y=0,color='k',linewidth=1.0)
plt.xticks(br1, ['A','B','C','D','E'])
ax6.set_xlabel('Combination',fontsize=14)
ax6.set_ylabel(r'Relative difference at max. current',fontsize=14)
ax6.set_title(r'Difference between Combination 2 and default',fontsize=18)

## xlabel ##
ax1.set_xlabel('$I$ (nA)',fontsize=14)
ax2.set_xlabel('$I$ (nA)',fontsize=14)
ax3.set_xlabel('$I$ (nA)',fontsize=14)
ax4.set_xlabel('$I$ (nA)',fontsize=14)
ax5.set_xlabel('$I$ (nA)',fontsize=14)
## ylabel ##
ax1.set_ylabel('Duration (ms)',fontsize=14)
ax2.set_ylabel('Duration (ms)',fontsize=14)
ax3.set_ylabel('Duration (ms)',fontsize=14)
ax4.set_ylabel('Duration (ms)',fontsize=14)
ax5.set_ylabel('Duration (ms)',fontsize=14)
## legend ##
ax1.legend(loc='center left',ncol=1)
ax2.legend(loc='center left',ncol=1)
ax3.legend(loc='center left',ncol=1)
ax4.legend(loc='center left',ncol=1)
ax5.legend(loc='center left',ncol=1)


fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(plotname)

plt.show()
