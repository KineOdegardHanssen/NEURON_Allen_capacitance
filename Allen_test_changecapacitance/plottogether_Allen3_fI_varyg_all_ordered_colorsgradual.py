import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

plt.rcParams.update({'font.family':'Arial'})

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)
plt.rc('legend', fontsize=12)

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

testmodels = [478513407]
idur       = 2000  ms
idelay     = 100
v_init     = -86.5 # mV
Ra         = 150
somasize   = 10 
dendlen    = 1000
denddiam   = 1
nsegments  = 200 
Nmodels    = len(testmodels)
spikedurat = -40
cms        = [1.0]

namestringfirst = ''
varyg = [0.1,0.3,0.5,1.0,3.0,7.0,10.0]
namestringfirstIh = namestringfirst + '_gIh'
plotlabelgIh = r'$\bar{g}_{\mathregular{Ih}}$'
namestringfirstKd = namestringfirst + '_gKd'
plotlabelgKd = r'$\bar{g}_{\mathregular{Kd}}$'
namestringfirstHVA = namestringfirst + '_gCaHVA'
plotlabelgHVA = r'$\bar{g}_{\mathregular{CaHVA}}$'
namestringfirstNaV = namestringfirst + '_gNaV'
plotlabelgNaV = r'$\bar{g}_{\mathregular{NaV}}$'
namestringfirstKv2like = namestringfirst + '_gKv2like'
plotlabelgKv2like = r'$\bar{g}_{\mathregular{Kv2like}}$'
namestringfirstKv31 = namestringfirst + '_gKv31'
plotlabelgKv31 = r'$\bar{g}_{\mathregular{Kv3}}$'
namestringfirstKT = namestringfirst + '_gKT'
plotlabelgKT = r'$\bar{g}_{\mathregular{KT}}$'
namestringfirstImv2 = namestringfirst + '_gImv2'
plotlabelgImv2 = r'$\bar{g}_{\mathregular{Imv2}}$'
namestringfirstSK = namestringfirst + '_gSK'
plotlabelgSK = r'$\bar{g}_{\mathregular{SK}}$'
namestringfirstCaLVA = namestringfirst + '_gCaLVA'
plotlabelgCaLVA = r'$\bar{g}_{\mathregular{CaLVA}}$'
namestringfirstpas = namestringfirst + '_gpas'
plotlabelgpas = r'$\bar{g}_{\mathregular{pas}}$'

plotstringIh      = '_vary_Ih'
plotstringKd      = '_vary_Kd'
plotstringHVA     = '_vary_CaHVA'
plotstringNaV     = '_vary_NaV'
plotstringKv2like = '_vary_Kv2like'
plotstringKv31    = '_vary_Kv31'
plotstringKT      = '_vary_KT'
plotstringImv2    = '_vary_Imv2'
plotstringSK      = '_vary_SK'
plotstringCaLVA   = '_vary_CaLVA'
plotstringpas     = '_vary_pas'

i_master = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]
    
NI  = len(i_master)
Ng  = len(varyg)

gHVA_legends = []
i_master_everywhere_all_gHVA   = []
Nspikes_everywhere_all_gHVA    = []
I_Nspikes_everywhere_all_gHVA  = []

for testmodel in testmodels:
    i_master_everywhere_gHVA   = []
    Nspikes_everywhere_gHVA    = []
    I_Nspikes_everywhere_gHVA  = []
    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varyg:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringHVA = namestringfirstHVA+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringHVA,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gHVA.append(Nspikes)
                I_Nspikes_everywhere_gHVA.append(I_Nspikes)
                print('-------------------------------------')
                gHVA_legends.append([cm,g])
    Nspikes_everywhere_all_gHVA.append(Nspikes_everywhere_gHVA) 
    I_Nspikes_everywhere_all_gHVA.append(I_Nspikes_everywhere_gHVA)

# Plotting

colors = []
for i in range(Ng):
    colors.append((1.0-i/float(Ng),0,i/float(Ng),1.0-abs(0.5-i/float(Ng))))

plotfolder = 'figures/Comparemodels/'
plotname = plotfolder+'fI_varyg_AllenPV3_all_ordered_colorsgradual_SF3.png'

