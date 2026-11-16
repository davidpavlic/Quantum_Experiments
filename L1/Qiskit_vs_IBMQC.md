# Fazit: Simulator vs. echte Hardware

## Durchgeführte Experimente

* **Bell-Schaltung (H auf q0, CNOT q0 → q1, Messung)**
   * Simulator (Composer-Visualisierung): exakt 50 % `00` und 50 % `11`
   * Hardware: `ibm_fez`, 1024 Shots, Region us-east, Job `dbtkh4uhrjis73e7cdv0`
   * Ergebnis Hardware: mehrheitlich `00` und `11`, zusätzlich ein kleiner Anteil `01` und `10`, die es theoretisch gar nicht geben dürfte
* **Bernstein-Vazirani mit s = 101**
   * Nur simuliert, nicht auf Hardware ausgeführt
   * Simulation (AerSimulator, 1024 Shots): `{'0101': 1024}`, also s = 101 mit 100 %
   * Lesson learned: Eine erste Composer-Version hatte `RX(π/2)` statt `X` auf der Ancilla. Ergebnis war 50 % `0000` und 50 % `0101`, weil die Ancilla nicht sauber in |−⟩ lag. Das war ein Bau-, kein Hardwarefehler

## Unterschiede und wahrscheinliche Ursachen

### 1. Backend-Wahl

* Der Simulator rechnet die Mathematik exakt auf einem klassischen Computer, also **ohne Rauschen**
* Ein echter QPU ist verrauscht. Die wichtigsten Fehlerquellen:
   * **Gate-Fehler:** vor allem das Zwei-Qubit-Gate (CNOT) erreicht den Zielzustand nur fast
   * **Readout-Fehler:** eine 1 wird als 0 gelesen oder umgekehrt, so wird aus `11` ein `10` oder `01`
   * **Dekohärenz:** |1⟩ zerfällt mit der Zeit von selbst zu |0⟩
   * **Crosstalk:** benachbarte Qubits stören sich gegenseitig
* Fehlerraten unterscheiden sich je nach QPU und Qubit und ändern sich mit jeder Kalibrierung (siehe «View calibration history»)
* → Die `01`/`10`-Ergebnisse auf `ibm_fez` sind Hardware-Rauschen, kein Fehler in der Schaltung

### 2. Shot-Anzahl

* Auch ein ideales 50/50 liefert bei endlich vielen Shots nicht exakt 512/512
* Standardabweichung: $\sigma = \sqrt{N \cdot p \cdot (1-p)} = \sqrt{1024 \cdot 0.5 \cdot 0.5} = \sqrt{256} = 16$ Shots
* Typische Schwankung also etwa 496 bis 528 Shots, das sind ±1.6 %
* Beispiel-Lauf im AerSimulator: `{'11': 504, '00': 496}`, liegt innerhalb dieser Schwankung
* Mehr Shots verkleinern die relative Schwankung (sie sinkt mit $1/\sqrt{N}$)
* Die Composer-Visualisierung zeigt dagegen exakte Wahrscheinlichkeiten (Statevector), ganz ohne Shot-Schwankung

### 3. Transpilation

* Der QPU kennt nur seine nativen Gates (z. B. CZ plus Einzelqubit-Rotationen). Ein CNOT wird vor dem Ausführen in diese Gates übersetzt
* Die logischen Qubits werden auf physische Qubits des Chips abgebildet (Layout). Sind sie nicht direkt verbunden, kommen SWAP-Gates dazu
* Mehr Gates bedeuten mehr Fehlerquellen. Die übersetzte Schaltung ist deshalb meist länger als die im Composer gebaute

### 4. Bit-Reihenfolge in der Anzeige

* Qiskit und der Composer zeigen Bitstrings als `c[n-1] … c[1] c[0]`, also **q0 ganz rechts**
* Der Composer hat standardmässig 4 klassische Bits. Ungenutzte Bits erscheinen als führende Nullen: `0001` bedeutet c0 = 1 und c1 = 0
* In Lehrbuch-Notation (q0 links) wäre `0001` also der Zustand |10⟩. Bei `01` und `10` vertauschen sich je nach Konvention die Labels
* Beim Bell-Zustand (`00`, `11`) und bei s = 101 fällt das nicht auf, weil beide vorwärts und rückwärts gleich sind
* Auch die Vorlesungsfolien mischen beide Konventionen (z. B. «CNOT|0+⟩»)

## Kernerkenntnisse

* Simulator = ideale Mathematik, Hardware = Mathematik plus Rauschen
* Kleine Anteile «unmöglicher» Ergebnisse auf echter Hardware sind normal
* Vor dem Ausführen auf Hardware die Schaltung immer im Simulator prüfen. Weicht schon der Simulator ab, liegt der Fehler in der Schaltung
* Bitstrings in Qiskit von rechts nach links lesen
