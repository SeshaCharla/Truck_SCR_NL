import numpy as np
from DataProcessing import filt_data as fd
from TemperatureSwitching import switching_handler as sh
from Regressor import phiT
from Regressor import km_data


class cAb_mats():
    """
        Container for the cost and constraint matrices for the linear program under various temperature bounds
    """
    def __init__(self, f_dat: fd.FilteredTruckData,  T_parts:list, T_ord:dict) -> None:
        self.dat = f_dat
        self.t_skips = f_dat.iod['t_skips']
        self.T_ord = T_ord
        self.swh = sh.switch_handle(T_parts)
        self.Nparms = self.T_ord['Gamma'] + 1
        self.T = self.dat.iod['T']
        self.data_len = len(self.T)
        self.row_len = self.get_row_len()
        self.b_vecs = self.get_b_eta()
        self.A_mats = self.get_A_mats()
        self.c_vecs = self.get_c()

    # ==================================================================================================================
    def get_interval_k(self, k) -> str:
        """ Get the interval of the kth time step """
        key = self.swh.get_interval_T(self.T[k])
        return key
    # ==================================================================================================================

    def get_row_len(self) -> dict[str, int]:
        """ The row length of each of the regression matrices of the switched system """
        mat_sizes = dict()
        for key_T in self.swh.part_keys:
            mat_sizes[key_T] = 0
        for l in range(len(self.t_skips)-1):
            for k in range(self.t_skips[l], self.t_skips[l+1] -1):
                key = self.get_interval_k(k)
                mat_sizes[key] += 1
        return mat_sizes
    # ==================================================================================================================

    def get_b_eta(self) -> dict[str, np.ndarray]:
        """ Returns a dictionary of b vectors for each of the partitions """
        # Creating the dictionary with zero matrices ============================================
        b_vecs = dict()
        for key_T in self.swh.part_keys:
            if self.row_len[key_T] == 0:
                b_vecs[key_T] = None
            else:
                b_vecs[key_T] = np.zeros(self.row_len[key_T])
        # ========================================================================================
        irc = dict()     # interval row counter
        for key_T in self.swh.part_keys:
            irc[key_T] = 0
        for l in range(len(self.t_skips) - 1):
            for k in range(self.t_skips[l], self.t_skips[l+1] - 1):
                key_T = self.get_interval_k(k)
                b_vecs[key_T][irc[key_T]] = self.dat.iod['eta'][k+1]
                irc[key_T] += 1
        return b_vecs
    # ==================================================================================================================

    def get_A_mats(self) -> dict[str, np.ndarray]:
        """ Returns a dictionary of A matrices for each of the partitions """
        # Creating a dictionary with zero matrices
        A_mats = dict()
        for key_T in self.swh.part_keys:
            if self.row_len[key_T] == 0:
                A_mats[key_T] = None
            else:
                A_mats[key_T] = np.zeros([self.row_len[key_T], self.Nparms])
        # ==========================================================================
        irc = dict()
        for key_T in self.swh.part_keys:
            irc[key_T] = 0
        for l in range(len(self.t_skips) - 1):
            for k in range(self.t_skips[l], self.t_skips[l+1] - 1):
                key_T = self.get_interval_k(k)
                u1_k = self.dat.iod['u1'][k]
                F_k = self.dat.iod['F'][k]
                T_k = self.dat.iod['T'][k]
                A_mats[key_T][irc[key_T], :] = (u1_k/F_k) * (phiT.phi_T(T_k, self.T_ord['Gamma'])).flatten()
                irc[key_T] += 1
        return A_mats
    # ==================================================================================================================

    def get_c(self) -> dict[str, np.ndarray]:
        """ Returns the c vectors for the linear programming """
        c_vecs = dict()
        for key in self.swh.part_keys:
            if self.A_mats[key] is not None:
                c_vecs[key] = np.sum(self.A_mats[key], axis=0)
            else:
                c_vecs[key] = None
        return c_vecs


# Testing
if __name__ == "__main__":
    import pprint
    cAb = cAb_mats(fd.FilteredTruckData(0, 0), T_parts=sh.T_hl, T_ord=phiT.T_ord)
    pprint.pprint(cAb.b_vecs)
    pprint.pprint(cAb.c_vecs)
    pprint.pprint(cAb.A_mats)