## avg and rms:
fig = plt.figure(figsize=(18,18),dpi=300)

gs = gridspec.GridSpec(4, 6)

ax1 = plt.subplot(gs[0, 0:2])
ax2 = plt.subplot(gs[0, 2:4])
ax3 = plt.subplot(gs[0, 4:6])
ax4 = plt.subplot(gs[1, 0:2])
ax5 = plt.subplot(gs[1, 2:4])
ax6 = plt.subplot(gs[1, 4:6])
ax7 = plt.subplot(gs[2, 0:2])
ax8 = plt.subplot(gs[2, 2:4])
ax9 = plt.subplot(gs[2, 4:6])
ax10 = plt.subplot(gs[3, 1:3])
ax11 = plt.subplot(gs[3, 3:5])

fig.suptitle(r'Frequency $f$ vs $I$, Allen model 3',fontsize=20)

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

ax1.set_title(r'Varying $\bar{g}_{\mathregular{CaHVA}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gHVA[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gHVA[0]
for j in range(Ng):
    theselegends_cahva = gHVA_legends[j]
    if theselegends_cahva[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax1.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_cahva[1]), linewidth=thelinewidth)
ax1.set_xlabel('$I$ (nA)',fontsize=14)
ax1.set_ylabel('$f$ (Hz)',fontsize=14)
ax1.legend(loc='upper left',ncol=1)

########################### NaV ####################################################
varygNaV = [0.8,1.0,3.0,7.0,10.0]
NgNaV = len(varygNaV)
navcolors = []
for i in range(NgNaV):
    navcolors.append((1.0-i/float(NgNaV),0,i/float(NgNaV),1.0-abs(0.5-i/float(NgNaV))))
# OR:
navcolors = colors[2:]


i_master_everywhere_all_gNaV   = []
Nspikes_everywhere_all_gNaV    = []
I_Nspikes_everywhere_all_gNaV  = []

gNaV_legends = []
for testmodel in testmodels:
    i_master_everywhere_gNaV   = []
    Nspikes_everywhere_gNaV    = []
    I_Nspikes_everywhere_gNaV  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varygNaV:
            print('g:',g)
            if cm!=1.0:
                print('cm!=1.0:',cm,'CONTINUE')
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringNaV = namestringfirstNaV+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringNaV,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gNaV.append(Nspikes)
                I_Nspikes_everywhere_gNaV.append(I_Nspikes)
                gNaV_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gNaV.append(Nspikes_everywhere_gNaV)
    I_Nspikes_everywhere_all_gNaV.append(I_Nspikes_everywhere_gNaV)
    

# Plotting
ax3.set_title(r'Varying $\bar{g}_{\mathregular{NaV}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gNaV[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gNaV[0]
for j in range(NgNaV):
    theselegends_nav = gNaV_legends[j]
    if theselegends_nav[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    print('Nspikes_everywhere_this[j]:',Nspikes_everywhere_this[j])
    print('gNaV_legends[j]:',gNaV_legends[j])
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax3.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=navcolors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_nav[1]), linewidth=thelinewidth)
ax3.set_xlabel('$I$ (nA)',fontsize=14)
ax3.set_ylabel('$f$ (Hz)',fontsize=14)
ax3.legend(loc='upper left',ncol=1)

########################### Ih ####################################################

i_master_everywhere_all_gIh   = []
Nspikes_everywhere_all_gIh    = []
I_Nspikes_everywhere_all_gIh  = []

gIh_legends = []
for testmodel in testmodels:
    i_master_everywhere_gIh   = []
    Nspikes_everywhere_gIh    = []
    I_Nspikes_everywhere_gIh  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varyg:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringIh = namestringfirstIh+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringIh,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gIh.append(Nspikes)
                I_Nspikes_everywhere_gIh.append(I_Nspikes)
                
                gIh_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gIh.append(Nspikes_everywhere_gIh)
    I_Nspikes_everywhere_all_gIh.append(I_Nspikes_everywhere_gIh)

# Plotting

ax10.set_title(r'Varying $\bar{g}_{\mathregular{h}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gIh[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gIh[0]
for j in range(Ng):
    theselegends_Ih = gIh_legends[j]
    if theselegends_Ih[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax10.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_Ih[1]), linewidth=thelinewidth)
