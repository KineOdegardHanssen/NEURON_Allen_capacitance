import os
from os.path import join
import sys
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import json
import neuron
import time as tm
import numpy as np

import LFPy

t0 = tm.clock()
## Choose model(s) to test:
#testmodel = 488462965 
#testmodel = 478513407 
testmodel = 478513437 
testmodelname = 'neur_%i' % testmodel
all_models    = [testmodelname]

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

# Defaulting to original values:
# DO NOT TOUCH THESE!
# SET THEM BELOW INSTEAD!
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
    
### Changing values:
# Changing values of membrane capacitance:
cm_changecmf = 1.5
changedg     = 10.0
setcao       = 20.0 #2000.0 #0.02
namestring = '_cao'+str(setcao)

varymech = 'None' # 'Na' # 'K' # 'pas'
varyE_bool = False # True # 
if varymech=='Na':
    varyE = 63 #[40,50,53,60,70]
    namestring = namestring + 'ENa'+str(varyE)
elif varymech=='K':
    varyE = -107 
    namestring = namestring + 'EK'+str(varyE)
elif varymech=='pas':
    varyE = -77
    namestring = namestring + 'Epas'+str(varyE)
elif varymech=='None':
    varyE = 'None'
varygbool = True # False # 
varyIh       = False
vary_NaV     = False 
vary_Kd      = False
vary_Kv2like = False 
vary_Kv3_1   = False
vary_K_T     = False
vary_Im_v2   = False
vary_SK      = True # False
vary_Ca_HVA  = False
vary_Ca_LVA  = False
vary_gpas    = False 



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

# "gbar_Ih"	"gbar_NaV"	"gbar_Kd"	"gbar_Kv2like"		"gbar_Kv3_1"	"gbar_K_T"	"gbar_Im_v2"	"gbar_SK"	"gbar_Ca_HVA"		"gbar_Ca_LVA"	
# "g_pas" (set individually in soma, dend, axon)
# Change current:
idur = 2000 # ms # 
if testmodel==478513437:
    iamps = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8]
elif testmodel==478513407:
    iamps = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5]
elif testmodel==488462965:
    iamps = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7]
idelay = 100  #     ms #
afteri = 100  #     ms # 

tstop_i = idur+afteri+idelay

