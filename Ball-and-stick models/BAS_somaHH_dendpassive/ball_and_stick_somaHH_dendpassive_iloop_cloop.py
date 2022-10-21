import numpy as np
import matplotlib.pyplot as plt
from neuron import h
import LFPy

def run_sim(somasize, dendlen, denddiam, cm=1.0, cmfac=1.0, idur=1.0, iamp=1.0, idelay=1.0, v_init=-65., tstart=-100., tstop=50., Ra=150, nsegments=200, dtexp=-7):

    dt = 2**dtexp
    cell_params = {          # various cell parameters,
                'morphology': "ballandstick.hoc",
                'v_init' : v_init,    # initial crossmembrane potential
                'cm': cm,
                'Ra': Ra,
                'passive': False,
                'passive_parameters': {'g_pas': 1./30000, 'e_pas': -65},
                'nsegs_method' : "lambda_f",
                'lambda_f': 200,
                'dt' : dt,   # [ms] dt's should be in powers of 2
                'tstart' : tstart,
                'tstop' : tstop,
            }


    cell = LFPy.Cell(**cell_params)
    h("soma insert hh")  # Inserting Hodgkin-Huxley mechanisms in soma
    h("dend insert pas") # Inserting passive mechanism in dendrite
    
    # Changing mechanisms
    # AND
    # Changing cm in proximal regions
    cmthis = cm*cmfac
    for sec in h.allsec():
        sec.Ra = Ra
        sectype = sec.name().split("[")[0]
        
        if sectype=="soma": # Works
            exec("sec.cm = {}".format(cmthis))
            sec.L = somasize
            sec.diam = somasize
            somasec  = sec
        if sectype=="dend":
            # First: Change passive mechanisms
            sec.e_pas = -65 
            sec.g_pas = 0.0003     
            # Then: Change geometry
            sec.L = dendlen
            sec.diam = denddiam
            sec.nseg = nsegments
            exec("sec.cm = {}".format(cmthis))
    
    stim_idx = 0
    stim_params = {
            'idx': stim_idx,
            'record_current': True,
            'pptype': 'IClamp',
            'amp': iamp,
            'dur': idur,
            'delay': idelay,
        }

    stimulus = LFPy.StimIntElectrode(cell, **stim_params)
    cell.simulate(rec_vmem=True, rec_imem=True)
    t, v = cell.tvec.copy(), cell.vmem[0].copy()
    
    if cm==1:
        for sec in h.allsec():
            h.psection()
    
    cell.__del__()
    return t, v


if __name__ == '__main__':
    cm     = 1.0
    cmfacs = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
    iamps  = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]
    idur     = 1000
    idelay   = 100.0
    afteri   = 10.0
    tstart   = -600.
    tstop_i  = idur+afteri+idelay
    v_init   = -65
    Ra       = 100
    somasize = 10
    denddiam = 1
    dendlen  = 1000
    outfolder_base = 'Results/IStim/Soma%i/dendlen%i/denddiam%i/' % (somasize,dendlen,denddiam)
    for iamp in iamps:
        currentfolder = 'current_idur'+str(idur)+'_iamp'+str(iamp)+'/'
        outfolder = outfolder_base+currentfolder 
        for cmfac in cmfacs:
            t, v = run_sim(somasize, dendlen, denddiam, cm, cmfac, idur, iamp, idelay, v_init, tstart, tstop_i,Ra)
            outfilename = outfolder+'basHHdendpass_cm'+str(cmfac)+'_idur%.1f_iamp'%idur+str(iamp)+'_Ra%i_vinit' %Ra+str(v_init)+'_V.txt' 
            outfile = open(outfilename,'w')
    
            Nt   = len(t)
            for i in range(Nt):
                outfile.write('%.16f %.16f\n' % (t[i],v[i]))
            outfile.close()    
            plotname = outfolder+'basHHdendpass_cm'+str(cmfac)+'_idur%.1f_iamp'%idur+str(iamp)+'_Ra%i_vinit'%Ra+str(v_init)+'_V.png'
            plt.figure(figsize=(6,5))
            plt.plot(t, v, label="c$_m$= {:1.2f} µF/cm²".format(cm))
            plt.xlabel('Time [ms]')
            plt.ylabel('Voltage [mV]')
            plt.title(r'Voltage vs time for different cell capacitances $c_m$ (current input)')
            plt.legend()
            plt.savefig(plotname)