ax10.set_xlabel('$I$ (nA)',fontsize=14)
ax10.set_ylabel('$f$ (Hz)',fontsize=14)
ax10.legend(loc='upper left',ncol=1)

########################### Kd ####################################################

i_master_everywhere_all_gKd   = []
Nspikes_everywhere_all_gKd    = []
I_Nspikes_everywhere_all_gKd  = []

gKd_legends = []
for testmodel in testmodels:
    i_master_everywhere_gKd   = []
    Nspikes_everywhere_gKd    = []
    I_Nspikes_everywhere_gKd  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varyg:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringKd = namestringfirstKd+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringKd,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gKd.append(Nspikes)
                I_Nspikes_everywhere_gKd.append(I_Nspikes)
                
                gKd_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gKd.append(Nspikes_everywhere_gKd)
    I_Nspikes_everywhere_all_gKd.append(I_Nspikes_everywhere_gKd)

# Plotting

ax7.set_title(r'Varying $\bar{g}_{\mathregular{Kd}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gKd[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gKd[0]
for j in range(Ng):
    theselegends_Kd = gKd_legends[j]
    if theselegends_Kd[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax7.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_Kd[1]), linewidth=thelinewidth)
ax7.set_xlabel('$I$ (nA)',fontsize=14)
ax7.set_ylabel('$f$ (Hz)',fontsize=14)
ax7.legend(loc='upper left',ncol=1)

########################### Kv2like ####################################################

i_master_everywhere_all_gKv2like   = []
Nspikes_everywhere_all_gKv2like    = []
I_Nspikes_everywhere_all_gKv2like  = []

gKv2like_legends = []
for testmodel in testmodels:
    i_master_everywhere_gKv2like   = []
    Nspikes_everywhere_gKv2like    = []
    I_Nspikes_everywhere_gKv2like  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varyg:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringKv2like = namestringfirstKv2like+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringKv2like,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gKv2like.append(Nspikes)
                I_Nspikes_everywhere_gKv2like.append(I_Nspikes)
                
                gKv2like_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gKv2like.append(Nspikes_everywhere_gKv2like)
    I_Nspikes_everywhere_all_gKv2like.append(I_Nspikes_everywhere_gKv2like)

# Plotting

ax5.set_title(r'Varying $\bar{g}_{\mathregular{Kv2like}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gKv2like[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gKv2like[0]
for j in range(Ng):
    theselegends_Kv2like = gKv2like_legends[j]
    if theselegends_Kv2like[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax5.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_Kv2like[1]), linewidth=thelinewidth)
ax5.set_xlabel('$I$ (nA)',fontsize=14)
ax5.set_ylabel('$f$ (Hz)',fontsize=14)
ax5.legend(loc='upper left',ncol=1)

########################### Kv31 ####################################################

gKv31  = [0.1,0.3,0.5,1.0,2.0,3.0]#,5.0]
NgKv31 = len(gKv31)
i_master_everywhere_all_gKv31   = []
Nspikes_everywhere_all_gKv31    = []
I_Nspikes_everywhere_all_gKv31  = []

gKv31_legends = []
for testmodel in testmodels:
    i_master_everywhere_gKv31   = []
    Nspikes_everywhere_gKv31    = []
    I_Nspikes_everywhere_gKv31  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in gKv31:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringKv31 = namestringfirstKv31+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringKv31,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gKv31.append(Nspikes)
                I_Nspikes_everywhere_gKv31.append(I_Nspikes)
                
                gKv31_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gKv31.append(Nspikes_everywhere_gKv31)
    I_Nspikes_everywhere_all_gKv31.append(I_Nspikes_everywhere_gKv31)

# Plotting

ax4.set_title(r'Varying $\bar{g}_{\mathregular{Kv3}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gKv31[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gKv31[0]
for j in range(NgKv31):
    theselegends_Kv31 = gKv31_legends[j]
    if theselegends_Kv31[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax4.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_Kv31[1]), linewidth=thelinewidth)
ax4.set_xlabel('$I$ (nA)',fontsize=14)
ax4.set_ylabel('$f$ (Hz)',fontsize=14)
ax4.legend(loc='upper left',ncol=1)

