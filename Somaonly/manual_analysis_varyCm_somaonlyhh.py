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
        elif voltage[i]>=durthr and voltage[i+1]<durthr: # Passing downwards
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
    
    # Checking if we've got consistent firing:
    if Npeaks!=0:
        if peaktimes[-1]<=(idur/2.+idelay): # Checking for firing in the last half of the stim. interval
            Npeaks=0      
    
    dur = []
    isi = []
    Ndur = min([len(passtimes_up),len(passtimes_down)])
    for i in range(10,Ndur-1):
        dur.append(passtimes_down[i]-passtimes_up[i])
    for i in range(1,len(peaktimes)):
        isi.append(peaktimes[i]-peaktimes[i-1])
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
    idelay     = 10
    iamp       = 0.2 # nA
    v_init     = -70 # mV
    Ra         = 100
    somasize   = 10  
    dendlen    = 1000
    denddiam   = 1
    nsegments  = 200 
    
    # Default HH values:
    ena = 50
    ek = -77
    el_hh = -54.3
    gnabar_hh = 0.12
    gkbar_hh = 0.036
    gl_hh = 0.0003
    
    varymech = 'Na' # 'K' # 'leak'
    varyE_bool = False # True
    varyE = 50 #[30,40,50,60,70] 
    varyg = 'None'
    
    varylist = [] # Should be redundant
    plotstring = '_vary'
    if varyE_bool==True:
        varylist = varyE
        plotstring = plotstring + 'E'
    else:
        varylist = varyg
        plotstring = plotstring + 'g'
      
    if varymech=='Na':
        folderstring = 'VaryNa/' 
        plotstring = plotstring + '_Na'
    elif varymech=='leak':
        folderstring = 'VaryLeak/'
        plotstring = plotstring + '_leak'
    elif varymech=='K':
        folderstring = 'VaryK/'
        plotstring = plotstring + '_K'

    changestring =''
    if varyE_bool==True:
        changestring =changestring+'_E'+str(varyE)+'_gdflt'
    else:
        changestring =changestring+'_Edf_g'+str(varyg)
    
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
    outfolder = 'Results/IStim/Soma%i/current_idur%i_iamp'%(somasize,idur)+str(iamp)+'/'
    hhstring = '_ena'+str(ena)+'_ek'+str(ek)+'_el'+str(el_hh)+'_gnabar'+str(gnabar_hh)+'_gkbar'+str(gkbar_hh)+'_gl'+str(gl_hh)
    outfilename_Nspikes = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cm.txt'
    outfilename_APampl  = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmax_vs_Cm.txt'
    outfilename_APmins  = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmin_vs_Cm.txt'
    outfilename_APdhw   = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cm.txt' % str(spikedurat)
    outfilename_ISI     = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_ISI_vs_Cm.txt'
    plotname_Nspikes    = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Nspikes_vs_Cmsprx.png'
    plotname_APampl     = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmax_vs_Cm.png'
    plotname_APmins     = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_Vmin_vs_Cm.png'
    plotname_APdhw      = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_sdurat%s_vs_Cm.png' % str(spikedurat)
    plotname_ISI        = outfolder+'somaonlyHH_idur%i_iamp'% (idur)+str(iamp) +'_manual_cmfs_ISI_vs_Cm.png'
    # make files
    outfile_Nspikes = open(outfilename_Nspikes,'w')
    outfile_APampl  = open(outfilename_APampl,'w')
    outfile_APmins  = open(outfilename_APmins,'w')
    outfile_APdhw   = open(outfilename_APdhw,'w')
    outfile_ISI     = open(outfilename_ISI,'w')
    firedbefore = False
    for j in range(NCms):
        print('Step ', j+1, ' of', NCms)
        filename = outfolder+'somaonly_cm'+str(cm[j])+'_idur%i_iamp'%idur+str(iamp)+hhstring+'_Ra%i_vinit' %Ra+str(v_init)+'_V.txt' 
        Nspikes[j], peaktimes, avg_AP_mins[j], rms_AP_mins[j], avg_AP_ampl[j], rms_AP_ampl[j], avg_AP_halfwidth[j], rms_AP_halfwidth[j], avg_ISI[j], rms_ISI[j], ISI = manual(filename,idelay,idur,spikedurat)
        if Nspikes[j]!=0 and firedbefore==False:
            firedbefore=True
        if Nspikes[j]!=0 or firedbefore==False:
            outfile_Nspikes.write('%.5f %i\n' % (cm[j],Nspikes[j]))
        if Nspikes[j]!=0:
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
    plt.title(r'Capacitance vs number of spikes, one comp. HH')
    plt.tight_layout()
    plt.savefig(plotname_Nspikes)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_ampl, yerr=rms_AP_ampl, capsize=2)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'Peak voltage [mV]')
    plt.title(r'Capacitance vs peak voltage, one comp. HH')
    plt.tight_layout()
    plt.savefig(plotname_APampl)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_mins, yerr=rms_AP_mins, capsize=2)
    plt.xlabel(r'$C_{m}$ [$\mu$ F/cm$^2$]')
    plt.ylabel(r'Peak voltage [mV]')
    plt.title(r'Capacitance vs min peak value at I=%.2f, one comp. HH' % iamp)
    plt.tight_layout()
    plt.savefig(plotname_APmins)
    
    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_AP_halfwidth, yerr=rms_AP_halfwidth, capsize=2)
    plt.xlabel(r'$C_{m} $[$\mu$ F/cm$^2$]')
    plt.ylabel(r'Spike duration at %s mV [ms] % str(spikedurat)')
    plt.title(r'Capacitance vs spike duration at %s mV, one comp. HH' % str(spikedurat))
    plt.tight_layout()
    plt.savefig(plotname_APdhw)

    plt.figure(figsize=(6,5))
    plt.errorbar(cm,avg_ISI, yerr=rms_ISI, capsize=2)
    plt.xlabel(r'$C_{m} $[$\mu$ F/cm$^2$]')
    plt.ylabel(r'Interspike interval [ms]')
    plt.title(r'Capacitance vs interspike interval at I=%.2f, one comp. HH')
    plt.tight_layout()
    plt.savefig(plotname_ISI)
    
    
    # Print results to terminal
    print('Nspikes:', Nspikes)
    print('AP amplitude, avg:', avg_AP_ampl)
    print('AP amplitude, rms:', rms_AP_ampl)
    print('AP duration at half width, avg:', avg_AP_halfwidth)
    print('AP duration at half width, rms:', rms_AP_halfwidth)
