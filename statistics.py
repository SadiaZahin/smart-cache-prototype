from matplotlib import mlab
from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt
import numpy as np
from src.utils import read_from_json_file, write_to_json_file
from scipy import interpolate
from src.utils import find_tail_latency




all_latencies = read_from_json_file('./dataset/all_latencies.json')
all_latencies = all_latencies['all_latencies']
d = np.sort(all_latencies)
# Percentile values
p = np.array([0, 20, 50, 75.0, 80, 85, 99])

perc = []
for p1 in p:
    perc.append(np.percentile(d, p1))

#perc = np.percentile(d, p=p)

#plt.plot(d)
# Place red dots on the percentiles
x = (len(d)-1) * p/100
#plt.plot(x, perc, 'ro')

# Set tick locations and labels





all_latencies_only_robinhood = read_from_json_file('./dataset/all_latencies_only_robinhood.json')
all_latencies_only_robinhood = all_latencies_only_robinhood['all_latencies']
d_new = np.sort(all_latencies_only_robinhood)
# Percentile values
p_new = np.array([0, 20, 50, 75.0, 80, 85, 99])

perc_new = []
for p1 in p_new:
    perc_new.append(np.percentile(d_new, p1))

#perc = np.percentile(d, p=p)


#plt.plot(d_new)
# Place red dots on the percentiles
x_1 = (len(d_new)-1) * p_new/100

x_1 = np.array(x_1)

x_new_2 = np.linspace(x_1.min(), x_1.max(), 300)
a_BSpline = interpolate.make_interp_spline(x_1, perc_new)
y_new = a_BSpline(x_new_2)

plt.plot(x_new_2, y_new, 'b-', label='Robinhood')



#plt.show()

x = np.array(x)

x_new = np.linspace(x.min(), x.max(), 300)
a_BSpline = interpolate.make_interp_spline(x, perc)
y_new = a_BSpline(x_new)



plt.plot(x_new, y_new, 'g-', label='Improved solution (Cluster + Robinhood)')
plt.xticks((len(d)-1) * p/100., map(str, p), fontsize=5)
plt.ylabel('Response time (sec)')
plt.xlabel('n-Percentile')
#plt.axvline(x=np.percentile(x_new, 99))
plt.legend()
plt.savefig('comparison_plot_99p.png')
plt.show()
