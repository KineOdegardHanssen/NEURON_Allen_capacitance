import numpy as np
import matplotlib.pyplot as plt

dtexp = -8
smallCm = True
cms = [0.5,1.0,1.25,1.5,2]#,3.0]#[0.5,1.0,1.75,3]#[0.5,1,1.5]
idur = 2000
idelay   = 100.0
afteri   = 100.0
tstart   = -500.
tstop    = idur+afteri+idelay
v_init   = -86.5
somasize = 10 # 15 # 
dendlen  = 1000
denddiam = 2

Is      = [0.145,0.146,0.147,0.148,0.149,0.15]#[0.186,0.187]#[0.131,0.132,0.133,0.134,0.135,0.136,0.137,0.138,0.139,0.14]#[0.181,0.182,0.183,0.184,0.185,0.186,0.187,0.188,0.189]#[0.13,0.131,0.132,0.133,0.134,0.135,0.136,0.137,0.138,0.139,0.14]
models  = [478513407]#[478513407,478513437,488462965] # [478513437,488462965] # 
Nmodels = len(models)
Ncms    = len(cms)
NI      = len(Is)
thresholds = np.zeros(Ncms)

plotname  = 'figures/threshold_Allen_everywhere_models%s.png' %str(models) 
outfilename  = 'figures/threshold_Allen_everywhere_models%s.txt' %str(models) 

outfile = open(outfilename,'w')

plt.figure(figsize=(6,5))
for l in range(Ncms):
    cm = cms[l]
    Nspikes_avg = np.zeros(NI)
    Nspikes_rms = np.zeros(NI)
    for j in range(Nmodels):
        testmodel = models[j]
        for i in range(NI):
            iamp = Is[i]
            if iamp==0.0:
                iamp=0
            theseNspikes = []
            currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
            if testmodel==480633479:
                v_init = -96.8
                cm_soma = 0.704866 
                cm_dend = 0.704866 
                cm_axon = 0.704866 
            elif testmodel==496497595:
                v_init = -86.5
                cm_soma = 1.14805
                cm_dend = 9.98231
                cm_axon = 3.00603
            elif testmodel==488462965:
                v_init = -86.5
                cm_soma = 3.31732779736 
                cm_dend = 3.31732779736
                cm_axon = 3.31732779736
            elif testmodel==497230463:
                v_init = -90
                cm_soma = 1.23729
                cm_dend = 2.57923
                cm_axon = 5.02697
            elif testmodel==497233075:
                v_init = -90
                cm_soma = 1.64168
                cm_dend = 2.83035
                cm_axon = 9.98442
            elif testmodel==478513437:
                v_init = -86.8
                cm_soma = 2.34539964752
                cm_dend = 2.34539964752
                cm_axon = 2.34539964752
            elif testmodel==478513407:
                v_init = -83.7
                cm_soma = 1.0
                cm_dend = 1.0
                cm_axon = 1.0
            elif testmodel==497233271:
                v_init = -90
                cm_soma = 0.783229
                cm_dend = 1.94512
                cm_axon = 8.25387
            elif testmodel==489931686:
                v_init = -95.7
                cm_soma = 1.66244903951
                cm_dend = 1.66244903951
                cm_axon = 1.66244903951
            infilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/idur%i_iamp" % idur + str(iamp)+"_changecmf" + str(cm) + "_everywhere_vinit"+str(v_init)+"_addedRa.txt"
            
            t = []
            V = []
            
            infile = open(infilename,'r')
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
            timestart = idur/2.+idelay
            for m in range (1,len(V)-1):
                if V[m-1]<V[m] and V[m+1]<V[m] and V[m]>vthr and t[m]>timestart:
                    Npeaks+=1
            print('cm:', cm, 'iamp:' ,iamp,'Npeaks:', Npeaks)      
            if Npeaks>0:
                thresholds[l]=iamp
                outfile.write('%.2f %.5f\n' % (cm,iamp))
                break 
outfile.close()
plt.plot(cms,thresholds,'-o')
plt.xlabel(r'$C_{m,all}$ ($\mu$F/cm$^2$)')
plt.ylabel('Threshold (nA)')
plt.title(r'Threshold, PV Allen %s' % (models))
plt.tight_layout()
plt.savefig(plotname)
plt.show()
