#!/usr/bin/python3

# CONFIDENTIAL AND PROPRIETARY CODE
# =====================================================================
# Copyright (c) 2025 [Yuan Ming Yu]. All rights reserved.
# This code is confidential and proprietary to [Yuan Ming Yu].
#
# Unauthorized copying, modification, distribution, or disclosure of this
# code is strictly prohibited.
#
# This code is provided "as-is" without any warranty, express or implied.
# Use at your own risk.
#
# For any inquiries regarding usage or licensing, please contact:
# [Contact Information or Legal Team Email]
# =====================================================================
# Author		: Yuan Ming Yu
# Date			: 2025/08/01
# Description	: Read spice netlist into Python object (function only)
# =====================================================================
import re, schemdraw
import schemdraw.elements as elm
import rdnl.core as core
import rdnl.globalvar as gv

# ---------------------------------------------------------------------
# process netlist
# ---------------------------------------------------------------------
def proc_netlist(file_path, tmp_file_path, rowcmt = '*', inline = '$'):
	f = open(tmp_file_path, 'w')
	for line in open(file_path, 'r'):
		if inline in line:
			line = line[:line.index(inline)]
		new_line = line.startswith('+')
		if new_line:
			line = line[1:]
		line = line.strip()
		if line.startswith(rowcmt) or not line:
			continue
		line = re.sub(r'\s+', ' ', line)
		f.write('\n' * (not new_line) + ' ' * new_line + line)
	f.close()

# ---------------------------------------------------------------------
# read subckt line
# ---------------------------------------------------------------------
def rd_subckt_line(words):
	name, ports, attr = words[1], [], {}
	for word in words[2:]: 
		if '=' in word:
			var, val = word.split('=')
			attr[var] = val
		else:
			ports.append(word)
	return name, ports, attr

# ---------------------------------------------------------------------
# read instance line
# ---------------------------------------------------------------------
def rd_inst_line(words):
	name, nets, master, attr = words[0], [], None, {}
	l = len(words)
	for i in range(1, l):
		word = words[i]
		if not master and (i < l - 1 and '=' in words[i + 1] or i == l - 1):
			master = word
		elif '=' in word:
			var, val = word.split('=')
			attr[var] = val
		else:
			nets.append(word)
	return name, nets, master, attr

# ---------------------------------------------------------------------
# parse netlist
# ---------------------------------------------------------------------
def parse_netlist(file_path, orig_file_path):
	subckts = {}
	top_subckt = core.subckt('', [], [], {})
	netlist = core.netlist(orig_file_path, [], top_subckt, [])
	rd_subckt, subckt, subckt_name = False, top_subckt, ''
	for line in open(file_path, 'r'):
		line = line.strip('\n')
		words = line.split()

		# start subckt
		if re.search(r'^\.subckt\s+\w+', line, re.IGNORECASE):
			rd_subckt = True
			subckt_name, subckt_ports, subckt_attr = rd_subckt_line(words)
			subckt = core.subckt(subckt_name, subckt_ports, [], subckt_attr)

		# end subckt
		elif re.search(r'^\.ends\s+' + subckt_name, line, re.IGNORECASE):
			subckt._sort_inst()
			subckts[subckt_name] = subckt
			rd_subckt, subckt, subckt_name = False, top_subckt, ''

		# global
		elif re.search(r'^\.global\s+' + subckt_name, line, re.IGNORECASE):
			netlist.globals += words[1:]

		# instance
		else:
			inst_name, inst_nets, inst_master, inst_attr = rd_inst_line(words)
			fst_char = inst_name[0]
			if fst_char in gv.linear_element:
				inst_attr['val'] = inst_master
				inst_master = gv.linear_element[fst_char]
			inst = core.inst(inst_name, inst_nets, subckt_name, inst_master, inst_attr)
			subckt.insts.append(inst)

	# connect netlist
	top_subckt._sort_inst()
	subckts[''] = top_subckt
	netlist.subckts = subckts.values()
	netlist._sort_subckt()
	for subckt in netlist.subckts:
		for inst in subckt.insts:
			master = netlist.get_subckt(inst.master)
			if master != None:
				inst.master = master
			else:
				inst.is_pri = True
		subckt.netlist = netlist
	return netlist

