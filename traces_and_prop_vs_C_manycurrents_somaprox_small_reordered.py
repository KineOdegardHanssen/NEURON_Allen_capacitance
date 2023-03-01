import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

# change the default font family
plt.rcParams.update({'font.family':'Arial'})

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
plt.rc('legend', fontsize=14)

fig = plt.figure(figsize=(15,17),dpi=300)

gs = gridspec.GridSpec(3, 4)

ax1 = plt.subplot(gs[0, 0:2])
ax2 = plt.subplot(gs[0, 2:4])
ax3 = plt.subplot(gs[1, 0:2])
ax4 = plt.subplot(gs[1, 2:4])
ax5 = plt.subplot(gs[2, 0:2])
ax6 = plt.subplot(gs[2, 2:4])

plotcolors = ['tab:blue','tab:orange','k','tab:purple','tab:green','tab:brown','tab:grey','tab:olive','tab:green','tab:cyan']
plotcolors_2 = ['tab:orange','k','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:grey','tab:olive','tab:cyan']

tracecms = [1.0,1.5]
tracedur = 500

mylinewidth = 2
defaultwidth = 3

idur       = 1000 # ms
idelay     = 100
iamp       = 0.2 # nA
iamp2      = 0.4
v_init     = -86.5 # mV
Ra         = 150
somasize   = 10
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
spikedurat = -40

#################### Soma only, Hodgkin-Huxley #########################################
Nspikes          = []
avg_AP_halfwidth = []
rms_AP_halfwidth = []
Cm_Nspikes       = []
Cm_AP_halfwidth  = []

# Default HH values:
ena = 50
ek = -77
el_hh = -54.3
gnabar_hh = 0.12
gkbar_hh = 0.036
gl_hh = 0.0003

infolder_shh = 'Somaonly/Results/IStim/Soma%i/' % somasize
currentfolder = 'current_idur%i_iamp'%idur+str(iamp)+'/'
infolder_shh  = infolder_shh+currentfolder
hhstring = '_ena'+str(ena)+'_ek'+str(ek)+'_el'+str(el_hh)+'_gnabar'+str(gnabar_hh)+'_gkbar'+str(gkbar_hh)+'_gl'+str(gl_hh)
infilename_Nspikes = infolder_shh+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cm.txt'
infilename_APdhw   = infolder_shh+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cm.txt' % str(spikedurat)
infile_Nspikes = open(infilename_Nspikes,'r')
infile_APdhw   = open(infilename_APdhw,'r')

lines_Nspikes = infile_Nspikes.readlines()
lines_APdhw   = infile_APdhw.readlines()
Nlines = len(lines_Nspikes) # All data types have the same length

for i in range(Nlines):
    words_Nspikes = lines_Nspikes[i].split()
    words_APdhw   = lines_APdhw[i].split()
    if len(words_Nspikes)>0:
        Cm_Nspikes.append(float(words_Nspikes[0]))
        Nspikes.append(float(words_Nspikes[1]))
    if len(words_APdhw)>0:
        Cm_AP_halfwidth.append(float(words_APdhw[0]))
        avg_AP_halfwidth.append(float(words_APdhw[1]))
        rms_AP_halfwidth.append(float(words_APdhw[2]))

infile_Nspikes.close()
infile_APdhw.close()

if np.sum(Nspikes)>0:
    ax3.plot(Cm_Nspikes, Nspikes,label=r'OC',color=plotcolors[0], linewidth=mylinewidth)
    ax5.errorbar(Cm_AP_halfwidth, avg_AP_halfwidth, yerr=rms_AP_halfwidth,color=plotcolors[0],label=r'OC', capsize=2, linewidth=mylinewidth)

####################### Ball-and-stick #######################################
varymech = 'Na'
varyE_bool = True
varyE = 50 
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

cm_master = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
    
NCms = len(cm_master)

Nspikes          = []
avg_AP_halfwidth = []
rms_AP_halfwidth = []
Cm_Nspikes       = []
Cm_AP_halfwidth  = []
    
# Set names
infolder = 'Ball-and-stick models/BAS_somaHH_dendpassive/Results/IStim/Soma%i/dendlen%i/denddiam'% (somasize,dendlen)+str(denddiam)+'/'
currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
infolder = infolder+currentfolder
infilename_Nspikes = infolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cmall.txt'
infilename_APdhw   = infolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmall.txt'% str(spikedurat) 
plotfolder = 'Comparemodels/All/'
plotname_all = plotfolder+'traces_and_features_vs_Cm_idur%i_iamp'%idur+str(iamp)+'_'+str(iamp2)+'_somaprox_winset_reordered.png'
# Read files
infile_Nspikes = open(infilename_Nspikes,'r')
infile_APdhw   = open(infilename_APdhw,'r')

lines_Nspikes = infile_Nspikes.readlines()
lines_APdhw   = infile_APdhw.readlines()
Nlines_Nspikes = len(lines_Nspikes)
Nlines_APdhw   = len(lines_APdhw)

for i in range(Nlines_Nspikes):
    words_Nspikes = lines_Nspikes[i].split()
    if len(words_Nspikes)>0:
        Cm_Nspikes.append(float(words_Nspikes[0]))
        Nspikes.append(float(words_Nspikes[1]))

for i in range(Nlines_APdhw):
    words_APdhw   = lines_APdhw[i].split()
    if len(words_APdhw)>0:
        Cm_AP_halfwidth.append(float(words_APdhw[0]))
        avg_AP_halfwidth.append(float(words_APdhw[1]))
        rms_AP_halfwidth.append(float(words_APdhw[2]))

