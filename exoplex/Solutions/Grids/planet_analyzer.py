import numpy as np
import pandas as pd



class Planet(object):
    """
        this class will prepare the data for you
        you can add functions to it if you want to add a plotting routine
        or anything else
    """

    def __init__(self,file_name):

        self.mantle_composition = self._get_mantle_composition(file_name)
        self.data = self._get_planet_data(file_name)


    def _get_mantle_composition(self,file_name):
        """
            find mantle composition in the header of the file you want
            in this case, it is called planet_file
        """
        mantle_composition_params = ["Fe/Mg", "Si/Mg", "Ca/Mg", "Al/Mg"]
        with open(file_name, "r") as p:
            line = p.readline()
            cnt=0
            while cnt<2:
                line=p.readline()
                cnt+=1

            mantle_comp_dict = dict(zip(mantle_composition_params, line.split()[1:]))
            p.close()

        return mantle_comp_dict

    def _get_columns_names(self,file_name):
        """
            just finds the columns names from the file
        """
        with open(file_name, "r") as p:
            line = p.readline()
            cnt=0
            while cnt<4:
                line=p.readline()
                cnt+=1


        col_names = line.split()[1:]

        return col_names

    def _get_planet_data(self,file_name):
        columns = self._get_columns_names(file_name)
        planet_data = np.genfromtxt(file_name, skip_header = 4, delimiter=",").T
        # replace nan with 0
        planet_data = np.nan_to_num(planet_data, copy=True)
        # name the columns using the columns names above
        # this leaves you with all the data you need
        planet_data = dict(zip(columns, planet_data))

        return planet_data


"""
    example of how to call planet object
    the only argument is the file name

    right now it has three attributes:
    mantle_composition
    data

    you access these by typing
    planet_1.mantle_composition and planet_1.data

"""

planet_1 = Planet("planet0100.dat")