# ---------------------------------------------------------------------
# get subckt dictionary
# ---------------------------------------------------------------------
def get_subckt_dict(netlist):
	dict = {}
	for subckt in netlist.subckts:
		dict[subckt] = []
		for inst in subckt.insts:
			master = inst.master if inst.is_pri else inst.master.name
			dict[subckt].append(master)
		dict[subckt] = list(dict.fromkeys(dict[subckt]))
	return dict

# ---------------------------------------------------------------------
# line is overlap
# ---------------------------------------------------------------------
def is_overlap(l1xy1, l1xy2, l2xy1, l2xy2):
	l1_xy_max = max(l1xy1, l1xy2)
	l1_xy_min = min(l1xy1, l1xy2)
	l2_xy_max = max(l2xy1, l2xy2)
	l2_xy_min = min(l2xy1, l2xy2)
	if l1_xy_max >= l2_xy_max:
		return l2_xy_max > l1_xy_min
	else:
		return l1_xy_max > l2_xy_min

# ---------------------------------------------------------------------
# line has overlap
# ---------------------------------------------------------------------
def has_overlap(xy1, xy2, xy, line):
	return xy in line and any([is_overlap(xy1, xy2, s, e) for s, e in line[xy]])

# ---------------------------------------------------------------------
# get schemdraw element
# ---------------------------------------------------------------------
def get_schemdraw_elm(name, nmos = None, pmos = None, vcc = None, gnd = None):
	if not nmos: nmos = []
	if not pmos: pmos = []
	if not vcc: vcc = []
	if not gnd: gnd = []
	if name == 'resistor':
		return elm.Resistor()
	elif name == 'capacitor':
		return elm.Capacitor()
	elif name == 'inductor':
		return elm.Inductor()
	elif name == 'voltage':
		return elm.SourceV()
	elif name == 'current':
		return elm.SourceI()
	elif name in nmos:
		return elm.NMos()
	elif name in pmos:
		return elm.PMos()
	elif name in vcc:
		return elm.Vdd()
	elif name in gnd:
		return elm.Ground()

# ---------------------------------------------------------------------
# get schemdraw instance
# ---------------------------------------------------------------------
def get_schemdraw_inst(inst, d, x, y, coords, v_ln, h_ln):
	offset = 0.75
	inst_x = 1.5
	subckt = inst.master
	port_num = len(subckt.ports)
	side_num = int(port_num / 2) + (port_num % 2 > 0)
	dx = (side_num + 1) * inst_x
	dy = (side_num + 1) * offset
	ul = (x, y)
	ll = (x, y - dy)
	ur = (x + dx, y)
	lr = (x + dx, y - dy)
	d.add(elm.Line().linestyle('--').at(ul).to(ur).label(subckt.name, loc = 'bot'))
	d.add(elm.Line().linestyle('--').at(ur).to(lr))
	d.add(elm.Line().linestyle('--').at(lr).to(ll).label(inst.name, loc = 'top'))
	d.add(elm.Line().linestyle('--').at(ll).to(ul))
	if x not in v_ln: v_ln[x] = []
	if (x + dx) not in v_ln: v_ln[x + dx] = []
	if y not in h_ln: h_ln[y] = []
	if (y + dy) not in h_ln: h_ln[y + dy] = []
	v_ln[x].append([y - dy, y])
	v_ln[x + dx].append([y - dy, y])
	h_ln[y].append([x, x + dx])
	h_ln[y + dy].append([x, x + dx])
	for i in range(len(subckt.ports)):
		port = subckt.ports[i]
		left = i % 2 == 0
		net_dy = (i // 2 + 1) * offset
		net_y = dot_y = port_y = y - net_dy
		row = i // 2
		if left:
			net_x = x - offset - row * offset
			dot_x = x - (1/3) * offset
			port_x = x + (1/3) * offset
		else:
			net_x = x + dx + offset + row * offset
			dot_x = x + dx + (1/3) * offset
			port_x = x + dx - (1/3) * offset
		n_coord = (net_x, net_y)
		d_coord = (dot_x, dot_y)
		p_coord = (port_x, port_y)
		if port_y not in h_ln: h_ln[port_y] = []
		h_ln[port_y].append([x - offset, x + dx + offset])
		coords[(inst, i)] = n_coord
		line = elm.Line().at(n_coord).to(p_coord)
		loc = 'right' if left else 'left'
		d.add(elm.Dot().at(d_coord))
		d.add(elm.Line().at(n_coord).to(p_coord).label(port, loc = loc))
	return dx, dy