infile_Nspikes.close()
infile_APdhw.close()


# Plotting

ax3.plot(Cm_Nspikes, Nspikes,label=r'BAS all',color=plotcolors[1], linewidth=mylinewidth)
ax3.set_xlabel(r'$c_\mathregular{m}/c_\mathregular{m0}$',fontsize=14)
ax3.set_ylabel('$f$ (Hz)',fontsize=14)

ax5.errorbar(Cm_AP_halfwidth, avg_AP_halfwidth, yerr=rms_AP_halfwidth,color=plotcolors[1],label=r'BAS, all', capsize=2, linewidth=mylinewidth)
ax5.set_xlabel(r'$c_\mathregular{m}/c_\mathregular{m0}$',fontsize=14)
ax5.set_ylabel('Spike duration [ms]',fontsize=14)


############# SOMAPROX ##################################
Nspikes          = []
avg_AP_halfwidth = []
rms_AP_halfwidth = []
Cm_Nspikes       = []
Cm_AP_halfwidth  = []
    
# Set names
infolder = 'Ball-and-stick models/BAS_somaHH_dendpassive/Results/IStim/Soma%i/dendlen%i/denddiam'% (somasize,dendlen)+str(denddiam)+'/'
currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
infolder      = infolder+currentfolder
infilename_Nspikes = infolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cmsprx.txt'
infilename_APdhw   = infolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmsprx.txt'% str(spikedurat) 
# Read files
infile_Nspikes = open(infilename_Nspikes,'r')
infile_APdhw   = open(infilename_APdhw,'r')

lines_Nspikes = infile_Nspikes.readlines()
lines_APdhw   = infile_APdhw.readlines()
Nlines_Nspikes = len(lines_Nspikes)
Nlines_APdhw   = len(lines_APdhw)

for i in range(Nlines_Nspikes):
    words_Nspikes = lines_Nspikes[i].split()
    if len(words_Nspikes)>0:
        Cm_Nspikes.append(float(words_Nspikes[0]))
        Nspikes.append(float(words_Nspikes[1]))


for i in range(Nlines_APdhw):
    words_APdhw   = lines_APdhw[i].split()
    if len(words_APdhw)>0:
        Cm_AP_halfwidth.append(float(words_APdhw[0]))
        avg_AP_halfwidth.append(float(words_APdhw[1]))
        rms_AP_halfwidth.append(float(words_APdhw[2]))

infile_Nspikes.close()
infile_APdhw.close()

ax3.plot(Cm_Nspikes, Nspikes,label=r'BAS sprx',ls='--',color=plotcolors[1], linewidth=mylinewidth)
ax5.errorbar(Cm_AP_halfwidth, avg_AP_halfwidth, yerr=rms_AP_halfwidth,ls='--',color=plotcolors[1],label=r'BAS sprx', capsize=2, linewidth=mylinewidth)

################## ADDING THRESHOLDS AT THE END: #######################################
Ncm_somaHH        = 6
infolder_thr      = 'Ball-and-stick models/BAS_somaHH_dendpassive/Results/IStim/Soma%i/dendlen%i/denddiam%i/' % (somasize,dendlen,denddiam)+folderstring
infolder_thr_soma = 'Somaonly/Results/IStim/Soma%i/' % somasize
infilename_all    = infolder_thr + 'thresholds_bashhdpas_everywhere_varyfactor'+plotstring+'.txt' 
infilename_sprx   = infolder_thr + 'thresholds_bashhdpas_somaprox_varyfactor'+plotstring+'.txt' 
infilename_soma   = infolder_thr_soma + 'thresholds_somaonlyHH_varycmfactor_%icms_idur%i' % (Ncm_somaHH,idur)+hhstring+'.txt'

infile_all  = open(infilename_all,'r')
infile_sprx = open(infilename_sprx,'r')
infile_soma = open(infilename_soma,'r')
lines_all   = infile_all.readlines()
lines_sprx  = infile_sprx.readlines()
lines_soma  = infile_soma.readlines()

cm_all    = []
cm_sprx   = []
cm_soma   = []
thrs_all  = []
thrs_sprx = []
thrs_soma = []

for line in lines_all:
    words = line.split()
    if len(words)>0:
        cm_all.append(float(words[0]))
        thrs_all.append(float(words[1]))

for line in lines_sprx:
    words = line.split()
    if len(words)>0:
        cm_sprx.append(float(words[0]))
        thrs_sprx.append(float(words[1]))

for line in lines_soma:
    words = line.split()
    if len(words)>0:
        cm_soma.append(float(words[0]))
        thrs_soma.append(float(words[1]))

cm_all    = np.array(cm_all)
cm_sprx   = np.array(cm_sprx)
cm_soma   = np.array(cm_soma)
thrs_all  = np.array(thrs_all)
thrs_sprx = np.array(thrs_sprx)
thrs_soma = np.array(thrs_soma)


# Plotting

ax2.plot(cm_soma,thrs_soma,label=r'OC',color=plotcolors[0], linewidth=mylinewidth)
ax2.plot(cm_all,thrs_all,label=r'BAS all',color=plotcolors[1], linewidth=mylinewidth)
ax2.plot(cm_sprx,thrs_sprx,label=r'BAS sprx',ls='--',color=plotcolors[1], linewidth=mylinewidth)

ax2.set_title(r'Threshold current',fontsize=15)
ax2.set_xlabel(r'$c_\mathregular{m}/c_\mathregular{m0}$',fontsize=14)
ax2.set_ylabel(r'Threshold current (nA)',fontsize=14)

