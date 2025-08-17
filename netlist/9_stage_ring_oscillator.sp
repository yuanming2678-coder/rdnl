********************************************
* CMOS Inverter Subckt
********************************************
* .SUBCKT INV in out vdd gnd Wn=..., Wp=..., L=...
.SUBCKT INV IN OUT VDD GND Wn=1u Wp=2u L=0.18u
M1 OUT IN GND GND NMOS W={Wn} L={L}
M2 OUT IN VDD VDD PMOS W={Wp} L={L}
r1 OUT GND 1k
c1 OUT GND 1f
l1 OUT GND 1n
v1 OUT GND 2.2
i1 OUT GND 1n
.ENDS INV

********************************************
* 9-Stage Ring Oscillator
********************************************
.SUBCKT RINGOSC9 VDD GND OUT Wn=1u Wp=2u L=0.18u
* Internal nodes
* OUT is connected to stage1 output (Node1)
*
* Nodes: N1 \u2192 N2 \u2192 ... \u2192 N9 \u2192 N1
*
X1  N1 N2 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X2  N2 N3 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X3  N3 N4 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X4  N4 N5 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X5  N5 N6 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X6  N6 N7 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X7  N7 N8 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X8  N8 N9 VDD GND INV Wn={Wn} Wp={Wp} L={L}
X9  N9 N1 VDD GND INV Wn={Wn} Wp={Wp} L={L}

* Output tap
EOUT OUT 0 N1 0 1
.ENDS RINGOSC9

XRO VDD GND OUT RINGOSC9 Wn=0.5u Wp=1u L=0.18u
