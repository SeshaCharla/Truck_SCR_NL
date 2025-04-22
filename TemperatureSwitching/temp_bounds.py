import numpy as np
from DataProcessing import filt_data as fd
from DataProcessing import unit_convs as uc
import switching_handler as sh
from DataProcessing.plotting import *

dct = fd.load_filtered_truck_data_set()
fig_dpi = 300
key = 'T'

lines = (sh.switch_handle(sh.T_hl)).T_parts
ag_tst = [4, 4]
# Plotting all the Data sets
plt.figure()
ax = plt.gca()
for i in range(2):
    for j in range(ag_tst[i]):
        plot_TD(ax, dct[i][j].iod['t'], dct[i][j].iod[key], dct[i][j].iod['t_skips'], label=dct[i][j].name, line_color=tab_lines.__next__())
for line in lines:
    plt.plot(dct[i][j].iod['t'], line * np.ones(np.shape(dct[i][j].iod['t'])), 'k--', linewidth=1)
    plt.text(1300, line+0.2, str((line*10)+200) + r'$\, ^0 C$')
plt.grid()
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel(key + uc.units[key])
plt.title("Temperature plots of Test Cell Data")
plt.savefig("figs/" + "hybrid_ssd_hl_" + key + ".png", dpi=fig_dpi)
plt.show()