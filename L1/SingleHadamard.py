from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi
#Zusätzliche imports
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.rz(pi / 2, qreg_q[0])
circuit.sx(qreg_q[0])
circuit.rz(pi / 2, qreg_q[0])
circuit.rz(pi / 2, qreg_q[1])
circuit.sx(qreg_q[1])
circuit.rz(pi / 2, qreg_q[1])
circuit.cz(qreg_q[0], qreg_q[1])
circuit.rz(pi / 2, qreg_q[1])
circuit.sx(qreg_q[1])
circuit.rz(pi / 2, qreg_q[1])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])

print(circuit.draw())   # Schaltung als Text im Terminal

# Darstellung der Messungen
counts = AerSimulator().run(circuit, shots=1024).result().get_counts()
print(counts)

circuit.draw("mpl", filename="diagrams/hadamard_circuit.png")   # Schaltung als Bild
plot_histogram(counts, filename="diagrams/hadamard_histogram.png")