#### PLOTTING ALLEN #####

testmodels = [478513437,488462965,478513407]
idur       = 2000 # ms
idelay     = 100
iamp       = 0.2 # nA
v_init     = -86.5 # mV
Ra         = 150
somasize   = 10  
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
Nmodels    = len(testmodels)
spikedurat = -40

varymech = 'Kd'
varyE_bool = True
varyE = -107 
varyg = 'None'

plotstring = '_vary'
if varyE_bool==True:
    plotstring = plotstring + 'E'
else:
    plotstring = plotstring + 'g'

if varymech=='NaV':
    folderstring = 'VaryNa/' 
    plotstring   = plotstring + '_NaV'
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

cm_master = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
    
NCms = len(cm_master)

Nspikes_all          = []
avg_AP_halfwidth_all = []
rms_AP_halfwidth_all = []
Cm_Nspikes_all       = []
Cm_AP_halfwidth_all  = []
    
for testmodel in testmodels:
    Nspikes          = []
    Cm_Nspikes       = []
    Cm_AP_halfwidth  = []
    avg_AP_halfwidth = []
    rms_AP_halfwidth = []
    
    # Set names
    infolder      = 'Allen_test_changecapacitance/figures/%i/' % (testmodel)
    currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
    infolder = infolder+currentfolder
    infilename_Nspikes = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Nspikes_vs_Cmall.txt'
    infilename_APdhw   = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmall.txt' % str(spikedurat)
    # Read files
    infile_Nspikes = open(infilename_Nspikes,'r')
    infile_APdhw   = open(infilename_APdhw,'r')
    
    lines_Nspikes = infile_Nspikes.readlines()
    lines_APdhw   = infile_APdhw.readlines()
    Nlines = len(lines_Nspikes) # All data types have the same length
    
    for i in range(Nlines):
        words_Nspikes = lines_Nspikes[i].split()
        words_APdhw   = lines_APdhw[i].split()
        if len(words_Nspikes)>0:
            Cm_Nspikes.append(float(words_Nspikes[0]))
            Nspikes.append(float(words_Nspikes[1]))
        if len(words_APdhw)>0:
            Cm_AP_halfwidth.append(float(words_APdhw[0]))
            avg_AP_halfwidth.append(float(words_APdhw[1]))
            rms_AP_halfwidth.append(float(words_APdhw[2]))
    
    infile_Nspikes.close()
    infile_APdhw.close()
    
    Nspikes_all.append(Nspikes)
    avg_AP_halfwidth_all.append(avg_AP_halfwidth)
    rms_AP_halfwidth_all.append(rms_AP_halfwidth)
    Cm_Nspikes_all.append(Cm_Nspikes)
    Cm_AP_halfwidth_all.append(Cm_AP_halfwidth)

Nspikes     = np.zeros(NCms)
Nspikes_rms = np.zeros(NCms)
avg_AP_halfwidth = np.zeros(NCms)
rms_AP_halfwidth = np.zeros(NCms)

Nspikes_bucket   = np.zeros((NCms,Nmodels))

Nspikes_collections = []
avg_AP_halfwidth_collections = []
rms_AP_halfwidth_collections = []

fcounter    = np.zeros(NCms)
hwcounter   = np.zeros(NCms)

for i in range(Nmodels):
    Nspikes_this = Nspikes_all[i]
    avg_AP_halfwidth_this = avg_AP_halfwidth_all[i]
    rms_AP_halfwidth_this = rms_AP_halfwidth_all[i]
    Cm_Nspikes_this       = Cm_Nspikes_all[i]
    Cm_AP_halfwidth_this  = Cm_AP_halfwidth_all[i]
    Nspikes_collections = []
    avg_AP_halfwidth_collections = []
    rms_AP_halfwidth_collections = []
    for j in range(NCms):
        for k in range(len(Cm_Nspikes_this)):
            if Cm_Nspikes_this[k]==cm_master[j]: 
                Nspikes[j] += Nspikes_this[k]
                Nspikes_bucket[j,i] = Nspikes_this[k]
                fcounter[j]+=1 
                continue
    for j in range(NCms):
        for k in range(len(Cm_AP_halfwidth_this)):
            if Cm_AP_halfwidth_this[k]==cm_master[j]: 
                avg_AP_halfwidth[j] += avg_AP_halfwidth_this[k]
                rms_AP_halfwidth[j] += rms_AP_halfwidth_this[k]**2 # Square now, square root at the end
                hwcounter[j]+=1 
                continue

# Average and finish rms
for j in range(NCms):
    if fcounter[j]!=0:
        Nspikes[j] /= fcounter[j]
        for i in range(int(fcounter[j])):
            Nspikes_rms[j]+=(Nspikes[j]-Nspikes_bucket[j,i])**2
        Nspikes_rms[j] = np.sqrt(Nspikes_rms[j]/(fcounter[j]-1))
for j in range(NCms):
    if hwcounter[j]!=0:
        avg_AP_halfwidth[j] /= hwcounter[j]
        rms_AP_halfwidth[j]  = np.sqrt(rms_AP_halfwidth[j]/(hwcounter[j]-1))

# Plotting

cm_short = []
Nspikes_short = []
for k in range(Nmodels):
    cm_short_this = []
    Nspikes_short_this = []
    for i in range(NCms):
        if Nspikes_bucket[i,k]!=0:
            cm_short_this.append(cm_master[i])
            Nspikes_short_this.append(Nspikes_bucket[i,k])
        else:
            break
    cm_short.append(cm_short_this)
    Nspikes_short.append(Nspikes_short_this)
    

