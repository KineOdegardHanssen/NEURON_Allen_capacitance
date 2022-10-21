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
    vprev = vthr-40 # A peak never kicks in at initiation, even if I change vthr
    durthr = spikedurat # Height at which we measure the duration. Need to be calibrated by peaks? # Was -20
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
            if len(peakmins)>0: # Need to verify stuff
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
    Ndur = min([len(passtimes_up),len(passtimes_down)])
    for i in range(Ndur):
        dur.append(passtimes_down[i]-passtimes_up[i])
    for i in range(1,len(peaktimes)):
        isi.append(peaktimes[i]-peaktimes[i-1])
    
    ## Avg and rms:
    peakmins_avg, peakmins_rms = avg_and_rms(peakmins)
    peakvals_avg, peakvals_rms = avg_and_rms(peakvals)
    dur_avg, dur_rms = avg_and_rms(dur)
    isi_avg, isi_rms = avg_and_rms(isi)
    
    ## Checking if we've got consistent firing:
    # Checking if there's no firing in the last half of the stim. interval
    # Making sure that there is no flatlining: check for firing within 5*ISI (5 is chosen a bit at random here)
    if len(peaktimes)>0:
        if peaktimes[-1]<=(idur/2.+idelay): 
            Npeaks=0
            print('No consistent firing')
        elif peaktimes[-1]<=(idur+idelay-5*isi_avg): # This should cover the first test, but better safe than sorry
            Npeaks=0
            print('No consistent firing')
        else:
            print('The neuron is firing!')
    
    return Npeaks, peaktimes, peakmins_avg, peakmins_rms, peakvals_avg,  peakvals_rms, dur_avg, dur_rms, isi_avg, isi_rms, isi