def return_allen_cell_model(model_folder):

    params = json.load(open(join(model_folder, "fit_parameters.json"), 'r'))

    Ra = params["passive"][0]["ra"]

    e_pas = params["passive"][0]["e_pas"]
    celsius = params["conditions"][0]["celsius"]
    cm_base = params["passive"][0]["cm"][0]["cm"]
    reversal_potentials = params["conditions"][0]["erev"]
    v_init = params["conditions"][0]["v_init"]
    active_mechs = params["genome"]
    neuron.h.celsius = celsius


    # Define cell parameters
    cell_parameters = {
        'morphology': join(model_folder, 'reconstruction.swc'),
        'v_init': v_init,    # initial membrane potential
        'passive': False,   # turn on NEURONs passive mechanism for all sections
        'nsegs_method': 'fixed_length', # spatial discretization method
        'max_nsegs_length': 20.,
        #'lambda_f' : 200.,           # frequency where length constants are computed
        'dt': 2.**-7,      # simulation time step size
        'tstart': -600.,      # start time of simulation, recorders start at t=0
        'tstop': tstop_i,     # stop simulation at tstop_i ms.
        'custom_code': ['remove_axon.hoc']
    }

    cell = LFPy.Cell(**cell_parameters)
    cell.set_rotation(z=np.pi/1.25)

    pnncutoff = 0
    for sec in neuron.h.allsec(): # Extracting soma length
        sectype = sec.name().split("[")[0]
        if sectype=="soma":
            somasec = sec
            pnncutoff = 3.5*sec.L 

    for sec in neuron.h.allsec():
        sec.insert("pas")
        sec.e_pas = e_pas
        sec.Ra = Ra
        sectype = sec.name().split("[")[0]
        
        cm_new = cm_base*cm_changecmf
        for sec_dict in active_mechs:
            if sec_dict["section"] == sectype:
                if sectype=="soma": # Works
                    exec("sec.cm = {}".format(cm_new))
                if sectype=="dend": # Works
                    ### TEST FOR DISTANCE 
                    section = sec
                    dist = neuron.h.distance(somasec(0.5),section(1))
                    if dist<=pnncutoff:
                        exec("sec.cm = {}".format(cm_new))
                    else:
                        exec("sec.cm = {}".format(cm_dend))
                        for seg in sec:
                            if neuron.h.distance(somasec(0.5),seg)<=pnncutoff:
                                exec("seg.cm = {}".format(cm_new)) # 
                                
                if sectype=="axon": # Works
                    exec("sec.cm = {}".format(cm_axon))
                if not sec_dict["mechanism"] == "":
                    sec.insert(sec_dict["mechanism"])
                exec("sec.{} = {}".format(sec_dict["name"], sec_dict["value"]))

        for sec_dict in reversal_potentials:
            if sec_dict["section"] == sectype:
                print(sectype, sec_dict)
                for key in sec_dict.keys():
                    if not key == "section":
                        exec("sec.{} = {}".format(key, sec_dict[key]))
    
    cell.cao0_ca_ion = setcao
    for sec in neuron.h.allsec():
        sectype = sec.name().split("[")[0]
        if sectype=="soma":
            print("cao before:",sec.cao)
            sec.cao = setcao
            
            print("cao after:",sec.cao)
            print("Successfully changed cao!!!")
    
    print("Double checking if cao has actually been changed:")
    for sec in neuron.h.allsec():
        sectype = sec.name().split("[")[0]
        if sectype=="soma":
            print("cao now:",sec.cao)
    print("cao0_ca_ion now:",cell.cao0_ca_ion)
     
    for sec in neuron.h.allsec():
        sectype = sec.name().split("[")[0]
        if varymech=='pas':
            if varyE!='None':
                sec.e_pas = varyE
        if vary_gpas==True:
            sec.g_pas *= changedg 
        if sectype=='soma':
            if varymech=='Na':
                if varyE!='None':
                    sec.ena = varyE
            elif varymech=='K':
                if varyE!='None':
                    sec.ek = varyE
            if varygbool==True: 
                if varyIh==True:
                    sec.gbar_Ih *= changedg 
                if vary_NaV==True:
                    sec.gbar_NaV *= changedg 
                if vary_Kd==True:
                    sec.gbar_Kd *= changedg 
                if vary_Kv2like==True:
                    sec.gbar_Kv2like *= changedg 
                if vary_Kv3_1==True:
                    sec.gbar_Kv3_1 *= changedg 
                if vary_K_T==True:
                    sec.gbar_K_T *= changedg 
                if vary_Im_v2==True:
                    sec.gbar_Im_v2 *= changedg 
                if vary_SK==True:
                    sec.gbar_SK *= changedg 
                if vary_Ca_HVA==True:
                    sec.gbar_Ca_HVA *= changedg 
                if vary_Ca_LVA==True:
                    sec.gbar_Ca_LVA *= changedg 
        
    return cell

cell_models_folder = "cell_models"

mod_folder = "Allen_test_changecapacitance/cell_models/"+testmodelname+"/modfiles"
if "win64" in sys.platform:
    print('Detected sys.platform as win64')
    warn("no autompile of NMODL (.mod) files on Windows. " 
         + "Run mknrndll from NEURON bash in the folder cells and rerun example script")
    if not pth in neuron.nrn_dll_loaded:
        neuron.h.nrn_load_dll(mod_folder+"/nrnmech.dll")
    neuron.nrn_dll_loaded.append(mod_folder)