ax1.set_title(r'A',loc='left', x=-0.05,fontsize=15)
ax2.set_title(r'B',loc='left', x=-0.05,fontsize=15)
ax3.set_title(r'C',loc='left', x=-0.05,fontsize=15)
ax4.set_title(r'D',loc='left', x=-0.05,fontsize=15)
ax5.set_title(r'E',loc='left', x=-0.05,fontsize=15)
ax6.set_title(r'F',loc='left', x=-0.05,fontsize=15)

ax3.set_ylabel('$f$ (Hz)',fontsize=14)
ax5.set_ylabel('Spike duration at %s mV (ms)' % str(spikedurat),fontsize=14)


## Saving arrays for next figure:
all_cm_short             = cm_short
all_Nspikes_short        = Nspikes_short
all_Cm_AP_halfwidth_all  = Cm_AP_halfwidth_all
all_avg_AP_halfwidth_all = avg_AP_halfwidth_all
all_rms_AP_halfwidth_all = rms_AP_halfwidth_all

############################################### SOMAPROX #######################################################
Nspikes_all          = []
avg_AP_halfwidth_all = []
rms_AP_halfwidth_all = []
Cm_Nspikes_all       = []
Cm_AP_halfwidth_all  = []
    
for testmodel in testmodels:
    Nspikes          = []
    Cm_Nspikes       = []
    Cm_AP_ampl       = []
    Cm_AP_mins       = []
    Cm_AP_halfwidth  = []
    avg_AP_halfwidth = []
    rms_AP_halfwidth = []
    
    # Set names
    infolder      = 'Allen_test_changecapacitance/figures/%i/' % (testmodel)
    currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
    infolder = infolder+currentfolder
    infilename_Nspikes = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Nspikes_vs_Cmsprx.txt'
    infilename_APdhw   = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmsprx.txt' % str(spikedurat)
    # Read files
    infile_Nspikes = open(infilename_Nspikes,'r')
    infile_APdhw   = open(infilename_APdhw,'r')
    
    lines_Nspikes = infile_Nspikes.readlines()
    lines_APdhw   = infile_APdhw.readlines()
    Nlines = len(lines_Nspikes) # All data types have the same length
    
    for i in range(Nlines):
        words_Nspikes = lines_Nspikes[i].split()
        words_APdhw   = lines_APdhw[i].split()
        if len(words_Nspikes)>0:
            Cm_Nspikes.append(float(words_Nspikes[0]))
            Nspikes.append(float(words_Nspikes[1]))
        if len(words_APdhw)>0:
            Cm_AP_halfwidth.append(float(words_APdhw[0]))
            avg_AP_halfwidth.append(float(words_APdhw[1]))
            rms_AP_halfwidth.append(float(words_APdhw[2]))
    
    infile_Nspikes.close()
    infile_APdhw.close()
    
    Nspikes_all.append(Nspikes)
    avg_AP_halfwidth_all.append(avg_AP_halfwidth)
    rms_AP_halfwidth_all.append(rms_AP_halfwidth)
    Cm_Nspikes_all.append(Cm_Nspikes)
    Cm_AP_halfwidth_all.append(Cm_AP_halfwidth)

Nspikes     = np.zeros(NCms)
Nspikes_rms = np.zeros(NCms)
avg_AP_halfwidth = np.zeros(NCms)
rms_AP_halfwidth = np.zeros(NCms)

Nspikes_bucket   = np.zeros((NCms,Nmodels))

Nspikes_collections = []
avg_AP_halfwidth_collections = []
rms_AP_halfwidth_collections = []

fcounter    = np.zeros(NCms)
hwcounter   = np.zeros(NCms)

for i in range(Nmodels):
    Nspikes_this = Nspikes_all[i]
    avg_AP_halfwidth_this = avg_AP_halfwidth_all[i]
    rms_AP_halfwidth_this = rms_AP_halfwidth_all[i]
    Cm_Nspikes_this       = Cm_Nspikes_all[i]
    Cm_AP_halfwidth_this  = Cm_AP_halfwidth_all[i]
    Nspikes_collections = []
    avg_AP_halfwidth_collections = []
    rms_AP_halfwidth_collections = []
    for j in range(NCms):
        for k in range(len(Cm_Nspikes_this)):
            if Cm_Nspikes_this[k]==cm_master[j]:
                Nspikes[j] += Nspikes_this[k]
                Nspikes_bucket[j,i] = Nspikes_this[k]
                fcounter[j]+=1 
                continue
    for j in range(NCms):
        for k in range(len(Cm_AP_halfwidth_this)):
            if Cm_AP_halfwidth_this[k]==cm_master[j]:
                avg_AP_halfwidth[j] += avg_AP_halfwidth_this[k]
                rms_AP_halfwidth[j] += rms_AP_halfwidth_this[k]**2 # Square now, square root at the end
                hwcounter[j]+=1 
                continue


# Average and finish rms
for j in range(NCms):
    if fcounter[j]!=0:
        Nspikes[j] /= fcounter[j]
        for i in range(int(fcounter[j])):
            Nspikes_rms[j]+=(Nspikes[j]-Nspikes_bucket[j,i])**2
        Nspikes_rms[j] = np.sqrt(Nspikes_rms[j]/(fcounter[j]-1))
for j in range(NCms):
    if hwcounter[j]!=0:
        avg_AP_halfwidth[j] /= hwcounter[j]
        rms_AP_halfwidth[j]  = np.sqrt(rms_AP_halfwidth[j]/(hwcounter[j]-1))

