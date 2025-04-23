from typing import Any

import numpy as np
from SatSys import theta_sat as ths
from DataProcessing import filt_data as fd
from TemperatureSwitching import switching_handler as sh
from Regressor import phiT


class sat_eta:
    """ Class simulating the saturated system """
    def __init__(self, f_dat: fd.FilteredTruckData, T_parts: list, T_ord: dict) -> None:
        """ Loads the data and generates the simulation of the saturated system """
        self.dat = f_dat
        self.T_ord = T_ord
        self.T_parts = T_parts
        self.theta_sat = ths.theta_sat(self.dat, self.T_parts, self.T_ord)
        self.swh = self.theta_sat.swh
        self.data_len = self.theta_sat.cAb.data_len
        self.eta_sim = self.sim_eta()
        self.str_frac = self.dat.iod['eta']/self.eta_sim

    # ===============================================================================

    def phi_sat(self, k:int) -> np.ndarray:
        """ Calculates the phi(k) for getting the eta(k+1) """
        u1_k = self.dat.iod['u1'][k]
        F_k = self.dat.iod['F'][k]
        T_k = self.dat.iod['T'][k]
        phi_k = phiT.phi_T(T_k, self.T_ord['Gamma'])
        return (u1_k/F_k)*phi_k
    # ============================================================

    def sim_eta(self) -> np.ndarray:
        """ Simulate the eta from data """
        eta_sim = np.zeros(self.data_len)
        for k in range(self.data_len-1):
            key_T = self.swh.get_interval_T(self.dat.iod['T'][k])
            eta_sim[k+1] = ((self.phi_sat(k)).T @ self.theta_sat.thetas[key_T])[0, 0]
        eta_sim[0] = eta_sim[1]
        return eta_sim
    # =================================================================================================

# Testing
if __name__ == "__main__":
    import pprint as pp
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('TkAgg')
    from DataProcessing import unit_convs as uc

    ag_tst = [4, 4]

    for age in range(2):
        for test in range(ag_tst[age]):
            dat = fd.FilteredTruckData(age, test)
            sim = sat_eta(dat, T_parts=sh.T_n, T_ord=phiT.T_ord)

            plt.figure()
            plt.plot(dat.iod['t'], dat.iod['eta'], label='eta from data set')
            plt.plot(dat.iod['t'], sim.eta_sim, label='eta_saturated')
            plt.plot(dat.iod['t'], dat.iod['F'], '--', label='F '+uc.units['F'])
            plt.legend()
            plt.grid()
            plt.title(dat.name)
            plt.xlabel('t [s]')
            plt.ylabel('eta' + uc.units['eta'])
            plt.savefig("figs/eta_bounds_"+dat.name+".png")

    plt.show()

# plt.figure()
# plt.plot(dat.ssd['t'], sim.str_frac, label="Storage fraction")
# plt.legend()
# plt.grid()
# plt.title(dat.name)
# plt.xlabel('t [s]')
# plt.ylabel('Storage fraction (ratio)')
