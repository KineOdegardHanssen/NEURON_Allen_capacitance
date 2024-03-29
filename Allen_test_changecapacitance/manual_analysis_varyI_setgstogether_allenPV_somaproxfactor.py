import numpy
import matplotlib.pyplot as plt

def avg_and_rms(x):
    N = len(x)
    avgx = numpy.mean(x)
    rmsx = 0
    for i in range(N):
        rmsx += (avgx-x[i])**2
    rmsx = numpy.sqrt(rmsx/(N-1))
    return avgx,rmsx

def manual(filename,idelay,idur,spikedurat):
    """Manual approach"""

    # Use numpy to read the trace data from the txt file
    data = numpy.loadtxt(filename)
    
    # Time is the first column
    time = data[:, 0]
    # Voltage is the second column
    voltage = data[:, 1]
    
    vmax = max(voltage) 
    vmin = min(voltage) 
    deltav = vmax-vmin
    vthr  = -20   # If there is a peak above this value, we count it 
    durthr = spikedurat # Height at which we measure the duration.
    Npeaks = 0
    peakmins = []
    peakvals = []
    peaktimes = []
    passtimes_up = []
    passvals_up  = []
    passtimes_down = []
    passvals_down  = []
    timestart = idur/2.+idelay
    extremumlast = 'minimum'
    for i in range (1,len(voltage)-1):  
        if voltage[i-1]<voltage[i] and voltage[i+1]<voltage[i] and voltage[i]>vthr and time[i]>timestart:
            if len(peakmins)>0:
                if extremumlast!='peak':
                    peaktimes.append(time[i])
                    peakvals.append(voltage[i])
                    extremumlast = 'peak'
            else:
                peaktimes.append(time[i])
                peakvals.append(voltage[i])
                extremumlast = 'peak'
            Npeaks+=1
        if voltage[i-1]>voltage[i] and voltage[i+1]>voltage[i] and voltage[i]<vthr and time[i]>timestart:
            if len(peakvals)>0:
                if extremumlast!='minimum':
                    peakmins.append(voltage[i])
                    extremumlast = 'minimum'
        if voltage[i]>=durthr and voltage[i-1]<durthr and time[i]>timestart: # Passing upwards
            tbef = time[i-1]
            taft = time[i]
            Vbef = voltage[i-1]
            Vaft = voltage[i]
            a = (Vaft-Vbef)/(taft-tbef)
            b = Vbef-a*tbef
            tint = (durthr-b)/a
            Vint = a*tint+b
            passtimes_up.append(tint)
            passvals_up.append(Vint) # For plotting
        elif voltage[i]>=durthr and voltage[i+1]<durthr and time[i]>timestart and len(passtimes_up)>0: # Passing downwards
            tbef = time[i]
            taft = time[i+1]
            Vbef = voltage[i]
            Vaft = voltage[i+1]
            a = (Vaft-Vbef)/(taft-tbef)
            b = Vbef-a*tbef
            tint = (durthr-b)/a
            Vint = a*tint+b
            passtimes_down.append(tint)
            passvals_down.append(Vint) # For plotting
        if time[i]>idur+idelay:
            break
    
    dur = []
    isi = []
    amps = []
    Namps = min([len(peakmins),len(peakvals)])
    Ndur = min([len(passtimes_up),len(passtimes_down)])
    for i in range(Ndur):
        dur.append(passtimes_down[i]-passtimes_up[i])
    for i in range(Namps):
        amps.append(peakvals[i]-peakmins[i])
    for i in range(1,len(peaktimes)):
        isi.append(peaktimes[i]-peaktimes[i-1])
    
    ## Avg and rms:
    peakmins_avg, peakmins_rms = avg_and_rms(peakmins)
    peakvals_avg, peakvals_rms = avg_and_rms(peakvals)
    amps_avg, amps_rms = avg_and_rms(amps)
    dur_avg, dur_rms = avg_and_rms(dur)
    isi_avg, isi_rms = avg_and_rms(isi)
    
    ## Checking if we've got consistent firing.
    # Goals:
    # Checking if there's no firing in the last half of the stim. interval
    # Making sure that there is no flatlining: check for firing within 5*ISI 
    if len(peaktimes)>0:
        if peaktimes[-1]<=(idur/2.+idelay): 
            Npeaks=0
            print('No consistent firing')
        if peaktimes[-1]<=(idur+idelay-5*isi_avg):
            Npeaks=0
            print('No consistent firing')
        else:
            print('The neuron is firing!')
    
    return Npeaks, peaktimes, peakmins_avg, peakmins_rms, peakvals_avg,  peakvals_rms, dur_avg, dur_rms, isi_avg, isi_rms, isi, dur, amps_avg, amps_rms