cm_short = []
Nspikes_short = []
for k in range(Nmodels):
    cm_short_this = []
    Nspikes_short_this = []
    for i in range(NCms):
        if Nspikes_bucket[i,k]!=0:
            cm_short_this.append(cm_master[i])
            Nspikes_short_this.append(Nspikes_bucket[i,k])
        else:
            break
    cm_short.append(cm_short_this)
    Nspikes_short.append(Nspikes_short_this)

########################### TRACES ########################
cm_dend = 2.34539964752 # For Allen model 1
cm_axon = 2.34539964752
trvinit = -86.8
folder = 'Allen_test_changecapacitance/figures/%i/current_idur' % testmodels[0] +str(tracedur)+'_iamp'+str(iamp)+'/'
for i in range(len(tracecms)):
    cmstr = str(tracecms[i])
    tracefilename = folder+'idur%i_iamp' % tracedur + str(iamp)+'_changecmf' + str(cmstr) + '_cmdend' + str(cm_dend) + '_cmaxon'+ str(cm_axon) + '_vinit'+str(trvinit)+'_addedRa.txt'
    tracefile = open(tracefilename,'r')
    lines = tracefile.readlines()
    
    t = []
    V = []
    for line in lines:
        words = line.split()
        if len(words)>0:
            t.append(float(words[0]))
            V.append(float(words[1]))
    t = np.array(t)
    V = np.array(V)
    
    if i==0:
        V1 = V
        thiscolor='k'
        thislinewidth=3
    if i==1:
        V2 = V
        thiscolor='tab:red'
        thislinewidth=2
    ax1.plot(t,V,linewidth=thislinewidth,color=thiscolor,label=r'%s$c_\mathregular{m}$' % cmstr)

istart = 15000 
iend   = 16620 
tnew = t[istart:iend]
Vnew1 = V1[istart:iend]
Vnew2 = V2[istart:iend]
shift = 40
# Find peak times:
for i in range(1,len(tnew)-1):
    if Vnew1[i]>Vnew1[i-1] and Vnew1[i]>Vnew1[i+1]:
        tpeak1 = tnew[i]
        indpeak1 = i+istart
    if Vnew2[i]>Vnew2[i-1] and Vnew2[i]>Vnew2[i+1]:
        tpeak2 = tnew[i]
        indpeak2 = i+istart
shift = indpeak1-indpeak2
tinset2 = t[istart:iend]
Vinset2 = V2[istart-shift:iend-shift]
# Extracting max and min
Vnewmax = max(Vnew1)
Vnewmin = min(Vnew1)
Vins2max = max(Vinset2)
Vins2min = min(Vinset2)
# Normalizing:
Vn1_norm = (Vnew1-Vnewmin)/(Vnewmax-Vnewmin)
Vn2_norm = (Vinset2-Vins2min)/(Vins2max-Vins2min)
ax1b = fig.add_axes([0.06,0.82,0.095,0.08])
ax1b.plot(tnew,Vn1_norm,linewidth=3,color='k')
ax1b.plot(tinset2,Vn2_norm,linewidth=2,color='tab:red')
ax1b.axis([tnew[50]-0.01,tnew[-600],-0.1,1.1])
ax1b.set_xticks([])
ax1b.set_yticks([])
ax1.set_title('Voltage trace, Allen model 1, I = %.1f nA' % iamp ,fontsize=15)
ax1.set_xlabel('Time (ms)',fontsize=14)
ax1.set_ylabel('Membrane potential (mV)',fontsize=14)
ax1.legend(loc='lower center',ncol=2)


##### Last plot: #####################################################################################
#### Thresholds: ####

all_cm_all    = []
all_cm_sprx   = []
all_thrs_all  = []
all_thrs_sprx = []
for model in testmodels:
    infilename_all  = 'Allen_test_changecapacitance/figures/threshold_Allen_everywhere_models%s.txt' %str(model) 
    infilename_sprx = 'Allen_test_changecapacitance/figures/threshold_Allen_somaprox_models%s.txt' %str(model) 
    
    infile_all  = open(infilename_all,'r')
    infile_sprx = open(infilename_sprx,'r')
    lines_all   = infile_all.readlines()
    lines_sprx  = infile_sprx.readlines()
    
    cm_all    = []
    cm_sprx   = []
    thrs_all  = []
    thrs_sprx = []
    
    for line in lines_all:
        words = line.split()
        if len(words)>0:
            cm_all.append(float(words[0]))
            thrs_all.append(float(words[1]))

    for line in lines_sprx:
        words = line.split()
        if len(words)>0:
            cm_sprx.append(float(words[0]))
            thrs_sprx.append(float(words[1]))
        
    cm_all    = np.array(cm_all)
    cm_sprx   = np.array(cm_sprx)
    thrs_all  = np.array(thrs_all)
    thrs_sprx = np.array(thrs_sprx)
    
    # Appending for plotting
    all_cm_all.append(cm_all)
    all_cm_sprx.append(cm_sprx)
    all_thrs_all.append(thrs_all)
    all_thrs_sprx.append(thrs_sprx)

ax3.set_title(r'Frequency $f$, I = %.1f nA' % iamp,fontsize=15)
for i in range(Nmodels):
    ax3.plot(all_cm_short[i], all_Nspikes_short[i],label='A%i all' % (i+1),color=plotcolors[i+2], linewidth=2)
    ax3.plot(cm_short[i], Nspikes_short[i],ls='--',label='A%i sprx' % (i+1),color=plotcolors[i+2], linewidth=2)
