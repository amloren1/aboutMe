# coding: utf-8
# This file is part of ExoPlex - a self consistent planet builder
# Copyright (C) 2017 - by the ExoPlex team, released under the GNU
# GPL v2 or later.


#**********************************************************************#
'''
This script contains functions which call on the ExoPlex backend code
to create planets in a veriety of scenarios:
-Model earth
-Prem
-single models of fixed radius or mass
    - calculate core mass fraction or leave it open

'''
#**********************************************************************#

import os
import sys
import io as sio

import numpy as np
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.realpath(__file__))
path = path[0:-4]

sys.path.insert(0, path)

# hack to allow scripts to be placed in subdirectories next to burnman:
# if not os.path.exists('main') and os.path.exists('../main'):
#     sys.path.insert(1, os.path.abspath('..'))

from exoplex.exoplex.run.PREM import prem as p
import main as exo




############################
'''
extract inputs from a dictionary or from file
'''
############################

def inputs_from_file(script):

    x = __import__(script, ['*'])

    compositional_params = np.empty((x.n_mod,), dtype = object)

    for i in range(x.n_mod):
        compositional_params[i] = [x.wt_frac_water[i],x.FeMg[i],x.SiMg[i],
                                x.CaMg[i],x.AlMg[i],x.xFeO[i] ,x.Si_wt[i],
                                x.O_wt[i], x.S_wt[i]]
        print(compositional_params)

    return(compositional_params)

def inputs_from_input(femg, simg, camg=0, almg=0, wtr_frac=0):

    si_cor, o_cor, s_cor, feo = (0,0,0,0)
    return [list(map(abs,[wtr_frac,femg,simg,camg,almg,feo,si_cor,o_cor, s_cor]))]

def map_inputs_from_file(script):
    x = __import__(script, ['*'])

    compositional_params = []

    for wtr_frac in x.wt_frac_water:
        for femg in x.FeMg:
            for simg in x.SiMg:
                for camg in x.CaMg:
                    for almg in x.AlMg:
                        for feo in x.xFeO:
                            for si_cor in x.Si_wt:
                                for o_cor in x.O_wt:
                                    for s_cor in x.S_wt:
                                        compositional_params.append([wtr_frac, femg, simg,
                                            camg, almg, feo, si_cor,
                                            o_cor, s_cor])
        print(compositional_params)

    return (compositional_params)

def inputs(composition, coreComp):

    SiMg       = composition.get('SiMg')
    FeMg       = composition.get('FeMg')
    CaMg       = composition.get('CaMg')
    AlMg       = composition.get('AlMg')
    fFeO_m     = composition.get('fFeO')
    wt_h2o     = composition.get('wt_h2o')


    #composition of core
    wt_frac_Si_core = coreComp.get('wtSi')
    wt_frac_O_core  = coreComp.get('wtO')
    wt_frac_S_core  = coreComp.get('wtS')

    compositional_params = [wt_frac_water,FeMg,SiMg,CaMg,AlMg,fFeO_m ,wt_frac_Si_core, \
                          wt_frac_O_core,wt_frac_S_core]

    return(compositional_params)

############################
'''
get input from input.py
'''
############################
from params import (
    Pressure_range_mantle_UM,
    Temperature_range_mantle_UM,
    resolution_UM,
    Pressure_range_mantle_LM,
    Temperature_range_mantle_LM,
    resolution_LM,
    Core_rad_frac_guess,
    Mantle_potential_temp,
    h20_radfrac_guess,
    T_surface_h2o,
    num_mantle_layers,
    num_core_layers,
    number_h2o_layers,
    perplex_only,
    verbose
)

