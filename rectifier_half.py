# %% md
# # Half Wave Rectifier
# ## Let's draw the circuit first
# For that I will use schemdraw
# ### v3.0

# %% Draw
import schemdraw
schemdraw.use('svg')
elm=schemdraw.elements
d=schemdraw.Drawing()
d+=elm.Ground()
d+=elm.SourceSin().reverse().up()
d+=(dio:=elm.Diode()).right()
d+=elm.Line(unit=1)
d+=elm.Resistor().down().label('$R_L$', loc='bottom')

# %% unfiltered
uf=schemdraw.Drawing(file='rectifier_half_ckt.svg', backend='svg')
uf+=elm.ElementDrawing(d)
uf+=elm.Line(unit=4).left()
uf.draw()

# %% with capacitor filter
f=schemdraw.Drawing(file='rectifier_half_c_ckt.svg', backend='svg')
f+=elm.ElementDrawing(uf)
f+=elm.Capacitor().down().at(dio.end)
f.draw()

# %% with inductor capacitor filter
lf=schemdraw.Drawing(file='rectifier_half_lc_ckt.svg', backend='svg')
lf+=elm.ElementDrawing(d)
lf+=elm.Inductor(unit=1).left()
lf+=elm.Line()
lf+=elm.Capacitor().down().at(dio.end)
lf.draw()

# %% md
# ## Now the simulation
# For this I will use PySpice

# %% import
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# %% setup
logger = Logging.setup_logging()

# %% ckt
ckt = Circuit("Half Wave Rectifier")
ckt.include('../model_library/diode.lib')
source=ckt.SinusoidalVoltageSource('input', 'input', ckt.gnd, amplitude=5@u_V, frequency=50@u_Hz)
ckt.D('', 'input', 'load', model='1N4148')
ckt.R('l', 'load', ckt.gnd, 100@u_Ohm)

# %% simulate
simulator = ckt.simulator()
analysis = simulator.transient(step_time=source.period/200, end_time=source.period*5)

# %% c filter
ckt.C('f', 'load', ckt.gnd, 1.25@u_mF)

# %% simulate c filter
simulator = ckt.simulator()
cfanalysis = simulator.transient(step_time=source.period/200, end_time=source.period*5)

# %% lc filter
ckt.Rl.detach()
ckt.L('f', 'load', 'loadr', 1.25@u_H)
ckt.R('', 'loadr', ckt.gnd, 100@u_Ohm)

# %% simulate lc filter
simulator = ckt.simulator()
lcfanalysis = simulator.transient(step_time=source.period/200, end_time=source.period*5)

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
ax.plot(analysis.load, label='unfiltered output')
ax.plot(cfanalysis.load, label='C filtered output')
ax.plot(lcfanalysis.loadr, label='LC filtered output')
plt.legend()
plt.show()
plt.savefig('rectifier_half_plt.svg')