ax3.set_ylabel('$f$ (Hz)',fontsize=14)
ax3.legend(loc='upper right',ncol=3)

ax5.set_title(r'Spike duration at %s mV, I = %.1f nA' % (str(spikedurat),iamp),fontsize=15)
for i in range(Nmodels):
    ax5.errorbar(all_Cm_AP_halfwidth_all[i], all_avg_AP_halfwidth_all[i], yerr=all_rms_AP_halfwidth_all[i],color=plotcolors[i+2], capsize=2,label='A%i all' % (i+1), linewidth=2)
    ax5.errorbar(Cm_AP_halfwidth_all[i], avg_AP_halfwidth_all[i], yerr=rms_AP_halfwidth_all[i], capsize=2,color=plotcolors[i+2],ls='--',label='A%i sprx' % (i+1), linewidth=2)
ax5.set_ylabel('Spike duration (ms)',fontsize=14)
ax5.legend(loc='center left',ncol=3)

ax2.set_title(r'Threshold current',fontsize=15)
for i in range(Nmodels):
    ax2.plot(all_cm_all[i], all_thrs_all[i], label='A%i all' % (i+1),color=plotcolors[i+2], linewidth=2)
    ax2.plot(all_cm_sprx[i], all_thrs_sprx[i], label='A%i sprx' % (i+1),color=plotcolors[i+2],ls='--', linewidth=2)
ax2.set_xlabel(r'$c_\mathregular{m}/c_\mathregular{m0}$',fontsize=14)
ax2.set_ylabel('Threshold current (nA)',fontsize=14)
ax2.legend(loc='lower left',bbox_to_anchor=(0, 0.1),ncol=3)

fig.tight_layout()

### Add another current: I=0.4
iamp       = iamp2 # nA

#################### Soma only, Hodgkin-Huxley #########################################
idur = 1000
Nspikes          = []
avg_AP_halfwidth = []
rms_AP_halfwidth = []
Cm_Nspikes       = []
Cm_AP_halfwidth  = []

infolder_shh = 'Somaonly/Results/IStim/Soma%i/' % somasize
currentfolder = 'current_idur%i_iamp'%idur+str(iamp)+'/'
infolder_shh  = infolder_shh+currentfolder
infilename_Nspikes = infolder_shh+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cm.txt'
infilename_APdhw   = infolder_shh+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cm.txt' % str(spikedurat)
infile_Nspikes = open(infilename_Nspikes,'r')
infile_APdhw   = open(infilename_APdhw,'r')

lines_Nspikes = infile_Nspikes.readlines()
lines_APdhw   = infile_APdhw.readlines()
Nlines        = len(lines_Nspikes)
Nlines_APdhw  = len(lines_APdhw)

for i in range(Nlines):
    words_Nspikes = lines_Nspikes[i].split()
    if len(words_Nspikes)>0:
        Cm_Nspikes.append(float(words_Nspikes[0]))
        Nspikes.append(float(words_Nspikes[1]))

for i in range(Nlines_APdhw):
    words_APdhw   = lines_APdhw[i].split()
    if len(words_APdhw)>0:
        Cm_AP_halfwidth.append(float(words_APdhw[0]))
        avg_AP_halfwidth.append(float(words_APdhw[1]))
        rms_AP_halfwidth.append(float(words_APdhw[2]))

infile_Nspikes.close()
infile_APdhw.close()

if np.sum(Nspikes)>0:
    ax4.plot(Cm_Nspikes, Nspikes,label=r'OC',color=plotcolors[0], linewidth=mylinewidth)
    ax6.errorbar(Cm_AP_halfwidth, avg_AP_halfwidth, yerr=rms_AP_halfwidth,color=plotcolors[0],label=r'OC', capsize=2, linewidth=mylinewidth)

#### PLOTTING ALLEN #####

testmodels = [478513437,488462965,478513407] 
idur       = 2000 # ms
idelay     = 100
iamp       = iamp2 # nA
v_init     = -86.5 # mV
Ra         = 150
somasize   = 10 
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
Nmodels    = len(testmodels)
spikedurat = -40

varymech = 'Kd'
varyE_bool = True
varyE = -107 
varyg = 'None'

plotstring = '_vary'
if varyE_bool==True:
    plotstring = plotstring + 'E'
else:
    plotstring = plotstring + 'g'

if varymech=='NaV':
    folderstring = 'VaryNa/' 
    plotstring   = plotstring + '_NaV'
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

cm_master = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
    
NCms = len(cm_master)

Nspikes_all          = []
avg_AP_halfwidth_all = []
rms_AP_halfwidth_all = []
Cm_Nspikes_all       = []
Cm_AP_halfwidth_all  = []
    