########################### KT ####################################################

varygKT = [0.1,0.3,0.5,1.0,2.0,3.0] # Stops firing early on

i_master_everywhere_all_gKT   = []
Nspikes_everywhere_all_gKT    = []
I_Nspikes_everywhere_all_gKT  = []

NgKT = 0
gKT_legends = []
for testmodel in testmodels:
    i_master_everywhere_gKT   = []
    Nspikes_everywhere_gKT    = []
    I_Nspikes_everywhere_gKT  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varygKT:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringKT = namestringfirstKT+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringKT,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
                # Read files
                try:
                    infile_Nspikes = open(infilename_Nspikes,'r')
                except:
                    break
                
                NgKT+=1
                lines_Nspikes = infile_Nspikes.readlines()
                Nlines_Nspikes = len(lines_Nspikes)
            
                for i in range(Nlines_Nspikes):
                    words_Nspikes = lines_Nspikes[i].split()
                    if len(words_Nspikes)>0:
                        I_Nspikes.append(float(words_Nspikes[0]))
                        Nspikes.append(float(words_Nspikes[1]))
            
                infile_Nspikes.close()
            
                Nspikes_everywhere_gKT.append(Nspikes)
                I_Nspikes_everywhere_gKT.append(I_Nspikes)
                
                gKT_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gKT.append(Nspikes_everywhere_gKT)
    I_Nspikes_everywhere_all_gKT.append(I_Nspikes_everywhere_gKT)

# Plotting

ax9.set_title(r'Varying $\bar{g}_{\mathregular{KT}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gKT[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gKT[0]
for j in range(NgKT):
    theselegends_KT = gKT_legends[j]
    if theselegends_KT[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax9.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_KT[1]), linewidth=thelinewidth)
ax9.set_xlabel('$I$ (nA)',fontsize=14)
ax9.set_ylabel('$f$ (Hz)',fontsize=14)
ax9.legend(loc='upper left',ncol=1)

########################### Imv2 ####################################################

i_master_everywhere_all_gImv2   = []
Nspikes_everywhere_all_gImv2    = []
I_Nspikes_everywhere_all_gImv2  = []

gImv2_legends = []
for testmodel in testmodels:
    i_master_everywhere_gImv2   = []
    Nspikes_everywhere_gImv2    = []
    I_Nspikes_everywhere_gImv2  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varyg:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringImv2 = namestringfirstImv2+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringImv2,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gImv2.append(Nspikes)
                I_Nspikes_everywhere_gImv2.append(I_Nspikes)
                
                gImv2_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gImv2.append(Nspikes_everywhere_gImv2)
    I_Nspikes_everywhere_all_gImv2.append(I_Nspikes_everywhere_gImv2)

# Plotting

ax8.set_title(r'Varying $\bar{g}_{\mathregular{Imv2}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gImv2[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gImv2[0]
for j in range(Ng):
    theselegends_Imv2 = gImv2_legends[j]
    if theselegends_Imv2[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax8.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_Imv2[1]), linewidth=thelinewidth)
ax8.set_xlabel('$I$ (nA)',fontsize=14)
ax8.set_ylabel('$f$ (Hz)',fontsize=14)
ax8.legend(loc='upper left',ncol=1)

########################### SK ####################################################

i_master_everywhere_all_gSK   = []
Nspikes_everywhere_all_gSK    = []
I_Nspikes_everywhere_all_gSK  = []

gSK_legends = []
for testmodel in testmodels:
    i_master_everywhere_gSK   = []
    Nspikes_everywhere_gSK    = []
    I_Nspikes_everywhere_gSK  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varyg:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringSK = namestringfirstSK+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringSK,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gSK.append(Nspikes)
                I_Nspikes_everywhere_gSK.append(I_Nspikes)
                
                gSK_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gSK.append(Nspikes_everywhere_gSK)
    I_Nspikes_everywhere_all_gSK.append(I_Nspikes_everywhere_gSK)

# Plotting

ax6.set_title(r'Varying $\bar{g}_{\mathregular{SK}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gSK[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gSK[0]
for j in range(Ng):
    theselegends_SK = gSK_legends[j]
    if theselegends_SK[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax6.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_SK[1]), linewidth=thelinewidth)
