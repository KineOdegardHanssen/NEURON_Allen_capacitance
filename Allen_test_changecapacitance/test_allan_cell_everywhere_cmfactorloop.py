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
testmodel = 488462965 
#testmodel = 478513407 
#testmodel = 478513437 
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
    
# Changing values of membrane capacitance:
cm_changecmfs = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]

# Change current:
idur = 2000 # ms 
iamp = 0.4  # nA 

idelay = 100  #     ms #
afteri = 100  #     ms # 

tstop_i = idur+afteri+idelay

def return_allen_cell_model(model_folder,cm_changecmf):

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
        'dt': 2.**-7,      # simulation time step size
        'tstart': -600.,      # start time of simulation, recorders start at t=0
        'tstop': tstop_i,     # stop simulation at tstop_i ms.
        'custom_code': ['remove_axon.hoc']
    }

    cell = LFPy.Cell(**cell_parameters)
    cell.set_rotation(z=np.pi/1.25)

    for sec in neuron.h.allsec():
        sec.insert("pas")
        sec.e_pas = e_pas
        sec.Ra = Ra
        sectype = sec.name().split("[")[0]
        
        cm_new = cm_base*cm_changecmf
        for sec_dict in active_mechs:
            if sec_dict["section"] == sectype:
                exec("sec.cm = {}".format(cm_new))
                if not sec_dict["mechanism"] == "":
                    sec.insert(sec_dict["mechanism"])
                exec("sec.{} = {}".format(sec_dict["name"], sec_dict["value"]))

        for sec_dict in reversal_potentials:
            if sec_dict["section"] == sectype:
                print(sectype, sec_dict)
                for key in sec_dict.keys():
                    if not key == "section":
                        exec("sec.{} = {}".format(key, sec_dict[key]))
    
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

for cm_changecmf in cm_changecmfs:
    for model_idx in range(len(all_models)):
        model_name = all_models[model_idx]
        model_folder = join("cell_models", model_name)
    
        cell = return_allen_cell_model(model_folder,cm_changecmf)
    
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

        fig.savefig(join("figures", "%i" % testmodel,"current_idur%i_iamp" % idur + str(iamp),  'idur{}_iamp{}_{}_changecmf{}_all_vinit{}_addedRa.png'.format(idur, iamp, testmodel,cm_changecmf,cm_dend,cm_axon,v_init)))
        
        for sec in neuron.h.allsec():
            neuron.h.psection()

        fig = plt.figure(figsize=[12, 8])
        plt.plot(cell.tvec, cell.vmem[0, :])
        plt.xlabel('Time (ms)')
        plt.ylabel('Potential (mV)')
        plt.title('Membrane potential in soma')
        plt.legend(loc='upper right')
        fig.savefig(join("figures", "%i" % testmodel,"current_idur%i_iamp" % idur + str(iamp),  'idur{}_iamp{}_{}_changecmf{}_all_vinit{}_addedRa_big.png'.format(idur, iamp, testmodel,cm_changecmf,cm_dend,cm_axon,v_init)))
        
        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/idur%i_iamp" % idur + str(iamp)+"_changecmf" + str(cm_changecmf) + "_all" + "_vinit"+str(v_init)+"_addedRa.txt"
        outfile = open(outfilename,'w')
        vmem_soma = cell.vmem[0,:]
        Ca_soma   = cell.rec_variables['cai'][0, :] 
        
        time = cell.tvec # time
        Nt   = len(time)
        
        for i in range(Nt):
            outfile.write('%.16f %.16f %.16f\n' % (time[i],vmem_soma[i],Ca_soma[i]))
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
        print('iamp:',iamp)
        print('vmax:', vmax)

        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/idur%i_iamp" % idur + str(iamp)+"_changecmf" + str(cm_changecmf) + "_all" + "_vinit"+str(v_init)+"_addedRa_vmax.txt"
        outfile = open(outfilename,'w') 
        outfile.write('%.5f' % vmax)
        outfile.close()   
        
        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/idur%i_iamp" % idur + str(iamp)+"_changecmf" + str(cm_changecmf) + "_all" + "_vinit"+str(v_init)+"_addedRa_Npeaks.txt"
        outfile = open(outfilename,'w') 
        outfile.write('%i' % Npeaks)
        outfile.close()   
    
        print('iamp:',iamp)
        t1 = tm.clock()
        print('Run time:', t1-t0)
        print('changecmf:',cm_changecmf, '; cm_dend:', cm_dend, '; cm_axon:', cm_axon)
    cell.__del__()                            
sys.exit()
