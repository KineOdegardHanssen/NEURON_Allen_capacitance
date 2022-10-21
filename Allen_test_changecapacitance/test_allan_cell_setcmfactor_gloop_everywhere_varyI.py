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
cm_changecmf = 1.0

varymech = 'None' #'Na' # 'K' # 'pas'
varyE_bool = False # True 
namestringfirst = ''
if varymech=='Na':
    varyE = 40 
    namestringfirst = namestringfirst + 'ENa'+str(varyE)
elif varymech=='K':
    varyE = -100 
    namestring = namestringfirst + 'EK'+str(varyE)
elif varymech=='pas': 
    varyE = -83 
    namestringfirst = namestringfirst + 'EK'+str(varyE)
elif varymech=='None':
    varyE = 'None'
varygbool = True # False # 
varyIh       = False # True # 
vary_NaV     = False # True # 
vary_Kd      = False # True # 
vary_Kv2like = False # True # 
vary_Kv3_1   = True # False # True # 
vary_K_T     = False # True # 
vary_Im_v2   = False # True # 
vary_SK      = False # True #   
vary_Ca_HVA  = False # True # 
vary_Ca_LVA  = False # True # 
vary_gpas    = False # True # 

varyglist =[4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9]#,60.0,61.0,62.0,63.0,64.0,65.0,66.0,67.0,68.0,69.0,71.0,72.0,73.0,74.0]#[16.0,16.1,16.2,16.3,16.4,16.5,16.6,16.7,16.8,16.9,17.0]#[5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9]#[1.81,1.82,1.83,1.84,1.85,1.86,1.87,1.88,1.89]#[6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,7.0,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9]#[0.02,0.03,0.04]#[2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9]#[25.0,26.0,27.0,28.0,29.0,30.0,31.0,32.0,33.0,34.0,35.0,36.0,37.0,38.0,39.0,40.0,41.0,42.0,43.0,44.0,45.0,46.0,47.0,48.0,49.0]#[13.1,13.2,13.3,13.4,13.5,13.6,13.7,13.8,13.9]#[3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9]#[25.1,25.2,25.3,25.4,25.5,25.6,25.7,25.8,25.9,26,26.1,26.2,26.3,26.4,26.5,26.6,26.7,26.8,26.9] #[0.06,0.07,0.08,0.09,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29] # [1.6,1.7,1.8,1.9] # 'None' # 
 

# "gbar_Ih"	"gbar_NaV"	"gbar_Kd"	"gbar_Kv2like"		"gbar_Kv3_1"	"gbar_K_T"	"gbar_Im_v2"	"gbar_SK"	"gbar_Ca_HVA"		"gbar_Ca_LVA"	
# "g_pas" (set individually in soma, dend, axon)
# Change current:
idur = 2000 # ms # 
iamp = 0.4

idelay = 100  #     ms #
afteri = 100  #     ms # 

tstop_i = idur+afteri+idelay

if varyIh==True:
    namestringfirst = namestringfirst + '_gIh'
if vary_NaV==True:
    namestringfirst = namestringfirst + '_gNaV'
if vary_Kd==True:
    namestringfirst = namestringfirst + '_gKd'
if vary_Kv2like==True:
    namestringfirst = namestringfirst + '_gKv2like'
if vary_Kv3_1==True:
    namestringfirst = namestringfirst + '_gKv31'
if vary_K_T==True:
    namestringfirst = namestringfirst + '_gKT'
if vary_Im_v2==True:
    namestringfirst = namestringfirst + '_gImv2'
if vary_SK==True:
    namestringfirst = namestringfirst + '_gSK'
if vary_Ca_HVA==True:
    namestringfirst = namestringfirst + '_gCaHVA'
if vary_Ca_LVA==True:
    namestringfirst = namestringfirst + '_gCaLVA'
if vary_gpas==True: 
    namestringfirst = namestringfirst + '_gpas'