def exoplex(script=None, mass=None, femg=None, simg=None ):
    """
        accept parameter inputs as either a file or just the parameters themselves
    """
    if script:
        x = __import__(script)

        if (x.n_mod) != len(x.cmf)  \
        or (x.n_mod) != len(x.FeMg) \
        or (x.n_mod) != len(x.SiMg) \
        or (x.n_mod) != len(x.CaMg) \
        or (x.n_mod) != len(x.X)    \
        or (x.n_mod) != len(x.AlMg):
            print('\n***input ERROR: missing/extra list values in {}.py***'.format(script))
            #sys.exit()

        comp_params = map_inputs_from_file(script)
        fix_core = x.fix_core
        core_mass_fraction = x.cmf[0]
        independent_var = x.indp
        X = x.X[0]
    else:
        comp_params = inputs_from_input(femg=femg, simg=simg)
        fix_core = False
        core_mass_fraction = None
        independent_var = 'M'
        X = mass

    Planet = np.empty(len(comp_params), dtype=object)

    for i in range(len(comp_params)):

        cmf2 = {'fix_man': fix_core, 'wtCore': core_mass_fraction}
        compositional_params = comp_params[i]
        structure_params = [Pressure_range_mantle_UM,Temperature_range_mantle_UM,resolution_UM,
                         Pressure_range_mantle_LM, Temperature_range_mantle_LM, resolution_LM,
                         Core_rad_frac_guess,Mantle_potential_temp, h20_radfrac_guess, T_surface_h2o]

        layers = [num_mantle_layers,num_core_layers,number_h2o_layers]

        sol_filename = 'NXNN00'

        # Here is where the ExoPlex model is called
        # result is a profile for density, mass, radius,
        # heat capacity, emissivity of heat and mineralogy
        # run_planet_mass(mass_planet, compositional_params, structure_params, layers,filename, truncate_comp)
        if independent_var == 'M' or independent_var == 'm':
            Planet[i] = exo.run_planet_mass(X,compositional_params,structure_params,layers,sol_filename, cmf2)
        elif independent_var == 'R' or independent_var == 'r':
            Planet[i] = exo.run_planet_radius(X, compositional_params, structure_params, layers,sol_filename, cmf2)
        else:
            print('\n***Unable to interpret model selection indp = {}***'.format(x.indp))
            print('\n Please select independent parameter as \'R\' (radius) or \'M\' (mass)')
            sys.exit()
        if perplex_only:
            continue

        if verbose:

            print('radius of planet')
            print(Planet[i]['radius'][-1]/1000)

            print()
            print("Mass = ", '%.3f'%(Planet[i]['mass'][-1]/5.97e24), "Earth masses")
            print("Core Mass Fraction = ", '%.3f'%(100.*Planet[i]['mass'][num_core_layers]/Planet[i]['mass'][-1]))
            print("Core Radius Fraction = ", '%.3f'%(100.*Planet[i]['radius'][num_core_layers]/Planet[i]['radius'][-1]))
            print("CMB Pressure = " ,'%.3f' % (Planet[i]['pressure'][num_core_layers]/10000), "GPa")
            print("Central pressure = {} GPa".format(Planet[i]['pressure'][0]/10000))

    return Planet










############################
'''
Simple Earth model.

The one kwarg is to determine if model will
be for fixed radius (defaul) or mass
'''
############################



def Earth_model(**kwargs):


    Earth_mantle = {'FeMg': 0.121212121 , 'SiMg': 0.79797979797,  \
                  'AlMg': 0.09090909 , 'CaMg': 0.0656565, \
                  'fFeO': 0.0,  'wt_h2o': 0.0}

    Earth_core = {'wtSi': 0.06, 'wtO': 0.0, 'wtS':0.019}

    Earth_man_only = {'fix_man': True, 'wtCore': 0.323}

    wt_frac_water      = wt_h2o # Earth = 0.0002

    #lists of compositional and structural inputs used to build planet
    compositional_params = inputs(Earth_mantle, Earth_core)

    structure_params =  [Pressure_range_mantle_UM,Temperature_range_mantle_UM,resolution_UM,
                         Pressure_range_mantle_LM, Temperature_range_mantle_LM, resolution_LM,
                         Core_rad_frac_guess,Mantle_potential_temp, h20_radfrac_guess, T_surface_h2o]

    layers = [num_mantle_layers,num_core_layers,number_h2o_layers]

    sol_filename = 'Star_Boy37'


    #Here is where the ExoPlex model is called
    #result is a profile for density, mass, radius,
    #heat capacity, emissivity of heat and mineralogy
    #run_planet_mass(mass_planet, compositional_params, structure_params, layers,filename, truncate_comp)

    if kwargs.get('indp') == 'M' or kwargs.get('indp') == 'm':
        #sys.exit()
        Planet = exo.run_planet_mass(1.0, compositional_params,structure_params,layers,sol_filename, Earth_man_only)
    else:
        sys.exit()
        Planet = exo.run_planet_radius(1.0, compositional_params, structure_params, layers,sol_filename, Earth_man_only)

    #run_planet_radius(radius_planet, compositional_params, structure_params, layers,filename, truncate_comp)

    #Planet = exo.run_planet_Radius(1.0, compositional_params,structure_params,layers,sol_filename, fix_core)


    #print this stuff to make sure you are not going insane in da membrane
    if verbose:

        print('radius of planet')
        print(Planet['radius'][-1]/1000)

        print()
        print("Mass = ", '%.3f'%(Planet['mass'][-1]/5.97e24), "Earth masses")
        print("Core Mass Fraction = ", '%.3f'%(100.*Planet['mass'][num_core_layers]/Planet['mass'][-1]))
        print("Core Radius Fraction = ", '%.3f'%(100.*Planet['radius'][num_core_layers]/Planet['radius'][-1]))
        print("CMB Pressure = " ,'%.3f' % (Planet['pressure'][num_core_layers]/10000), "GPa")
        print("Central pressure = {} GPa".format(Planet['pressure'][0]/10000))


    return Planet


############################
'''
PREM

output dictionary with prem model
'''
############################


def prem():
    #import prem data (rad, depth, rho_depth, rho_rad)
    #keys: 'radius', 'depth', 'rho_depth', 'rho_radius' , \
    #     'VPV', 'VPH', 'VSV', 'VSH'}
    prem_dat = p.prem()

    return prem_dat



############################
'''
Single model
'''
############################

def exoplex_single(**kwargs):

    if kwargs.get('filename') != None:

        params = from_file(kwargs.get('filename'))

    else:

        compositional_params = inputs(composition, coreComp)







#TODO:
'''

3) edit input file to allow users to select output



'''

















