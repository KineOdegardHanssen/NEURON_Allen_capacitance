"""Modified from 'Basic example 1 for eFEL'."""

import efel
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
    durthr = spikedurat # Height at which we measure the duration. 
    Npeaks = 0
    peakmins  = []
    peakvals  = []
    peaktimes = []
    passtimes_up = []
    passvals_up  = []
    passtimes_down = []
    passvals_down  = []
    for i in range (1,len(voltage)-1):  
        if voltage[i-1]<voltage[i] and voltage[i+1]<voltage[i] and voltage[i]>vthr:
            peaktimes.append(time[i])
            peakvals.append(voltage[i])
            Npeaks+=1
        if voltage[i-1]>voltage[i] and voltage[i+1]>voltage[i] and voltage[i]<vthr:
            peakmins.append(voltage[i])
        if voltage[i]>=durthr and voltage[i-1]<durthr: # Passing upwards
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
        elif voltage[i]>=durthr and voltage[i+1]<durthr and len(passtimes_up)>0: # Passing downwards
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
    # Find resting potential:
    k = 0
    
    print('Nspikes before testing:',Npeaks)
    # Checking if we've got consistent firing:
    if Npeaks!=0:
        if peaktimes[-1]<=(idur/2+idelay): # Checking if there's no firing in the last half of the stim. interval
            Npeaks=0                       
    if Npeaks==0:
        passtimes_up   = []
        passtimes_down = []
    
    dur = []
    isi = []
    Ndur = min([len(passtimes_up),len(passtimes_down)])
    for i in range(10,Ndur-1):
        dur.append(passtimes_down[i]-passtimes_up[i])
    for i in range(1,len(peaktimes)):
        thisisi = peaktimes[i]-peaktimes[i-1]
        isi.append(thisisi)
    isi      = isi[9:-1]
    peakvals = peakvals[9:-1]
    peakmins = peakmins[9:-1]
    
    ## Avg and rms:
    peakmins_avg, peakmins_rms = avg_and_rms(peakmins)
    peakvals_avg, peakvals_rms = avg_and_rms(peakvals)
    dur_avg, dur_rms = avg_and_rms(dur)
    isi_avg, isi_rms = avg_and_rms(isi)
    
    return Npeaks, peaktimes, peakmins_avg, peakmins_rms, peakvals_avg,  peakvals_rms, dur_avg, dur_rms, isi_avg, isi_rms, isi

if __name__ == '__main__':
    spikedurat = -40
    idur       = 1000 # ms
    idelay     = 100
    iamp       = 0.4 # nA
    v_init     = -65 # mV
    Ra         = 100
    somasize   = 10 
    dendlen    = 1000
    denddiam   = 1
    nsegments  = 200 
    
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
    outfolder = 'Results/IStim/Soma%i/dendlen%i/denddiam'% (somasize,dendlen)+str(denddiam)+'/'
    currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
    outfolder = outfolder+currentfolder
    outfilename_Nspikes = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cmall.txt'
    outfilename_APampl  = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmax_vs_Cmall.txt'
    outfilename_APmins  = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmin_vs_Cmall.txt'
    outfilename_APdhw   = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmall.txt' % str(spikedurat)
    outfilename_ISI     = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_ISI_vs_Cmall.txt'
    plotname_Nspikes    = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cmall.png'
    plotname_APampl     = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmax_vs_Cmall.png'
    plotname_APmins     = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmin_vs_Cmall.png'
    plotname_APdhw      = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cmall.png' % str(spikedurat)
    plotname_ISI        = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_ISI_vs_Cmall.png'
    # make files
    outfile_Nspikes = open(outfilename_Nspikes,'w')
    outfile_APampl  = open(outfilename_APampl,'w')
    outfile_APmins  = open(outfilename_APmins,'w')
    outfile_APdhw   = open(outfilename_APdhw,'w')
    outfile_ISI     = open(outfilename_ISI,'w')
    firedbefore = False
    for j in range(NCms):
        print('Step ', j+1, ' of', NCms, ', cm=',cm[j])
        infolder = 'Results/IStim/Soma%i/dendlen%i/denddiam'% (somasize,dendlen)+str(denddiam)+'/'+currentfolder
        filename = infolder+'basHHdendpass_cm'+str(cm[j])+'_idur%.1f_iamp'%idur+str(iamp)+'_Ra%i_vinit' %Ra+str(v_init)+'_V.txt' 
        Nspikes[j], peaktimes, avg_AP_mins[j], rms_AP_mins[j], avg_AP_ampl[j], rms_AP_ampl[j], avg_AP_halfwidth[j], rms_AP_halfwidth[j], avg_ISI[j], rms_ISI[j], ISI = manual(filename,idelay,idur,spikedurat)
        if Nspikes[j]!=0 and firedbefore==False:
            firedbefore = True
        if Nspikes[j]!=0 or firedbefore==False:
            outfile_Nspikes.write('%.5f %i\n' % (cm[j],Nspikes[j]))
        if Nspikes[j]!=0:
            outfile_APampl.write('%.5f %.10f %.10f\n' % (cm[j],avg_AP_ampl[j],rms_AP_ampl[j]))
            outfile_APmins.write('%.5f %.10f %.10f\n' % (cm[j],avg_AP_mins[j],rms_AP_mins[j]))
            outfile_APdhw.write('%.5f %.10f %.10f\n' % (cm[j],avg_AP_halfwidth[j],rms_AP_halfwidth[j]))
            outfile_ISI.write('%.5f %.10f %.10f\n' % (cm[j],avg_ISI[j],rms_ISI[j]))
            # Write all ISIs:
            outfilename_ISI_all = outfolder+'basHHdpas_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmf'+str(cm[j])+'_ISIall_vs_Cmall.txt'
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
    plt.title(r'Capacitance vs number of spikes, BASHH')
    plt.tight_layout()
    plt.savefig(plotname_Nspikes)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_ampl, yerr=rms_AP_ampl, capsize=2)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'Peak voltage [mV]')
    plt.title(r'Capacitance vs peak voltage, BASHH')
    plt.tight_layout()
    plt.savefig(plotname_APampl)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_mins, yerr=rms_AP_mins, capsize=2)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'Peak voltage [mV]')
    plt.title(r'Capacitance vs min peak value at I=%.2f, BAS HH' % iamp)
    plt.tight_layout()
    plt.savefig(plotname_APmins)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_halfwidth, yerr=rms_AP_halfwidth, capsize=2)
    plt.xlabel(r'$C_{m} $[$\mu$ F/cm$^2$]')
    plt.ylabel(r'Spike duration at %s mV [ms] % str(spikedurat)')
    plt.title(r'Capacitance vs spike duration at %s mV, BASHH' % str(spikedurat))
    plt.tight_layout()
    plt.savefig(plotname_APdhw)

    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_ISI, yerr=rms_ISI, capsize=2)
    plt.xlabel(r'$C_{m} $[$\mu$ F/cm$^2$]')
    plt.ylabel(r'Interspike interval [ms]')
    plt.title(r'Capacitance vs interspike interval at I=%.2f, BASHH' % iamp)
    plt.tight_layout()
    plt.savefig(plotname_ISI)
    