for testmodel in testmodels:
    Nspikes          = []
    Cm_Nspikes       = []
    Cm_AP_halfwidth  = []
    avg_AP_halfwidth = []
    rms_AP_halfwidth = []
    
    # Set names
    infolder      = 'Allen_test_changecapacitance/figures/%i/' % (testmodel)
    currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
    infolder = infolder+currentfolder
    infilename_Nspikes = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Nspikes_vs_Cmall.txt'
    infilename_APdhw   = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmall.txt' % str(spikedurat)
    # Read files
    infile_Nspikes = open(infilename_Nspikes,'r')
    infile_APdhw   = open(infilename_APdhw,'r')
    
    lines_Nspikes = infile_Nspikes.readlines()
    lines_APdhw   = infile_APdhw.readlines()
    Nlines = len(lines_Nspikes) # All data types have the same length
    
    for i in range(Nlines):
        words_Nspikes = lines_Nspikes[i].split()
        words_APdhw   = lines_APdhw[i].split()
        if len(words_Nspikes)>0:
            Cm_Nspikes.append(float(words_Nspikes[0]))
            Nspikes.append(float(words_Nspikes[1]))
        if len(words_APdhw)>0:
            Cm_AP_halfwidth.append(float(words_APdhw[0]))
            avg_AP_halfwidth.append(float(words_APdhw[1]))
            rms_AP_halfwidth.append(float(words_APdhw[2]))
    
    infile_Nspikes.close()
    infile_APdhw.close()
    
    Nspikes_all.append(Nspikes)
    avg_AP_halfwidth_all.append(avg_AP_halfwidth)
    rms_AP_halfwidth_all.append(rms_AP_halfwidth)
    Cm_Nspikes_all.append(Cm_Nspikes)
    Cm_AP_halfwidth_all.append(Cm_AP_halfwidth)

Nspikes     = np.zeros(NCms)
Nspikes_rms = np.zeros(NCms)
avg_AP_halfwidth = np.zeros(NCms)
rms_AP_halfwidth = np.zeros(NCms)

Nspikes_bucket   = np.zeros((NCms,Nmodels))

Nspikes_collections = []
avg_AP_halfwidth_collections = []
rms_AP_halfwidth_collections = []

fcounter    = np.zeros(NCms)
hwcounter   = np.zeros(NCms)

for i in range(Nmodels):
    Nspikes_this = Nspikes_all[i]
    avg_AP_halfwidth_this = avg_AP_halfwidth_all[i]
    rms_AP_halfwidth_this = rms_AP_halfwidth_all[i]
    Cm_Nspikes_this       = Cm_Nspikes_all[i]
    Cm_AP_halfwidth_this  = Cm_AP_halfwidth_all[i]
    Nspikes_collections = []
    avg_AP_halfwidth_collections = []
    rms_AP_halfwidth_collections = []
    for j in range(NCms):
        for k in range(len(Cm_Nspikes_this)):
            if Cm_Nspikes_this[k]==cm_master[j]:
                Nspikes[j] += Nspikes_this[k]
                Nspikes_bucket[j,i] = Nspikes_this[k]
                fcounter[j]+=1 
                continue
    for j in range(NCms):
        for k in range(len(Cm_AP_halfwidth_this)):
            if Cm_AP_halfwidth_this[k]==cm_master[j]:
                avg_AP_halfwidth[j] += avg_AP_halfwidth_this[k]
                rms_AP_halfwidth[j] += rms_AP_halfwidth_this[k]**2 # Square now, square root at the end
                hwcounter[j]+=1 
                continue

# Average and finish rms
for j in range(NCms):
    if fcounter[j]!=0:
        Nspikes[j] /= fcounter[j]
        for i in range(int(fcounter[j])):
            Nspikes_rms[j]+=(Nspikes[j]-Nspikes_bucket[j,i])**2
        Nspikes_rms[j] = np.sqrt(Nspikes_rms[j]/(fcounter[j]-1))
for j in range(NCms):
    if hwcounter[j]!=0:
        avg_AP_halfwidth[j] /= hwcounter[j]
        rms_AP_halfwidth[j]  = np.sqrt(rms_AP_halfwidth[j]/(hwcounter[j]-1))

# Plotting

cm_short = []
Nspikes_short = []
for k in range(Nmodels):
    cm_short_this = []
    Nspikes_short_this = []
    for i in range(NCms): 
        if Nspikes_bucket[i,k]!=0:
            cm_short_this.append(cm_master[i])
            Nspikes_short_this.append(Nspikes_bucket[i,k])
        else:
            break
    cm_short.append(cm_short_this)
    Nspikes_short.append(Nspikes_short_this)
    
ax4.set_ylabel('$f$ (Hz)',fontsize=14)
ax4.set_xlabel('$c_\mathregular{m}/c_\mathregular{m0}$',fontsize=14)
ax6.set_xlabel('$c_\mathregular{m}/c_\mathregular{m0}$',fontsize=14)

ax6.set_title(r'Spike duration at %s mV, I = %.1f nA' % (str(spikedurat),iamp),fontsize=15)
ax6.set_ylabel('Spike duration at %s mV (ms)' % str(spikedurat),fontsize=14)


## Saving arrays for next figure:
all_cm_short             = cm_short
all_Nspikes_short        = Nspikes_short
all_Cm_AP_halfwidth_all  = Cm_AP_halfwidth_all
all_avg_AP_halfwidth_all = avg_AP_halfwidth_all
all_rms_AP_halfwidth_all = rms_AP_halfwidth_all

############################################### SOMAPROX #######################################################
Nspikes_all          = []
avg_AP_halfwidth_all = []
rms_AP_halfwidth_all = []
Cm_Nspikes_all       = []
Cm_AP_halfwidth_all  = []
    