def return_allen_cell_model(model_folder,gfac):

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
        
     
    for sec in neuron.h.allsec():
        sectype = sec.name().split("[")[0]
        warning = 'Appropriate amount of gs set (zero or one)'
        gnumber = 0
        # First: Change mechanisms 
        # Mechanisms that can be anywhere
        if varymech=='pas':
            if varyE!='None':
                sec.e_pas = varyE
        if vary_gpas==True: 
            sec.g_pas *= gfac
            gnumber+=1
        if sectype=='soma':
            if varymech=='Na':
                if varyE!='None':
                    sec.ena = varyE
            elif varymech=='K':
                if varyE!='None':
                    sec.ek = varyE
            if varygbool==True: 
                if varyIh==True:
                    sec.gbar_Ih *= gfac 
                    gnumber+=1
                if vary_NaV==True:
                    sec.gbar_NaV *= gfac
                    gnumber+=1
                if vary_Kd==True:
                    sec.gbar_Kd *= gfac 
                    gnumber+=1
                if vary_Kv2like==True:
                    sec.gbar_Kv2like *= gfac
                    gnumber+=1
                if vary_Kv3_1==True:
                    sec.gbar_Kv3_1 *= gfac
                    gnumber+=1
                if vary_K_T==True:
                    sec.gbar_K_T *= gfac 
                    gnumber+=1
                if vary_Im_v2==True:
                    sec.gbar_Im_v2 *= gfac 
                    gnumber+=1
                if vary_SK==True:
                    sec.gbar_SK *= gfac
                    gnumber+=1
                if vary_Ca_HVA==True:
                    sec.gbar_Ca_HVA *= gfac 
                    gnumber+=1
                if vary_Ca_LVA==True:
                    sec.gbar_Ca_LVA *= gfac 
                    gnumber+=1
                if gnumber>1:
                    warning = 'WARNING! %i gs set, max. 1 appropriate!' % gnumber
    
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

for g in varyglist:
    namestring = namestringfirst + str(g)+'p'
    for model_idx in range(len(all_models)):
        model_name = all_models[model_idx]
        model_folder = join("cell_models", model_name)
    
        cell = return_allen_cell_model(model_folder,g)
    
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

        fig.savefig(join("figures", "%i" % testmodel,"current_idur%i_iamp" % idur + str(iamp),  '{}_changecmf{}_everywhere_vinit{}_addedRa.png'.format(namestring,cm_changecmf,v_init)))
        
        for sec in neuron.h.allsec():
            neuron.h.psection()

        fig = plt.figure(figsize=[12, 8])
        plt.plot(cell.tvec, cell.vmem[0, :])
        plt.xlabel('Time (ms)')
        plt.ylabel('Potential (mV)')
        plt.title('Membrane potential in soma')
        plt.legend(loc='upper right')
        fig.savefig(join("figures", "%i" % testmodel,"current_idur%i_iamp" % idur + str(iamp),  '{}_changecmf{}_everywhere_vinit{}_addedRa_big.png'.format(namestring,cm_changecmf,v_init)))
        
        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/"+namestring+"_changecmf" + str(cm_changecmf) + "_everywhere_vinit"+str(v_init)+"_addedRa.txt"
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
        vthr  = -40  If there is a peak above this value, we count it
        vprev = vthr-40 # A peak never kicks in at initiation, even if I change vthr
        Npeaks = 0
        for i in range (1,len(vmem_soma)-1):  
            if vmem_soma[i-1]<vmem_soma[i] and vmem_soma[i+1]<vmem_soma[i] and vmem_soma[i]>vthr:
                Npeaks+=1
        print(Npeaks, ' peaks for model ', testmodel, ',' , namestring)
        print('iamp:',iamp)
        print(namestring)
        print('vmax:', vmax)

        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/"+namestring+"_changecmf" + str(cm_changecmf) + "_everywhere_vinit"+str(v_init)+"_addedRa_vmax.txt"
        outfile = open(outfilename,'w') 
        outfile.write('%.5f' % vmax)
        outfile.close()   
        
        outfilename = "figures/%i/current_idur%i_iamp" % (testmodel,idur) + str(iamp)+"/"+namestring+"_changecmf" + str(cm_changecmf) + "_everywhere_vinit"+str(v_init)+"_addedRa_Npeaks.txt"
        outfile = open(outfilename,'w') 
        outfile.write('%i' % Npeaks)
        outfile.close()   
    
        print(namestring)
        t1 = tm.clock()
        print('Run time:', t1-t0)
        print('changecmf:',cm_changecmf)
    cell.__del__()                            
sys.exit()
