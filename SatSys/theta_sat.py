from scipy.optimize import linprog
from DataProcessing import filt_data as fd
from TemperatureSwitching import switching_handler as sh
from SatSys import phi_sat_mats as psm
from Regressor import phiT
import numpy as np


class theta_sat:
    """ Class holding the saturated system parameters for the temperature ranges """

    def __init__(self, f_dat: fd.FilteredTruckData, T_parts: list, T_ord: dict):
        """ Loads all the data and solves the linear program in each case """
        self.dat  = f_dat
        self.T_ord = T_ord
        self.T_parts = T_parts
        self.cAb = psm.cAb_mats(self.dat,  self.T_parts, self.T_ord)
        self.swh = self.cAb.swh
        self.Nparms = self.cAb.Nparms
        self.thetas = self.get_thetas()
    # =========================================================================

    def get_thetas(self):
        """ Calculates the solution for each hybrid model case """
        thetas = dict()
        for key in self.swh.part_keys:
            if self.cAb.c_vecs[key] is not None:
                c = self.cAb.c_vecs[key]
                A = self.cAb.A_mats[key]
                b = self.cAb.b_vecs[key]
                sol = linprog(c, -A, -b, bounds= (None, None))
                # print(sol)
                thetas[key] = sol.x
            else:
                thetas[key] = None
        return thetas



# Testing
if __name__ == '__main__':
    import pprint as pp
    ag_tst = [4, 4]
    for age in range(2):
        for tst in range(ag_tst[age]):
            dat = fd.FilteredTruckData(age, tst)
            thetas = theta_sat(dat, T_parts=sh.T_hl, T_ord=phiT.T_ord)
            print(dat.name)
            pp.pprint(thetas.thetas)