for testmodel in testmodels:
    Nspikes          = []
    Cm_Nspikes       = []
    Cm_AP_ampl       = []
    Cm_AP_mins       = []
    Cm_AP_halfwidth  = []
    avg_AP_halfwidth = []
    rms_AP_halfwidth = []
    
    # Set names
    infolder      = 'Allen_test_changecapacitance/figures/%i/' % (testmodel)
    currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
    infolder = infolder+currentfolder
    infilename_Nspikes = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Nspikes_vs_Cmsprx.txt'
    infilename_APdhw   = infolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmsprx.txt' % str(spikedurat)
    # Read files
    infile_Nspikes = open(infilename_Nspikes,'r')
    infile_APdhw   = open(infilename_APdhw,'r')
    
    lines_Nspikes = infile_Nspikes.readlines()
    lines_APdhw   = infile_APdhw.readlines()
    Nlines = len(lines_Nspikes) # All data types have the same length
    
    for i in range(Nlines):
        words_Nspikes = lines_Nspikes[i].split()
        words_APdhw   = lines_APdhw[i].split()
        if len(words_Nspikes)>0:
            Cm_Nspikes.append(float(words_Nspikes[0]))
            Nspikes.append(float(words_Nspikes[1]))
        if len(words_APdhw)>0:
            Cm_AP_halfwidth.append(float(words_APdhw[0]))
            avg_AP_halfwidth.append(float(words_APdhw[1]))
            rms_AP_halfwidth.append(float(words_APdhw[2]))
    
    infile_Nspikes.close()
    infile_APdhw.close()
    
    Nspikes_all.append(Nspikes)
    avg_AP_halfwidth_all.append(avg_AP_halfwidth)
    rms_AP_halfwidth_all.append(rms_AP_halfwidth)
    Cm_Nspikes_all.append(Cm_Nspikes)
    Cm_AP_halfwidth_all.append(Cm_AP_halfwidth)

Nspikes     = np.zeros(NCms)
Nspikes_rms = np.zeros(NCms)
avg_AP_halfwidth = np.zeros(NCms)
rms_AP_halfwidth = np.zeros(NCms)

Nspikes_bucket   = np.zeros((NCms,Nmodels))

Nspikes_collections = []
avg_AP_halfwidth_collections = []
rms_AP_halfwidth_collections = []

fcounter    = np.zeros(NCms)
hwcounter   = np.zeros(NCms)

for i in range(Nmodels):
    Nspikes_this = Nspikes_all[i]
    avg_AP_halfwidth_this = avg_AP_halfwidth_all[i]
    rms_AP_halfwidth_this = rms_AP_halfwidth_all[i]
    Cm_Nspikes_this       = Cm_Nspikes_all[i]
    Cm_AP_halfwidth_this  = Cm_AP_halfwidth_all[i]
    Nspikes_collections = []
    avg_AP_halfwidth_collections = []
    rms_AP_halfwidth_collections = []
    for j in range(NCms):
        for k in range(len(Cm_Nspikes_this)):
            if Cm_Nspikes_this[k]==cm_master[j]:
                Nspikes[j] += Nspikes_this[k]
                Nspikes_bucket[j,i] = Nspikes_this[k]
                fcounter[j]+=1 
                continue
    for j in range(NCms):
        for k in range(len(Cm_AP_halfwidth_this)):
            if Cm_AP_halfwidth_this[k]==cm_master[j]:
                avg_AP_halfwidth[j] += avg_AP_halfwidth_this[k]
                rms_AP_halfwidth[j] += rms_AP_halfwidth_this[k]**2 # Square now, square root at the end
                hwcounter[j]+=1 
                continue


# Average and finish rms
for j in range(NCms):
    if fcounter[j]!=0:
        Nspikes[j] /= fcounter[j]
        for i in range(int(fcounter[j])):
            Nspikes_rms[j]+=(Nspikes[j]-Nspikes_bucket[j,i])**2
        Nspikes_rms[j] = np.sqrt(Nspikes_rms[j]/(fcounter[j]-1))
for j in range(NCms):
    if hwcounter[j]!=0:
        avg_AP_halfwidth[j] /= hwcounter[j]
        rms_AP_halfwidth[j]  = np.sqrt(rms_AP_halfwidth[j]/(hwcounter[j]-1))

cm_short = []
Nspikes_short = []
for k in range(Nmodels):
    cm_short_this = []
    Nspikes_short_this = []
    for i in range(NCms): 
        if Nspikes_bucket[i,k]!=0:
            cm_short_this.append(cm_master[i])
            Nspikes_short_this.append(Nspikes_bucket[i,k])
        else:
            break
    cm_short.append(cm_short_this)
    Nspikes_short.append(Nspikes_short_this)

ax4.set_title(r'Frequency $f$, I = %.1f nA' % iamp,fontsize=15)
for i in range(Nmodels):
    ax4.plot(all_cm_short[i], all_Nspikes_short[i],label='A%i all' % (i+1),color=plotcolors[i+2], linewidth=2)
    ax4.plot(cm_short[i], Nspikes_short[i],ls='--',label='A%i sprx' % (i+1),color=plotcolors[i+2], linewidth=2)
ax4.set_ylabel('$f$ (Hz)',fontsize=14)
ax4.legend(loc='upper right')

ax6.set_title(r'Spike duration at %s mV, I = %.1f nA' % (str(spikedurat),iamp),fontsize=15)
for i in range(Nmodels):
    ax6.errorbar(all_Cm_AP_halfwidth_all[i], all_avg_AP_halfwidth_all[i], yerr=all_rms_AP_halfwidth_all[i],color=plotcolors[i+2], capsize=2,label='A%i all' % (i+1), linewidth=2)
    ax6.errorbar(Cm_AP_halfwidth_all[i], avg_AP_halfwidth_all[i], yerr=rms_AP_halfwidth_all[i],color=plotcolors[i+2], capsize=2,ls='--',label='A%i sprx' % (i+1), linewidth=2)
ax6.set_ylabel('Spike duration (ms)',fontsize=14)
ax6.legend(loc='lower right')


plt.savefig(plotname_all)

plt.show()
    
