import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

iamp = 0.5

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

fig = plt.figure(figsize=(20,20),dpi=300)

gs = gridspec.GridSpec(4, 6)

ax1 = plt.subplot(gs[0, 0:2])
ax2 = plt.subplot(gs[0, 2:4])
ax3 = plt.subplot(gs[0, 4:6])
ax4 = plt.subplot(gs[1, 1:3])
ax5 = plt.subplot(gs[1, 3:5])
ax6 = plt.subplot(gs[2, 0:2])
ax7 = plt.subplot(gs[2, 2:4])
ax8 = plt.subplot(gs[2, 4:6])
ax9 = plt.subplot(gs[3, 0:2])
ax10 = plt.subplot(gs[3, 2:4])
ax11 = plt.subplot(gs[3, 4:6])

ax1.set_title(r'A',loc='left',fontsize=18)
ax2.set_title(r'B',loc='left',fontsize=18)
ax3.set_title(r'C',loc='left',fontsize=18)
ax4.set_title(r'D',loc='left',fontsize=18)
ax5.set_title(r'E',loc='left',fontsize=18)
ax6.set_title(r'F',loc='left',fontsize=18)
ax7.set_title(r'G',loc='left',fontsize=18)
ax8.set_title(r'H',loc='left',fontsize=18)
ax9.set_title(r'I',loc='left',fontsize=18)
ax10.set_title(r'J',loc='left',fontsize=18)
ax11.set_title(r'K',loc='left',fontsize=18)

plotname = 'figures/Comparemodels/varyseveraltogether_shapes_reflabels_somaprox_selected_big_tracedur.png'

testmodel  = 478513437
idur       = 2000 # ms
idelay     = 100
v_init     = -86.8 # mV
Ra         = 150
somasize   = 10 
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
spikedurat = -40

varymech = 'None' # 'Na' # 'K' # 'pas'
namestring = ''

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

cms        = [1.0,1.5,1.5,1.5,1.5]
varygs     = [1.0,1.5,2.0,3.0,4.0]
varycao    = [2.0,20.0,20.0,20.0,20.0]
varyENas   = [53,63,63,63,63]
varyEKs    = [-107,-107,-107,-107,-107]
varyEpases = [0,0,0,0,0]
combos     = ['Default','1', '2', '3', '4','5','6','7','8','9','10']
Ncms       = len(cms) 

colors = ['k']
for i in range(Ncms-1):
    colors.append((0.5-i/(2.0*Ncms),0,0.5+i/float(2.0*Ncms),1.0-i/float(Ncms)))

for i in range(1,Ncms):
    if varygs[i]==1.5:
        combos[i] =  r'%.1f$\bar{g}_X$' % varygs[i]
    else:
        combos[i] =  r'%i$\bar{g}_X$' % varygs[i]

cm_dend = 2.34539964752
cm_axon = 2.34539964752

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

NI = len(i_master)
Ng = len(varygs)

i_master_everywhere = []

infolder      = 'figures/%i/current_idur%i_iamp' % (testmodel,idur) + str(iamp)+'/'
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
dur_everywhere_Na_Kv2l_SK   = []
I_dur_everywhere_Na_Kv2l_SK = []
dur_sprx_Na_Kv2l_SK         = []
I_dur_sprx_Na_Kv2l_SK       = []