for iamp in iamps:
    for model_idx in range(len(all_models)):
        model_name = all_models[model_idx]
        model_folder = join("cell_models", model_name)
    
        cell = return_allen_cell_model(model_folder)
    
        pointprocess = {
                'idx': 0,
                'record_current': True,
                'pptype': 'IClamp',
                'amp': iamp,
                'dur': idur,
                'delay': idelay,
            }
        stimulus = LFPy.StimIntElectrode(cell,**pointprocess)
        cell.simulate(rec_vmem=True, rec_variables=['cai'])
        
        plt.close("all")
        fig = plt.figure(figsize=[12, 8])
        fig.subplots_adjust(wspace=0.5)
        ax1 = fig.add_subplot(231, aspect=1, xlabel="x", ylabel="z")
        ax2 = fig.add_subplot(234, aspect=1, xlabel="x", ylabel="y")
        ax3 = fig.add_subplot(132, xlabel="ms", ylabel="mV")
        ax4 = fig.add_subplot(133, xlabel="ms", ylabel="nA")

        [ax1.plot([cell.xstart[idx], cell.xend[idx]],
              [cell.zstart[idx], cell.zend[idx]], c='k') for idx in range(cell.totnsegs)]

        [ax2.plot([cell.xstart[idx], cell.xend[idx]],
              [cell.ystart[idx], cell.yend[idx]], c='k') for idx in range(cell.totnsegs)]

        ax3.plot(cell.tvec, cell.somav)

        ax4.plot(cell.tvec, stimulus.i)

        fig.savefig(join("figures", "%i" % testmodel,"current_idur%i_iamp" % idur + str(iamp),  '{}_changecmf{}_somaprox_vinit{}_addedRa_man.png'.format(namestring,cm_changecmf,v_init)))
        
        for sec in neuron.h.allsec():
            neuron.h.psection()

        fig = plt.figure(figsize=[12, 8])
        plt.plot(cell.tvec, cell.vmem[0, :])
        plt.xlabel('Time (ms)')
        plt.ylabel('Potential (mV)')
        plt.title('Membrane potential in soma')
        plt.legend(loc='upper right')
        fig.savefig(join("figures", "%i" % testmodel,"current_idur%i_iamp" % idur + str(iamp),  '{}_changecmf{}_somaprox_vinit{}_addedRa_big_man.png'.format(namestring,cm_changecmf,v_init)))
        
        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/"+namestring+"_changecmf" + str(cm_changecmf) + "_somaprox_vinit"+str(v_init)+"_addedRa_man.txt"
        outfile = open(outfilename,'w')
        vmem_soma = cell.vmem[0,:]
        Ca_soma   = cell.rec_variables['cai'][0, :] 
        
        time = cell.tvec # time
        Nt   = len(time)
        
        for i in range(Nt):
            outfile.write('%.16f %.16f\n' % (time[i],vmem_soma[i]))
        outfile.close()    
        
        vmax = max(vmem_soma) 
        vmin = min(vmem_soma) 
        deltav = vmax-vmin
        vthr  = -40 # If there is a peak above this value, we count it
        vprev = vthr-40 # A peak never kicks in at initiation, even if I change vthr
        Npeaks = 0
        for i in range (1,len(vmem_soma)-1):  
            if vmem_soma[i-1]<vmem_soma[i] and vmem_soma[i+1]<vmem_soma[i] and vmem_soma[i]>vthr:
                Npeaks+=1
        print(Npeaks, ' peaks for model ', testmodel, ', current ', iamp)
        print('iamps:',iamps)
        print('vmax:', vmax)

        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/"+namestring+"_changecmf" + str(cm_changecmf) + "_somaprox_vinit"+str(v_init)+"_addedRa_vmax_man.txt"
        outfile = open(outfilename,'w') 
        outfile.write('%.5f' % vmax)
        outfile.close()   
        
        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/"+namestring+"_changecmf" + str(cm_changecmf) + "_somaprox_vinit"+str(v_init)+"_addedRa_Npeaks_man.txt"
        outfile = open(outfilename,'w') 
        outfile.write('%i' % Npeaks)
        outfile.close()   
    
        print('iamp:',iamp)
        t1 = tm.clock()
        print('Run time:', t1-t0)
        print('changecmf:',cm_changecmf)
    cell.__del__()                            
sys.exit()