if __name__ == '__main__':
    testmodel  = 488462965 # 478513407 # 478513437 #  
    spikedurat = -40
    idur       = 2000 # ms
    idelay     = 100
    iamp       = 0.4 # nA
    v_init     = -83.7 # mV
    Ra         = 100
    somasize   = 10
    dendlen    = 1000
    denddiam   = 1
    nsegments  = 200 
    
    varymech = 'Na' # 'K' # 'leak'
    varyE_bool = True
    varyE = 50
    varyg = 'None'
      
    if varymech=='Na':
        folderstring = 'VaryNa/' 
    elif varymech=='leak':
        folderstring = 'VaryLeak/'
    elif varymech=='K':
        folderstring = 'VaryK/'

    changestring =''
    if varyE_bool==True:
        changestring = changestring+'_E'+str(varyE)+'_gdflt'
    else:
        changestring = changestring+'_Edf_g'+str(varyg)
    
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
    
    cm = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
    
    NCms = len(cm)
    
    Nspikes = numpy.zeros(NCms)
    avg_ISI = numpy.zeros(NCms)
    rms_ISI = numpy.zeros(NCms)
    avg_AP_ampl = numpy.zeros(NCms)
    rms_AP_ampl = numpy.zeros(NCms)
    avg_AP_mins = numpy.zeros(NCms)
    rms_AP_mins = numpy.zeros(NCms)
    avg_AP_halfwidth = numpy.zeros(NCms)
    rms_AP_halfwidth = numpy.zeros(NCms)
    
    # Set names
    outfolder = 'figures/%i/current_idur%i_iamp' % (testmodel,idur) + str(iamp)+'/'
    outfilename_Nspikes = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Nspikes_vs_Cmall.txt'
    outfilename_APampl = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Vmax_vs_Cmall.txt'
    outfilename_APmins = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Vmin_vs_Cmall.txt'
    outfilename_APdhw  = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmall.txt' % str(spikedurat)
    outfilename_ISI   = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_ISI_vs_Cmall.txt'
    plotname_Nspikes  = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp)+'_manual_cmfs_Nspikes_vs_Cmall.png'
    plotname_APampl   = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_Vmax_vs_Cmall.png'
    plotname_APmins   = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_Vmin_vs_Cmall.png'
    plotname_APdhw    = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmall.png' % str(spikedurat)
    plotname_ISI      = outfolder+'%i_idur%i_iamp'% (testmodel,idur)+str(iamp) +'_manual_cmfs_ISI_vs_Cmall.png'
    # make files
    outfile_Nspikes = open(outfilename_Nspikes,'w')
    outfile_APampl  = open(outfilename_APampl,'w')
    outfile_APmins  = open(outfilename_APmins,'w')
    outfile_APdhw   = open(outfilename_APdhw,'w')
    outfile_ISI     = open(outfilename_ISI,'w')
    for j in range(NCms):
        print('Step ', j+1, ' of', NCms)
        filename = outfolder+"idur%i_iamp" % idur + str(iamp)+"_changecmf" + str(cm[j]) + "_all" + "_vinit"+str(v_init)+"_addedRa.txt"
        Nspikes[j], peaktimes, avg_AP_mins[j], rms_AP_mins[j], avg_AP_ampl[j], rms_AP_ampl[j], avg_AP_halfwidth[j], rms_AP_halfwidth[j], avg_ISI[j], rms_ISI[j], ISI = manual(filename,idelay,idur,spikedurat)  
        #print('Nspikes[j]:',Nspikes[j], 'cm[j]:',cm[j])
        #print('filename:', filename)  
        if Nspikes[j]!=0:
            outfile_Nspikes.write('%.5f %i\n' % (cm[j],Nspikes[j]))
            outfile_APampl.write('%.5f %.10f %.10f\n' % (cm[j],avg_AP_ampl[j],rms_AP_ampl[j]))
            outfile_APmins.write('%.5f %.10f %.10f\n' % (cm[j],avg_AP_mins[j],rms_AP_mins[j]))
            outfile_APdhw.write('%.5f %.10f %.10f\n' % (cm[j],avg_AP_halfwidth[j],rms_AP_halfwidth[j]))
            outfile_ISI.write('%.5f %.10f %.10f\n' % (cm[j],avg_ISI[j],rms_ISI[j]))
            # Write all ISIs:
            outfilename_ISI_all = outfolder+'basPV_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmf'+str(cm[j])+'_ISIall_vs_Cmsprx.txt'
            outfile_ISI_all = open(outfilename_ISI_all,'w')
            for k in range(len(ISI)):
                outfile_ISI_all.write('%.10f ' % ISI[k])
            outfile_ISI_all.close()
    outfile_Nspikes.close()
    outfile_APampl.close()
    outfile_APmins.close()
    outfile_APdhw.close()
    outfile_ISI.close()
    
    # Plot results
    plt.figure(figsize=(6,5))
    plt.plot(cm,Nspikes)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'$N_{spikes}$')
    plt.title(r'$C_{m,all}$ vs number of spikes, PV, $C_{m,all}$')
    plt.tight_layout()
    plt.savefig(plotname_Nspikes)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_ampl, yerr=rms_AP_ampl, capsize=2)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'Peak voltage [mV]')
    plt.title(r'$C_{m,all}$ vs peak voltage, PV, $C_{m,all}$')
    plt.tight_layout()
    plt.savefig(plotname_APampl)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_mins, yerr=rms_AP_mins, capsize=2)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'Peak voltage [mV]')
    plt.title(r'$C_{m,all}$ vs spike minimum at I=%.2f, model %i' % (iamp,testmodel))
    plt.tight_layout()
    plt.savefig(plotname_APmins)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_halfwidth, yerr=rms_AP_halfwidth, capsize=2)
    plt.xlabel(r'$C_{m} $[$\mu$ F/cm$^2$]')
    plt.ylabel(r'Spike duration at %s mV [ms] % str(spikedurat)')
    plt.title(r'$C_{m,all}$ vs spike duration at %s mV, PV, $C_{m,all}$' % str(spikedurat))
    plt.tight_layout()
    plt.savefig(plotname_APdhw)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_ISI, yerr=rms_ISI, capsize=2)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'Interspike interval [ms]')
    plt.title(r'$C_{m,all}$ vs interspike interval, PV, $C_{m,all}$')
    plt.tight_layout()
    plt.savefig(plotname_ISI)
    
    # Print results to terminal
    print('Nspikes:', Nspikes)
    print('AP amplitude, avg:', avg_AP_ampl)
    print('AP amplitude, rms:', rms_AP_ampl)
    print('AP duration at half width, avg:', avg_AP_halfwidth)
    print('AP duration at half width, rms:', rms_AP_halfwidth)
    
    print('outfilename_Nspikes:',outfilename_Nspikes)