if __name__ == '__main__':
    testmodel  = 478513437 # 488462965 # 478513407 # 
    spikedurat = -40
    idur       = 2000 # ms
    idelay     = 100
    v_init     = -83.7 # mV
    Ra         = 100
    somasize   = 10
    dendlen    = 1000
    denddiam   = 1
    nsegments  = 200 
    
    varymech     = 'Na' # 'None' # 'pas' # 'K' # 
    varyE_bool   = True # False # 
    varygbool    = True
    varyIh       = False
    vary_NaV     = False
    vary_Kd      = False
    vary_Kv2like = True # False 
    vary_Kv3_1   = False
    vary_K_T     = False
    vary_Im_v2   = False
    vary_SK      = True # False
    vary_Ca_HVA  = False 
    vary_Ca_LVA  = False
    vary_gpas    = False 

    cms    = [1.5] # [1.0,1.5]
    varygs = [1.5] # [1.0,1.5]
    varyENas  = [63]
    varyEKs   = [-107]
    varyEpases = [0]
    
    if testmodel==496497595:
        cm_soma = 1.14805
        cm_dend = 9.98231
        cm_axon = 3.00603
    elif testmodel==497233271:
        cm_soma = 0.783229
        cm_dend = 1.94512
        cm_axon = 8.25387
    elif testmodel==497230463:
        cm_soma = 1.23729
        cm_dend = 2.57923
        cm_axon = 5.02697
    elif testmodel==497233075:
        cm_soma = 1.64168
        cm_dend = 2.83035
        cm_axon = 9.98442
    elif testmodel==488462965:
        cm_soma = 3.31732779736
        cm_dend = 3.31732779736
        cm_axon = 3.31732779736
    elif testmodel==478513407:
        cm_soma = 1.0
        cm_dend = 1.0
        cm_axon = 1.0
    elif testmodel==480633479:
        cm_soma = 0.704866
        cm_dend = 0.704866
        cm_axon = 0.704866
    elif testmodel==478513437:
        cm_soma = 2.34539964752
        cm_dend = 2.34539964752
        cm_axon = 2.34539964752
    elif testmodel==489931686:
        cm_soma = 1.66244903951
        cm_dend = 1.66244903951
        cm_axon = 1.66244903951
    elif testmodel==485694403:
        cm_soma = 0.763348896
        cm_dend = 0.763348896
        cm_axon = 0.763348896
    
    if testmodel==480633479:
        v_init = -96.8
    elif testmodel==496497595:
        v_init = -86.5
    elif testmodel==488462965:
        v_init = -86.5
    elif testmodel==497230463:
        v_init = -90
    elif testmodel==497233075:
        v_init = -90
    elif testmodel==478513437:
        v_init = -86.8
    elif testmodel==478513407:
        v_init = -83.7
    elif testmodel==497233271:
        v_init = -90
    elif testmodel==489931686:
        v_init = -95.7
    elif testmodel==485694403:
        v_init = -88.8
    ###########################################################
    
    if testmodel==478513437:
        iamps = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8]
    elif testmodel==478513407:
        iamps = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]
    elif testmodel==488462965:
        iamps = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7]
    
    NI   = len(iamps)
    
    Nspikes = numpy.zeros(NI)
    avg_ISI = numpy.zeros(NI)
    rms_ISI = numpy.zeros(NI)
    avg_AP_ampl = numpy.zeros(NI)
    rms_AP_ampl = numpy.zeros(NI)
    avg_AP_mins = numpy.zeros(NI)
    rms_AP_mins = numpy.zeros(NI)
    avg_AP_halfwidth = numpy.zeros(NI)
    rms_AP_halfwidth = numpy.zeros(NI)
    avg_AP_amplitudes = numpy.zeros(NI)
    rms_AP_amplitudes = numpy.zeros(NI)
    
    # Set names
    outfolder = 'figures/%i/' % testmodel
    for k in range(len(varygs)):
        cm       = cms[k]
        changedg = varygs[k]
        varyENa  = varyENas[k] 
        varyEK   = varyEKs[k] 
        varyEpas = varyEpases[k] 
        namestring = ''
        if varymech=='Na':
            namestring = namestring + 'ENa'+str(varyENa)
        if varymech=='K':
            namestring = namestring + 'EK'+str(varyEK)
        if varymech=='pas':
            namestring = namestring + 'Epasshift'+str(varyEpas)
        if varyIh==True:
            namestring = namestring + '_gIh'+str(changedg)+'p'
        if vary_NaV==True:
            namestring = namestring + '_gNaV'+str(changedg)+'p'
        if vary_Kd==True:
            namestring = namestring + '_gKd'+str(changedg)+'p'
        if vary_Kv2like==True:
            namestring = namestring + '_gKv2like'+str(changedg)+'p'
        if vary_Kv3_1==True:
            namestring = namestring + '_gKv31'+str(changedg)+'p'
        if vary_K_T==True:
            namestring = namestring + '_gKT'+str(changedg)+'p'
        if vary_Im_v2==True:
            namestring = namestring + '_gImv2'+str(changedg)+'p'
        if vary_SK==True:
            namestring = namestring + '_gSK'+str(changedg)+'p'
        if vary_Ca_HVA==True:
            namestring = namestring + '_gCaHVA'+str(changedg)+'p'
        if vary_Ca_LVA==True:
            namestring = namestring + '_gCaLVA'+str(changedg)+'p'
        if vary_gpas==True: 
            namestring = namestring + '_gpas'+str(changedg)+'p'
        outfilename_Nspikes = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.txt'
        outfilename_APampl  = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Vmax_vs_I.txt'
        outfilename_APmins  = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Vmin_vs_I.txt'
        outfilename_APdhw   = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_sdurat%s_vs_I.txt' % str(spikedurat)
        outfilename_amps    = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Ampl_vs_I.txt'
        outfilename_ISI     = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+'_idur%i_varyiamp'% idur+'_manual_ISI_vs_I.txt'
        plotname_Nspikes    = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Nspikes_vs_I.png'
        plotname_APampl     = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Vmax_vs_I.png'
        plotname_APmins     = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_Vmin_vs_I.png'
        plotname_APdhw      = outfolder+'%s_%i_cmfsprx'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_sdurat%s_vs_I.png' % str(spikedurat)
        plotname_ISI        = outfolder+'%s_%i_cmfall'%(namestring,testmodel)+str(cm)+'_idur%i_varyiamp'% idur+'_manual_ISI_vs_I.png'
        # make files
        outfile_Nspikes = open(outfilename_Nspikes,'w')
        outfile_APampl  = open(outfilename_APampl,'w')
        outfile_APmins  = open(outfilename_APmins,'w')
        outfile_APdhw   = open(outfilename_APdhw,'w')
        outfile_amps    = open(outfilename_amps,'w')
        outfile_ISI     = open(outfilename_ISI,'w')
        thr_reached=False
        for j in range(NI):
            iamp = iamps[j]
            infolder = 'figures/%i/current_idur%i_iamp' % (testmodel,idur) + str(iamp)+'/'
            print('Step ', j+1, ' of', NI)
            filename = infolder+namestring+"_changecmf" + str(cm) + "_cmdend" + str(cm_dend) + "_cmaxon"+ str(cm_axon)+"_vinit"+str(v_init)+"_addedRa.txt"
            try:
                Nspikes[j], peaktimes, avg_AP_mins[j], rms_AP_mins[j], avg_AP_ampl[j], rms_AP_ampl[j], avg_AP_halfwidth[j], rms_AP_halfwidth[j], avg_ISI[j], rms_ISI[j], ISI, dur, avg_AP_amplitudes[j], rms_AP_amplitudes[j] = manual(filename,idelay,idur,spikedurat) 
            except:
                filename = infolder+namestring+"_changecmf" + str(cm) + "_somaprox"+"_vinit"+str(v_init)+"_addedRa.txt"
                Nspikes[j], peaktimes, avg_AP_mins[j], rms_AP_mins[j], avg_AP_ampl[j], rms_AP_ampl[j], avg_AP_halfwidth[j], rms_AP_halfwidth[j], avg_ISI[j], rms_ISI[j], ISI, dur, avg_AP_amplitudes[j], rms_AP_amplitudes[j] = manual(filename,idelay,idur,spikedurat) 
            if Nspikes[j]!=0:
                thr_reached=True
                outfile_APampl.write('%.5f %.10f %.10f\n' % (iamp,avg_AP_ampl[j],rms_AP_ampl[j]))
                outfile_APmins.write('%.5f %.10f %.10f\n' % (iamp,avg_AP_mins[j],rms_AP_mins[j]))
                outfile_APdhw.write('%.5f %.10f %.10f\n' % (iamp,avg_AP_halfwidth[j],rms_AP_halfwidth[j]))
                outfile_amps.write('%.5f %.10f %.10f\n' % (iamp,avg_AP_amplitudes[j],rms_AP_amplitudes[j]))
                outfile_ISI.write('%.5f %.10f %.10f\n' % (iamp,avg_ISI[j],rms_ISI[j]))
            if thr_reached==False or Nspikes[j]!=0:
                outfile_Nspikes.write('%.5f %i\n' % (iamp,Nspikes[j]))
        outfile_Nspikes.close()
        outfile_APampl.close()
        outfile_APmins.close()
        outfile_APdhw.close()
        outfile_ISI.close()
        
        # Plot results
        plt.figure(figsize=(6,5))
        plt.plot(iamps,Nspikes)
        plt.xlabel(r'I$ [nA]')
        plt.ylabel(r'$N_{spikes}$')
        plt.title(r'$I$ vs number of spikes, PV, $C_{m,all}$')
        plt.tight_layout()
        plt.savefig(plotname_Nspikes)
        
        plt.figure(figsize=(6,5))
        plt.errorbar(iamps,avg_AP_ampl, yerr=rms_AP_ampl, capsize=2)
        plt.xlabel(r'I$ [nA]')
        plt.ylabel(r'Peak voltage [mV]')
        plt.title(r'$I$ vs peak voltage, PV, $C_{m,all}$')
        plt.tight_layout()
        plt.savefig(plotname_APampl)
        
        plt.figure(figsize=(6,5))
        plt.errorbar(iamps,avg_AP_mins, yerr=rms_AP_mins, capsize=2)
        plt.xlabel(r'I$ [nA]')
        plt.ylabel(r'Peak voltage [mV]')
        plt.title(r'$I$ vs spike minimum at I=%.2f, model %i' % (iamp,testmodel))
        plt.tight_layout()
        plt.savefig(plotname_APmins)
        
        plt.figure(figsize=(6,5))
        plt.errorbar(iamps,avg_AP_halfwidth, yerr=rms_AP_halfwidth, capsize=2)
        plt.xlabel(r'I$ [nA]')
        plt.ylabel(r'Spike duration at %s mV [ms] % str(spikedurat)')
        plt.title(r'$I$ vs spike duration at %s mV, PV, $C_{m,all}$' % str(spikedurat))
        plt.tight_layout()
        plt.savefig(plotname_APdhw)
        
        plt.figure(figsize=(6,5))
        plt.errorbar(iamps,avg_ISI, yerr=rms_ISI, capsize=2)
        plt.xlabel(r'I$ [nA]')
        plt.ylabel(r'Interspike interval [ms]')
        plt.title(r'$I$ vs interspike interval, PV, $C_{m,all}$')
        plt.tight_layout()
        plt.savefig(plotname_ISI)
        
        
        # Print results to terminal
        print('Nspikes:', Nspikes)
        print('AP amplitude, avg:', avg_AP_ampl)
        print('AP amplitude, rms:', rms_AP_ampl)
        print('AP duration at half width, avg:', avg_AP_halfwidth)
        print('AP duration at half width, rms:', rms_AP_halfwidth)
