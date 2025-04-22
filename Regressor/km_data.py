import numpy as np
import math


class km_dat():
    """ Class holding the current and previous data of iod set"""
    # ====================================================
    def __init__(self, iod, k, check_integrity = False):
        if k < 1:
            raise ValueError("No causally preceding data")
        # =====================================
        # ssd at time-step k
        self.y1k = iod['y1'][k]
        self.u1k = iod['u1'][k]
        self.u2k = iod['u2'][k]
        self.Tk  = iod['T'][k]
        self.Fk  = iod['F'][k]
        self.etak = iod['eta'][k]
        # ssd at time-step m = k-1
        self.y1m = iod['y1'][k-1]
        self.u1m = iod['u1'][k-1]
        self.u2m = iod['u2'][k-1]
        self.Tm = iod['T'][k-1]
        self.Fm = iod['F'][k-1]
        self.etam = iod['eta'][k-1]

        # Checking the integrity of eta
        if check_integrity:
            if not self.check_eta_integrity():
                print('eta[k] = {} \n x1[k] = {} \n u1[m] = {}'.format(self.etak, self.x1k, self.u1m))
                print("  diff = {}".format(self.etak - (self.u1m - self.x1k)))
                raise ValueError("Eta integrity check failed!")

    # =====================================================
    def check_eta_integrity(self):
        """ checks if eta has the appropriate definition eta[k] = u1[m] - x1[k]"""
        return math.isclose(np.round(self.etak, 4), np.round((self.u1m - self.x1k), 4), rel_tol= 1e-5)

    # =============================================================================

# Testing
# ========================
if __name__ == '__main__':
    from DataProcessing import filt_data as fd
    dat = fd.FilteredTruckData(0, 0)
    km_data = km_dat(dat.iod, 5, check_integrity = True)
