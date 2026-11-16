from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi
#Zusätzliche imports
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.h(qreg_q[2])
circuit.rx(pi, qreg_q[3])
circuit.h(qreg_q[3])
circuit.h(qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[3])
circuit.measure(qreg_q[1], creg_c[1])
circuit.h(qreg_q[0])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.h(qreg_q[2])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[2], creg_c[2])

print(circuit.draw())   # Schaltung als Text im Terminal

# Darstellung der Messungen
counts = AerSimulator().run(circuit, shots=1024).result().get_counts()
print(counts)

circuit.draw("mpl", filename="diagrams/vazirani_circuit.png")   # Schaltung als Bild
plot_histogram(counts, filename="diagrams/vazirani_histogram.png")