ax6.set_xlabel('$I$ (nA)',fontsize=14)
ax6.set_ylabel('$f$ (Hz)',fontsize=14)
ax6.legend(loc='upper left',ncol=1)

########################### CaLVA ####################################################

i_master_everywhere_all_gCaLVA   = []
Nspikes_everywhere_all_gCaLVA    = []
I_Nspikes_everywhere_all_gCaLVA  = []

gCaLVA_legends = []
for testmodel in testmodels:
    i_master_everywhere_gCaLVA   = []
    Nspikes_everywhere_gCaLVA    = []
    I_Nspikes_everywhere_gCaLVA  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in varyg:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringCaLVA = namestringfirstCaLVA+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringCaLVA,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gCaLVA.append(Nspikes)
                I_Nspikes_everywhere_gCaLVA.append(I_Nspikes)
                
                gCaLVA_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gCaLVA.append(Nspikes_everywhere_gCaLVA)
    I_Nspikes_everywhere_all_gCaLVA.append(I_Nspikes_everywhere_gCaLVA)

# Plotting

ax2.set_title(r'Varying $\bar{g}_{\mathregular{CaLVA}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gCaLVA[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gCaLVA[0]
for j in range(Ng):
    theselegends_CaLVA = gCaLVA_legends[j]
    if theselegends_CaLVA[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax2.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_CaLVA[1]), linewidth=thelinewidth)
ax2.set_xlabel('$I$ (nA)',fontsize=14)
ax2.set_ylabel('$f$ (Hz)',fontsize=14)
ax2.legend(loc='upper left',ncol=1)

########################### pas ####################################################

gLs = [0.1,0.3,0.5,1.0,2.0,3.0]
NgL = len(gLs)

i_master_everywhere_all_gpas   = []
Nspikes_everywhere_all_gpas    = []
I_Nspikes_everywhere_all_gpas  = []

gpas_legends = []
for testmodel in testmodels:
    i_master_everywhere_gpas   = []
    Nspikes_everywhere_gpas   = []
    I_Nspikes_everywhere_gpas  = []

    infolder      = 'figures/%i/' % (testmodel)
    vrestfolder   = infolder 
    for cm in cms:
        for g in gLs:
            if cm!=1.0:
                continue
            else:
                Nspikes   = []
                I_Nspikes = []
                
                namestringpas= namestringfirstpas+str(g)+'p'
                
                # Set names
                infilename_Nspikes = infolder+'%s_%i_cmfall'%(namestringpas,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
                print('infilename_Nspikes:',infilename_Nspikes)
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
            
                Nspikes_everywhere_gpas.append(Nspikes)
                I_Nspikes_everywhere_gpas.append(I_Nspikes)
                
                gpas_legends.append([cm,g])
    print('-------------------------------------')
    Nspikes_everywhere_all_gpas.append(Nspikes_everywhere_gpas)
    I_Nspikes_everywhere_all_gpas.append(I_Nspikes_everywhere_gpas)

# Plotting

ax11.set_title(r'Varying $\bar{g}_{\mathregular{L}}$',fontsize=16)
I_Nspikes_everywhere_this = I_Nspikes_everywhere_all_gpas[0]
Nspikes_everywhere_this   = Nspikes_everywhere_all_gpas[0]
for j in range(NgL):
    theselegends_pas = gpas_legends[j]
    if theselegends_pas[1]==1.0:
        thelinewidth = defaultwidth
    else:
        thelinewidth = mylinewidth
    if np.sum(Nspikes_everywhere_this[j])>0:
        ### Everywhere:
        ax11.plot(I_Nspikes_everywhere_this[j], Nspikes_everywhere_this[j],color=colors[j],label=r'%.1f$\bar{g}_X$' % (theselegends_pas[1]), linewidth=thelinewidth)
    else:
        print('gL=',varyg[j], 'No firing')
ax11.set_xlabel('$I$ (nA)',fontsize=14)
ax11.set_ylabel('$f$ (Hz)',fontsize=14)
ax11.legend(loc='upper left',ncol=1)

fig.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.savefig(plotname)

plt.show()
