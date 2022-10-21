import numpy as np
import matplotlib.pyplot as plt

read_off = True # False # 

dtexp = -7
varymech = 'Na' #'K'#'leak'
varyE_bool = True
varyE = 50 
varyg = 'None'
    
varylist = [] 
plotstring = '_vary'
if varyE_bool==True:
    varylist = varyE
    plotstring = plotstring + 'E'+str(varyE)
else:
    varylist = varyg
    plotstring = plotstring + 'g'+str(varyg)
      
if varymech=='Na':
    folderstring = 'VaryNa/' 
    plotstring = plotstring + '_Na'
elif varymech=='pas':
    folderstring = 'VaryLeak/'
    plotstring = plotstring + '_leak'
elif varymech=='K':
    folderstring = 'VaryK/'
    plotstring = plotstring + '_K'

dtexp = -7
idur = 1000
idelay   = 100.0
afteri   = 100.0
tstart   = -500.
tstop    = idur+afteri+idelay
v_init   = -65
Ra       = 100
somasize = 10 
dendlen  = 1000
denddiam = 1

I_all  = [[0.091,0.092,0.093,0.094,0.095,0.096,0.097,0.098,0.099,0.1],[0.101,0.102,0.103,0.104,0.105,0.106,0.107,0.108,0.109,0.11],[0.109,0.11,0.111,0.112],[0.11,0.111,0.112,0.113,0.114,0.115,0.116,0.117,0.118,0.119,0.12],[0.141,0.142,0.143,0.144,0.145,0.146,0.147,0.148,0.149]]
cm     = 1.0 
cmfacs = [0.5,1.0,1.25,1.5,2.0]
N      = len(cmfacs)

outfolder   = 'Results/IStim/Soma%i/dendlen%i/denddiam%i/' % (somasize,dendlen,denddiam) +folderstring
plotname    = outfolder + 'thresholds_bashhdpas_everywhere_varyfactor'+plotstring+'.png' 
outfilename = outfolder + 'thresholds_bashhdpas_everywhere_varyfactor'+plotstring+'.txt' 
outfile     = open(outfilename,'w')

thresholds = np.zeros(N)

for l in range(N):
    cmfac = cmfacs[l]
    changestring =''
    if varyE_bool==True:
        changestring = changestring+'_E'+str(varyE)+'_gdf'
    else:
        changestring = changestring+'_Edf_g'+str(varyg)
    Is = I_all[l]
    NI = len(Is)
    Nspikes     = np.zeros(NI)
    for i in range(NI):
        iamp = Is[i]
        print('Cm:',cmfac,'iamp:',iamp)
        if iamp==0.0:
            iamp=0
        theseNspikes = []
        currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
        infolder = 'Results/IStim/Soma%i/dendlen%i/denddiam'% (somasize,dendlen)+str(denddiam)+'/'+ folderstring
        infolder = infolder+currentfolder
        infilename = infolder+'basHHdpas_cmf'+str(cmfac)+'_idur%i_iamp'%idur+str(iamp)+'_Ra%i_vinit' %Ra+str(v_init)+changestring+'_V_all.txt' 
        try:
            infile = open(infilename,'r')
        except:
            changestring2 = '_E'+str(varyE)+'_gd'
            infilename = infolder+'basHHdpas_cmf'+str(cmfac)+'_idur%i_iamp'%idur+str(iamp)+'_Ra%i_vinit' %Ra+str(v_init)+changestring2+'_V_all.txt' 
            try:
                infile = open(infilename,'r')
            except:
                changestring3 = '_E'+str(varyE)
                infilename = infolder+'basHHdpas_cmf'+str(cmfac)+'_idur%i_iamp'%idur+str(iamp)+'_Ra%i_vinit' %Ra+str(v_init)+changestring3+'_V_all.txt' 
                infile = open(infilename,'r')
        
        t = []
        V = []
        
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
        vthr   = -20
        vprev  = vthr-40 # A peak never kicks in at initiation, even if I change vthr
        Npeaks = 0
        peaktimelast = 0
        for m in range (1,len(V)-1):
            if V[m-1]<V[m] and V[m+1]<V[m] and V[m]>vthr:
                Npeaks+=1
                peaktimelast = t[m]
        if vmax<-20:
            Npeaks = 0
        if Npeaks!=0:
            if peaktimelast<=(idur/2+idelay): # Checking if there's no firing in the last half of the stim. interval
                Npeaks=0            
        if Npeaks>0:
            thresholds[l]=iamp
            outfile.write('%.2f %.5f\n' % (cmfac,iamp))
            break 
outfile.close()

plt.figure(figsize=(6,5))
plt.plot(cmfacs,thresholds,'-o')
plt.xlabel('$C_m$ ($\mu$F/cm$^2$)')
plt.ylabel('Threshold (nA)')  
plt.title(r'Spiking threshold vs $C_m$, BAS-HH')
plt.savefig(plotname)
plt.tight_layout()
plt.show()

