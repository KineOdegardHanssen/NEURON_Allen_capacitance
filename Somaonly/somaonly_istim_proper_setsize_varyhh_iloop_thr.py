import numpy as np
import matplotlib.pyplot as plt

import neuron
from neuron import h
import LFPy
################################ HH #############################
# Default HH values:
ena = 50
ek = -77
el_hh = -54.3
gnabar_hh = 0.12
gkbar_hh = 0.036
gl_hh = 0.0003

### Change HH values here: ####
#ena = 49.3
#ek = ek-20
#el_hh = el_hh+10
#gnabar_hh *= 1.0
#gkbar_hh = 0.020
#gl_hh = 0

######################### Other params ##########################
# iamps: nA
iamps = [0.0,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.02,0.021, 0.022,0.023,0.024,0.025]
idur = 1000
idelay = 10
tstop = idur+idelay+10.
v_init = -70

cm = 0.5
Ra = 100.
somasize = 10  ### Change this in h("""...""") too.

for iamp in iamps:
    h("""
    create soma
    objref all
    
    soma.L = 10
    soma.diam = 10  
    
    all = new SectionList()
    soma all.append()
    
    forall {nseg = 1}
    
    Ra = 100.
    cm = 0.5
    Rm = 30000
    
    forall {
        insert hh
        }
    """) 
    
    # Vary HH properties:
    for sec in h.soma:
        sec.ena       = ena
        sec.ek        = ek
        sec.el_hh     = el_hh
        sec.gnabar_hh = gnabar_hh
        sec.gkbar_hh  = gkbar_hh
        sec.gl_hh     = gl_hh
    
    
    dt = 2**-7
    print("dt: ", dt)
    cell_params = {          # various cell parameters,
                'morphology': h.all, 
                'delete_sections': False,
                'v_init' : v_init,    # initial crossmembrane potential
                'cm': cm,
                'Ra': Ra,
                'passive' : False,   # switch on passive mechs
                'nsegs_method' : None,
                'dt' : dt,   # [ms] dt's should be in powers of 2 for both,
                'tstart' : -600.,    # start time of simulation, recorders start at t=0
                'tstop' : tstop,   # stop simulation at 200 ms. These can be overridden
            }
    
    
    cell = LFPy.Cell(**cell_params)
    
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
    
    for sec in neuron.h.allsec():
        neuron.h.psection()
    
    #ena, ek, el_hh, gnabar_hh, gkbar_hh, gl_hh
    folder = 'Results/IStim/Soma%i/current_idur%i_iamp'%(somasize,idur)+str(iamp)+'/'
    hhstring = '_ena'+str(ena)+'_ek'+str(ek)+'_el'+str(el_hh)+'_gnabar'+str(gnabar_hh)+'_gkbar'+str(gkbar_hh)+'_gl'+str(gl_hh)
    filename = folder+'somaonly_cm'+str(cm)+'_idur%i_iamp'%idur+str(iamp)+hhstring+'_Ra%i_vinit' %Ra+str(v_init)+'_V.txt' 
    plotname = folder+'somaonly_cm'+str(cm)+'_idur%i_iamp'%idur+str(iamp)+hhstring+'_Ra%i_vinit' %Ra+str(v_init)+'_V.png' 
    
    plt.figure(figsize=(6,5))
    plt.plot(cell.tvec, cell.vmem[0,:])
    
    plt.savefig(plotname, dpi=300)

    V = cell.vmem[0,:]
    
    file = open(filename,'w')
    for i in range(len(V)):
        file.write('%.16e %.16e\n' % (cell.tvec[i],V[i]))
    file.close()
    
    cell.__del__()      
