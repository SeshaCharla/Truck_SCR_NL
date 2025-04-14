import numpy as np
from scipy.io import loadmat
import pathlib as pth
import pickle as pkl
import unit_convs as uc


class RawTruckData():
    """ Class reads the raw-truck data and does the unit-conversions """



    def load_truck_data(self):
        # Load the truck Data
        file_name = truck_dir + "/" + truck_dict[self.name]
        data = loadmat(file_name)
        # Assigning the Data to the variables
        self.raw['t'] = np.array(data['tod']).flatten()
        self.raw['F'] = np.array(data['pExhMF']).flatten()                                       # g/sec
        self.raw['T'] = uc.uConv(np.array(data['pSCRBedTemp']).flatten(), "T250C")      # 250 deg-C
        self.raw['u2'] = np.array(data['pUreaDosing']).flatten()
        self.raw['u1'] = uc.uConv(np.array(data['pNOxInppm']).flatten(), "NOx ppm to mol/m^3")
        self.raw['y1'] = uc.uConv(np.array(data['pNOxOutppm']).flatten(), "NOx ppm to mol/m^3")
        self.gen_iod()
        self.ssd = None
        self.pickle_data()

#