startind = 32500
endind   = 32800
shifts   = [0]
shifts.append(265)
shifts.append(-106)
shifts.append(-262)
shifts.append(248)
startinds = [startind]
startinds.append(startind-shifts[1])
startinds.append(startind-shifts[2])
startinds.append(startind-shifts[3])
startinds.append(startind-shifts[4])
endinds   = [endind]
endinds.append(endind-shifts[1])
endinds.append(endind-shifts[2])
endinds.append(endind-shifts[3])
endinds.append(endind-shifts[4])
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
    
    infilename_dur = infolder+namestring+"_changecmf" + str(cm) + "_somaprox_vinit"+str(v_init)+"_addedRa.txt"
    
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

    ax1.plot(I_dur_sprx[startinds[k]+shifts[k]:endinds[k]+shifts[k]], dur_sprx[startinds[k]:endinds[k]],color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax2

ax2.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_cao_SK   = []
I_dur_sprx_cao_SK = []

shifts   = [0]
shifts.append(169)
shifts.append(412)
shifts.append(47)
shifts.append(-140)
startinds = [startind]
startinds.append(startind-shifts[1])
startinds.append(startind-shifts[2])
startinds.append(startind-shifts[3])
startinds.append(startind-shifts[4])
endinds   = [endind]
endinds.append(endind-shifts[1])
endinds.append(endind-shifts[2])
endinds.append(endind-shifts[3])
endinds.append(endind-shifts[4])
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
    
    infilename_dur = infolder+namestring+"_changecmf" + str(cm) + "_somaprox_vinit"+str(v_init)+"_addedRa.txt"
    
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
    ax2.plot(I_dur_sprx[startinds[k]+shifts[k]:endinds[k]+shifts[k]], dur_sprx[startinds[k]:endinds[k]],color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax3

ax3.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA   = []
I_dur_sprx_Na_CaHVA = []

shifts   = [0]
shifts.append(156)
shifts.append(-331)
shifts.append(591)
shifts.append(-220)
startinds = [startind]
startinds.append(startind-shifts[1])
startinds.append(startind-shifts[2])
startinds.append(startind-shifts[3])
startinds.append(startind-shifts[4])
endinds   = [endind]
endinds.append(endind-shifts[1])
endinds.append(endind-shifts[2])
endinds.append(endind-shifts[3])
endinds.append(endind-shifts[4])
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
    
    infilename_dur = infolder+namestring+"_changecmf" + str(cm) + "_somaprox_vinit"+str(v_init)+"_addedRa.txt"
    
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
    ax3.plot(I_dur_sprx[startinds[k]+shifts[k]:endinds[k]+shifts[k]], dur_sprx[startinds[k]:endinds[k]],color=colors[k],label='%s' % combos[k], linewidth=thelinewidth)

## ax4

ax4.set_title(r'Vary $c_\mathregular{m}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA   = []
I_dur_sprx_Na_CaHVA = []

shifts   = [0]
shifts.append(-159)
shifts.append(398)
shifts.append(201)
shifts.append(623)
startinds = [startind]
startinds.append(startind-shifts[1])
startinds.append(startind-shifts[2])
startinds.append(startind-shifts[3])
startinds.append(startind-shifts[4])
endinds   = [endind]
endinds.append(endind-shifts[1])
endinds.append(endind-shifts[2])
endinds.append(endind-shifts[3])
endinds.append(endind-shifts[4])
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
    
    infilename_dur = infolder+namestring+"_changecmf" + str(cm) + "_somaprox_vinit"+str(v_init)+"_addedRa.txt"
    
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
    
    ax4.plot(I_dur_sprx[startinds[k]+shifts[k]:endinds[k]+shifts[k]], dur_sprx[startinds[k]:endinds[k]],color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax5

ax5.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$, $E_{\mathregular{Na}}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA   = []
I_dur_sprx_Na_CaHVA = []

shifts   = [0]
shifts.append(-260)
shifts.append(415)
shifts.append(321)
shifts.append(-479)
startinds = [startind]
startinds.append(startind-shifts[1])
startinds.append(startind-shifts[2])
startinds.append(startind-shifts[3])
startinds.append(startind-shifts[4])
endinds   = [endind]
endinds.append(endind-shifts[1])
endinds.append(endind-shifts[2])
endinds.append(endind-shifts[3])
endinds.append(endind-shifts[4])
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
    
    infilename_dur = infolder+namestring+"_changecmf" + str(cm) + "_somaprox_vinit"+str(v_init)+"_addedRa.txt"
    
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
    
    ax5.plot(I_dur_sprx[startinds[k]+shifts[k]:endinds[k]+shifts[k]], dur_sprx[startinds[k]:endinds[k]],color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## xlabel ##
ax1.set_xlabel('$t$ (ms)',fontsize=14)
ax2.set_xlabel('$t$ (ms)',fontsize=14)
ax3.set_xlabel('$t$ (ms)',fontsize=14)
ax4.set_xlabel('$t$ (ms)',fontsize=14)
ax5.set_xlabel('$t$ (ms)',fontsize=14)
## ylabel ##
ax1.set_ylabel('$V$ (mV)',fontsize=14)
ax2.set_ylabel('$V$ (mV)',fontsize=14)
ax3.set_ylabel('$V$ (mV)',fontsize=14)
ax4.set_ylabel('$V$ (mV)',fontsize=14)
ax5.set_ylabel('$V$ (mV)',fontsize=14)
## legend ##
ax1.legend(loc='upper left',ncol=1)
ax2.legend(loc='upper left',ncol=1)
ax3.legend(loc='upper left',ncol=1)
ax4.legend(loc='upper left',ncol=1)
ax5.legend(loc='upper left',ncol=1)

############################################### DURS ##############################################################
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

NI = len(i_master)
Ng = len(varygs)

i_master_everywhere = []

infolder    = 'figures/%i/' % (testmodel)
vrestfolder = infolder 

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


I_1_all = []
f_1_all = []
I_2_all = []
f_2_all = []
I_3_all = []
f_3_all = []
I_4_all = []
f_4_all = []
I_5_all = []
f_5_all = []

### ax6
ax6.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Na}}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_everywhere_Na_Kv2l_SK   = []
I_dur_everywhere_Na_Kv2l_SK = []
dur_sprx_Na_Kv2l_SK         = []
I_dur_sprx_Na_Kv2l_SK       = []
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
        I_1_all.append(I_dur_sprx)
        f_1_all.append(dur_sprx)

    ax6.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax7

ax7.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_cao_SK   = []
I_dur_sprx_cao_SK = []
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
        I_2_all.append(I_dur_sprx)
        f_2_all.append(dur_sprx)
    ax7.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax8

ax8.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA   = []
I_dur_sprx_Na_CaHVA = []
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
    print('infilename_dur:',infilename_dur)
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
        I_3_all.append(I_dur_sprx)
        f_3_all.append(dur_sprx)
    ax8.plot(I_dur_sprx, dur_sprx,color=colors[k],label='%s' % combos[k], linewidth=thelinewidth)
    print('plotted')

## ax9

ax9.set_title(r'Vary $c_\mathregular{m}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA   = []
I_dur_sprx_Na_CaHVA = []
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
        I_4_all.append(I_dur_sprx)
        f_4_all.append(dur_sprx)
    
    ax9.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)

## ax10

ax10.set_title(r'Vary $c_\mathregular{m}$, $E_{\mathregular{Ca}}(0)$, $E_{\mathregular{Na}}$, $\bar{g}_{\mathregular{Kv2like}}$ and $\bar{g}_{\mathregular{SK}}$',fontsize=18)
dur_sprx_Na_CaHVA   = []
I_dur_sprx_Na_CaHVA = []
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
        I_5_all.append(I_dur_sprx)
        f_5_all.append(dur_sprx)
    
    ax10.plot(I_dur_sprx, dur_sprx,color=colors[k],label=r'%s' % combos[k], linewidth=thelinewidth)


Is = [I_1,I_2,I_3,I_4,I_5]
fs = [f_1,f_2,f_3,f_4,f_5]
lastdiff1 = []
for i in range(5):
    im, rd1 = reldiffs(fs[i],f_default,Is[i],I_default) 
    if len(rd1)>0:
        lastdiff1.append(rd1[-1])

rds = []
lastdiffs = []
for i in range(Ncms-1):
    lastdiff = []
    Is = [I_1_all[i],I_2_all[i],I_3_all[i],I_4_all[i],I_5_all[i]]
    fs = [f_1_all[i],f_2_all[i],f_3_all[i],f_4_all[i],f_5_all[i]]
    for j in range(5):
        imi, rdi = reldiffs(fs[j],f_default,Is[j],I_default) 
        if len(rdi)>0:
            lastdiff.append(rdi[-1])
        else:
            lastdiff.append(0)
    lastdiffs.append(lastdiff)

barWidth = 0.1
br1  = np.arange(len(lastdiffs[0]))
br2  = [x+barWidth for x in br1]
br3  = [x+2*barWidth for x in br1]
br4  = [x+3*barWidth for x in br1]
br5  = [x+4*barWidth for x in br1]
br6  = [x+5*barWidth for x in br1]
br7  = [x+6*barWidth for x in br1]
br8  = [x+7*barWidth for x in br1]
br9  = [x+6*barWidth for x in br1]
br10 = [x+7*barWidth for x in br1]
brcenter = [x+((Ncms-1)/2.+0.5)*barWidth for x in br1]

ax11.bar(br1, lastdiffs[0],width=barWidth,color=colors[1],label=combos[1])
ax11.bar(br2, lastdiffs[1],width=barWidth,color=colors[2],label=combos[2])
ax11.bar(br3, lastdiffs[2],width=barWidth,color=colors[3],label=combos[3])
ax11.bar(br4, lastdiffs[3],width=barWidth,color=colors[4],label=combos[4])
ax11.legend(loc='lower left',ncol=4,fontsize=15)

ax11.axhline(y=0,color='k',linewidth=1.0)
plt.xticks(br1, ['F','G','H','I','J'])
ax11.set_xlabel('Combination',fontsize=14)
ax11.set_ylabel(r'Relative difference at max. current',fontsize=14)
ax11.set_title(r'Difference from default',fontsize=18)
ax11.set_ylim([-0.30,0])


## xlabel ##
ax6.set_xlabel('$I$ (nA)',fontsize=14)
ax7.set_xlabel('$I$ (nA)',fontsize=14)
ax8.set_xlabel('$I$ (nA)',fontsize=14)
ax9.set_xlabel('$I$ (nA)',fontsize=14)
ax10.set_xlabel('$I$ (nA)',fontsize=14)
## ylabel ##
ax6.set_ylabel('Duration (ms)',fontsize=14)
ax7.set_ylabel('Duration (ms)',fontsize=14)
ax8.set_ylabel('Duration (ms)',fontsize=14)
ax9.set_ylabel('Duration (ms)',fontsize=14)
ax10.set_ylabel('Duration (ms)',fontsize=14)
## legend ##
ax6.legend(loc='center left',ncol=1)
ax7.legend(loc='center left',ncol=1)
ax8.legend(loc='center right',ncol=1)
ax9.legend(loc='center left',ncol=1)
ax10.legend(loc='center left',ncol=1)

fig.tight_layout()
plt.savefig(plotname)

plt.show()
