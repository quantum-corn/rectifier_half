# %% md
# # Half Wave Rectifier
# ## Let's draw the circuit first
# For that I will use schemdraw
# ### v1.0

# %% Draw
import schemdraw
schemdraw.use('svg')
elm=schemdraw.elements
d=schemdraw.Drawing(file='rectifier_half_ckt.svg')
d+=elm.SourceSin().reverse().up()
d+=elm.Line().right()
d+=elm.Diode().down()
d+=elm.Line().left()
d+=elm.Ground()
d.draw()

# %% md
# ## Now the simulation
# For this I will use PySpice

# %% import
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# %% setup
logger = Logging.setup_logging()

# %% circuit
circuit = Circuit("Half Wave Rectifier")
circuit.include('../model_library/diode.lib')
source=circuit.SinusoidalVoltageSource('input', 'input', circuit.gnd, amplitude=5@u_V, frequency=50@u_Hz)
circuit.D('', 'input', 'R', model='1N4148')
circuit.R('', 'R', circuit.gnd, 100@u_Ohm)

# %% simulate
simulator = circuit.simulator()
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*2)

# %% md
# ### Now let's plot the data
# For this I will use matplotlib

# %% import
import matplotlib.pyplot as plt

# %% plot data
fig, ax=plt.subplots()
ax.set(title="Half Wave Rectifier", ylabel='Voltage in V', xlabel='Time in x0.1 ms')
ax.grid()
ax.axhline(y=0, color='black')
ax.axvline(x=0, color='black')
ax.plot(analysis.input, label='input')
ax.plot(analysis.R, label='output')
plt.legend()
plt.show()
plt.savefig('rectifier_half_plt.svg')
