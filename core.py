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
# Description	: Read spice netlist into Python object (core class only)
# =====================================================================
import schemdraw
import schemdraw.elements as elm
import rdnl.func as func
import rdnl.globalvar as gv

# ---------------------------------------------------------------------
# Class: netlist
# ---------------------------------------------------------------------
class netlist():
	'''
	Description:
		Netlist from top-level subckt to lower-level instances
	Props:
		path		: Netlist absolute file path
		globals		: Global powers
		top_subckt	: Top-level subckt
		subckts		: All netlist subckts
		deli		: Hierarchy delimiter
	'''

	def __init__(self, path, globals, top_subckt, subckts):
		self.path = path
		self.globals = globals
		self.top_subckt = top_subckt
		self.deli = '.'
		self.subckts = sorted(subckts, key = lambda subckt:subckt.name)
		self.vcc = ['vcc', 'vdd']
		self.gnd = ['gnd', 'vss']
		self.nmos = ['nmos']
		self.pmos = ['pmos']
		self.linear = ['resistor', 'capacitor', 'inductor', 'voltage', 'current']

	def __repr__(self):
		return self.path

	def get_str_path(self, path):
		'''
		Description:
			Get string path from instance/net path
		Args:
			Instance/net path
		Return:
			String path
		'''
		return self.deli.join([str(i) for i in path])

	def get_subckt(self, name):
		'''
		Description:
			Get subckt from subckt name
		Args:
			Subckt name
		Return:
			Subckt
		'''
		l = 0
		r = len(self.subckts) - 1
		while l <= r:
			m = round((r - l) / 2) + l
			if self.subckts[m].name == name:
				return self.subckts[m]
			elif self.subckts[m].name >= name:
				r = m - 1
			else:
				l = m + 1
		return None

	def get_path_from_str(self, path):
		'''
		Description:
			Get instance/net path from string path
		Args:
			String path
		Return:
			Instance/net path
		'''
		return self.top_subckt.get_path_from_str(path)

	def write(self, f, max_len = 80):
		'''
		Description:
			Write netlist into output file
		Args:
			File handler
		Return:
		'''
		if self.globals:
			f.write('.global ' + ' '.join(self.globals) + '\n\n')
		for subckt in self.subckts[1:]:
			subckt.write(f)
			f.write('\n')
		for inst in self.top_subckt.insts:
			inst.write(f)

	def get_top_path(self, net_path):
		'''
		Description:
			Get top-level net path
		Args:
			Net path
		Return:
			Net path
		'''
		up_net_path = self.get_up_path(net_path)
		if not net_path or not isinstance(net_path[-1], str):
			return []
		elif not up_net_path:
			return net_path
		else:
			return self.get_top_path(up_net_path)

	def get_up_path(self, net_path):
		'''
		Description:
			Get upper-level net path
		Args:
			Net path
		Return:
			Net path
		'''
		if len(net_path) <= 1:
			return []
		net = net_path[-1]
		inst = net_path[-2]
		subckt = inst.master
		for i in range(len(subckt.ports)):
			if net == subckt.ports[i]:
				return net_path[:-2] + [inst.nets[i]]
		return []

	def get_net_to_pri_paths(self, net_path):
		'''
		Description:
			Get all primitive paths and terminals connected to net path
		Args:
			Net path
		Return:
			Generator of primitive paths and terminals
		'''
		top_net_path = self.get_top_path(net_path)
		if not top_net_path:
			return
			yield
		else:
			l = len(top_net_path)
			subckt = self.top_subckt if l == 1 else top_net_path[-2].master
			net = top_net_path[-1]
			path = top_net_path[:-1]
		yield from self._get_net_to_pri_paths_rcs(subckt, net, path)

	def get_subckt_inst_paths(self, subckt_name):
		'''
		Description:
			Get all instance paths from subckt name
		Args:
			Subckt name
		Return:
			Generator of instance paths
		'''
		subckt_dict = func.get_subckt_dict(self)
		yield from self._get_subckt_inst_paths_rcs(subckt_name, subckt_dict)

	def is_same_net(self, net_path_1, net_path_2):
		'''
		Description:
			Check if two nets are same node
		Args:
			Net path
			Net path
		Return:
			Boolean
		'''
		top_net_path_1 = self.get_top_path(net_path_1)
		top_net_path_2 = self.get_top_path(net_path_2)
		return top_net_path_1 == top_net_path_2

	def get_net_path_at_term(self, inst_path, term):
		'''
		Description:
			Get net path connected to instance terminal
		Args:
			Instance path
			Terminal
		Return:
			Net path
		'''
		if not inst_path:
			return []
		else:
			return inst_path[:-1] + [inst_path[-1].nets[term]]

	def get_hier_net_paths(self, net_path):
		'''
		Description:
			Get all net paths across hierarchy on same node
		Args:
			Net path
		Return:
			Generator of net paths
		'''
		top_net_path = self.get_top_path(net_path)
		if not top_net_path:
			return
			yield
		else:
			l = len(top_net_path)
			subckt = self.top_subckt if l == 1 else top_net_path[-2].master
			net = top_net_path[-1]
			path = top_net_path[:-1]
		yield from self._get_net_paths_rcs(subckt, net, path)

	def short_by_term(self, master, terms):
		'''
		Description:
			Short instance master on all specified terminals
		Args:
			Master name
			Terminals
		Return:
		'''
		for subckt in self.subckts:
			nets = []
			for inst in list(subckt.insts):
				if str(inst.master) == master:
					nets += [inst.nets[t] for t in terms]
					subckt.insts.remove(inst)
			if nets:
				win_net = self._get_win_net(nets)
				for inst in subckt.insts:
					for i in range(len(inst.nets)):
						if inst.nets[i] in nets:
							inst.nets[i] = win_net

	def get_net_to_inst_paths(self, net_path, masters):
		'''
		Description:
			Get all instance/primitive paths and terminals connected
			to net path with specified masters
		Args:
			Net path
			Master names
		Return:
			Generator of instance/primitive paths and terminals
		'''
		top_net_path = self.get_top_path(net_path)
		if not top_net_path:
			return
			yield
		else:
			l = len(top_net_path)
			subckt = self.top_subckt if l == 1 else top_net_path[-2].master
			net = top_net_path[-1]
			path = top_net_path[:-1]
		yield from self._get_net_to_inst_paths_rcs(subckt, net, path, masters)

	def _get_net_to_inst_paths_rcs(self, subckt, port, path, masters):
		for inst in subckt.insts:
			l = len(inst.nets)
			if str(inst.master) in masters:
				terms = []
				for i in range(l):
					if inst.nets[i] == port:
						terms.append(i)
				if terms:
					yield path + [inst], terms
			elif not inst.is_pri:
				for i in range(l):
					if inst.nets[i] == port:
						path.append(inst)
						yield from self._get_net_to_inst_paths_rcs(inst.master, inst.master.ports[i], path, masters)
						path.pop()

	def _get_win_net(self, nets):
		globals = [net for net in nets if net in self.globals]
		if globals:
			return max(globals)
		else:
			return max(nets)

	def _get_net_paths_rcs(self, subckt, port, path):
		yield path + [port]
		for inst in subckt.insts:
			if not inst.is_pri:
				l = len(inst.nets)
				for i in range(l):
					if inst.nets[i] == port:
						path.append(inst)
						yield from self._get_net_paths_rcs(inst.master, inst.master.ports[i], path)
						path.pop()

	def _get_net_to_pri_paths_rcs(self, subckt, port, path):
		for inst in subckt.insts:
			l = len(inst.nets)
			if inst.is_pri:
				terms = []
				for i in range(l):
					if inst.nets[i] == port:
						terms.append(i)
				if terms:
					yield path + [inst], terms
			else:
				for i in range(l):
					if inst.nets[i] == port:
						path.append(inst)
						yield from self._get_net_to_pri_paths_rcs(inst.master, inst.master.ports[i], path)
						path.pop()

	def _get_subckt_inst_paths_rcs(self, subckt_name, dict, path = []):
		if subckt_name == '':
			yield path
		for upper in dict:
			if subckt_name in dict[upper]:
				for inst in upper.insts:
					master = inst.master if inst.is_pri else inst.master.name
					if master == subckt_name:
						yield from self._get_subckt_inst_paths_rcs(upper.name, dict, [inst] + path)

	def _sort_subckt(self):
		self.subckts = sorted(self.subckts, key = lambda subckt:subckt.name)

	def _get_net_to_pri_paths_rcs(self, subckt, port, path):
		for inst in subckt.insts:
			l = len(inst.nets)
			if inst.is_pri:
				terms = []
				for i in range(l):
					if inst.nets[i] == port:
						terms.append(i)
				if terms:
					yield path + [inst], terms
			else:
				for i in range(l):
					if inst.nets[i] == port:
						path.append(inst)
						yield from self._get_net_to_pri_paths_rcs(inst.master, inst.master.ports[i], path)
						path.pop()

# ---------------------------------------------------------------------
# Class: subckt
# ---------------------------------------------------------------------
class subckt():
	'''
	Description:
		Subckt with ports and instances
	Props:
		name		: Subckt name
		ports		: Subckt ports
		insts		: All instances under subckt
		attr		: Subckt attributes
		netlist		: Netlist
	'''

	def __init__(self, name, ports, insts, attr):
		self.name = name
		self.ports = ports
		self.insts = sorted(insts, key = lambda inst:inst.name)
		self.attr = attr
		self.netlist = None

	def __repr__(self):
		return self.name

	def get_inst(self, name):
		'''
		Description:
			Get instance from instance name
		Args:
			Instance name
		Return:
			Instance
		'''
		l = 0
		r = len(self.insts) - 1
		while l <= r:
			m = round((r - l) / 2) + l
			if self.insts[m].name == name:
				return self.insts[m]
			elif self.insts[m].name >= name:
				r = m - 1
			else:
				l = m + 1
		return None

	def write(self, f):
		'''
		Description:
			Write subckt into output file
		Args:
			File handler
		Return:
		'''
		line = f'.subckt {self.name}'
		for port in self.ports:
			line += ' ' + port
		for var in self.attr:
			line += ' ' + var + '=' + self.attr[var]
		f.write(line + '\n')
		for inst in self.insts:
			inst.write(f)
		f.write('.ends ' + self.name + '\n')

	def get_path_from_str(self, path):
		'''
		Description:
			Get instance/net path under subckt from string path
		Args:
			String path
		Return:
			Instance/net path
		'''
		subckt = self
		inst_path = []
		path = path.split(self.netlist.deli)
		for hier in path:
			inst = subckt.get_inst(hier)
			if inst:
				inst_path.append(inst)
				subckt = inst.master
			elif subckt.has_net(hier):
				inst_path.append(hier)
				break
			else:
				break
		return inst_path if len(inst_path) == len(path) else []

	def has_net(self, net):
		'''
		Description:
			Check if subckt has net
		Args:
			Net name
		Return:
			Boolean
		'''
		for inst in self.insts:
			if net in inst.nets:
				return True
		return False

	def replace_net(self, master_net, slave_net):
		'''
		Description:
			Replace subckt slave net by master net
		Args:
			Net name (master)
			Net name (slave)
		Return:
		'''
		for inst in self.insts:
			for i in range(len(inst.nets)):
				if inst.nets[i] == slave_net:
					inst.nets[i] = master_net

	def show(self, scale = 2.5, offset = 0.5, save_path = None):
		'''
		Description:
			Show subckt connectivity
		Args:
			Scale of instance placement
			Offset of net connection detour
		Return:
		'''
		d = schemdraw.Drawing()
		nets, coords, h_ln, v_ln = [], {}, {}, {}
		curr_x, curr_y, port_y, global_y = scale * 1.5, 0, 0, scale * 0.5
		vcc, gnd = self.netlist.vcc, self.netlist.gnd
		nmos, pmos = self.netlist.nmos, self.netlist.pmos
		d.add(elm.Label().label(f'subckt:{self.name}').at((0, -scale * 0.5)))
		for inst in self.insts:
			master = inst.master if inst.is_pri else inst.master.name
			master = master.lower()
			if master in nmos + pmos:
				is_nmos = master in nmos
				dev = func.get_schemdraw_elm(master, nmos, pmos)
				dev.right().at((curr_x, curr_y))
				dev.label(inst.name, loc = 'right')
				d.add(dev)
				coords[(inst, 0)] = dev.drain if is_nmos else dev.source
				coords[(inst, 1)] = dev.gate
				coords[(inst, 2)] = dev.source if is_nmos else dev.drain
				x, y = dev.drain[0], dev.gate[1]
				if x not in v_ln: v_ln[x] = []
				if y not in h_ln: h_ln[y] = []
				v_ln[x].append([dev.source[1], dev.drain[1]])
				h_ln[y].append([dev.gate[0], dev.drain[0]])
			elif any([master == i for i in self.netlist.linear]):
				dev = func.get_schemdraw_elm(master)
				value = inst.attr['val']
				dev.right().at((curr_x, curr_y))
				dev.label(inst.name, loc = 'top')
				dev.label(value, loc = 'bottom')
				d.add(dev)
				coords[(inst, 0)] = dev.end
				coords[(inst, 1)] = dev.start
				y = dev.start[1]
				if y not in h_ln: h_ln[y] = []
				h_ln[y].append([dev.start[0], dev.end[0]])
			else:
				dx, dy = func.get_schemdraw_inst(inst, d, curr_x, curr_y, coords, v_ln, h_ln)
				curr_x += dx
				curr_y += dy
			if curr_y >= (len(self.ports) - 1) * scale:
				curr_x += scale
				curr_y = 0
			else:
				curr_y += scale
		net_to_inst = self._get_net_to_inst()
		for net in net_to_inst:
			net_low = net.lower()
			s_node = net_to_inst[net][0]
			s_coord = coords[s_node]
			if net in self.ports and net not in nets:
				l_coord = (0, port_y)
				d.add(elm.Line(label = net).at((-scale * 0.5, port_y)).to(l_coord))
				if port_y not in h_ln: h_ln[port_y] = []
				h_ln[port_y].append([-scale * 0.5, 0])
				self._conn_node(d, l_coord, s_coord, h_ln, v_ln, offset)
				nets.append(net)
				port_y += scale
			if any([i == net_low for i in vcc + gnd]):
				is_vcc = any([i == net_low for i in vcc])
				global_x = scale * 0.5
				r_coord = (global_x, global_y)
				rail = func.get_schemdraw_elm(net_low, vcc = vcc, gnd = gnd)
				rail.right().at(r_coord)
				rail.label(net, loc = 'top')
				d.add(rail)
				if global_x not in v_ln: v_ln[global_x] = []
				y_diff = 0.5 if is_vcc else -0.5
				v_ln[global_x].append([global_y, global_y + y_diff])
				self._conn_node(d, s_coord, r_coord, h_ln, v_ln, offset)
				global_y += scale
			for e_node in net_to_inst[net][1:]:
				e_coord = coords[e_node]
				self._conn_node(d, s_coord, e_coord, h_ln, v_ln, offset, coords, s_node)
				s_coord = coords[s_node]
		if save_path:
			d.save(save_path)
		else:
			d.draw()

	def _conn_node(self, d, start, end, h_ln, v_ln, offset = 0.5, coords = None, node = None):
		count = 0
		x1, y1 = start
		x2, y2 = end
		while True:
			overlap = False
			if count >= 10: break
			if func.has_overlap(x1, x2, y1, h_ln):
				overlap = True
				if not func.has_overlap(y1, y1 + offset, x1, v_ln):
					d.add(elm.Line().at((x1, y1)).to((x1, y1 + offset)))
					if x1 not in v_ln: v_ln[x1] = []
					v_ln[x1].append([y1, y1 + offset])
					y1 += offset
				else:
					offset *= -1.1
			if func.has_overlap(y1, y2, x2, v_ln):
				overlap = True
				if not func.has_overlap(x2, x2 + offset, y2, h_ln):
					d.add(elm.Line().at((x2, y2)).to((x2 + offset, y2)))
					if y2 not in h_ln: h_ln[y2] = []
					h_ln[y2].append([x2, x2 + offset])
					x2 += offset
				else:
					offset *= -1.1
			if not overlap:
				break
			count += 1
		d.add(elm.Line().at((x1, y1)).to((x2, y1)))
		d.add(elm.Line().at((x2, y1)).to((x2, y2)))
		d.add(elm.Dot().at((x1, y1)))
		if x2 not in v_ln: v_ln[x2] = []
		if y1 not in h_ln: h_ln[y1] = []
		v_ln[x2].append([y1, y2])
		h_ln[y1].append([x1, x2])
		if node:
			coords[node] = (x1, y1)

	def _get_net_to_inst(self):
		net_to_inst = {}
		for inst in self.insts:
			for i in range(len(inst.nets)):
				net = inst.nets[i]
				if str(inst.master) in ['NMOS', 'PMOS'] and i == 3: continue
				if net not in net_to_inst:
					net_to_inst[net] = []
				net_to_inst[net].append((inst, i))
		return net_to_inst

	def _sort_inst(self):
		self.insts = sorted(self.insts, key = lambda inst:inst.name)

# ---------------------------------------------------------------------
# Class: inst
# ---------------------------------------------------------------------
class inst():
	'''
	Description:
		Instance with nets and master
	Props:
		name		: Instance name
		nets		: Instance nets
		subckt		: Subckt containing the instance
		master		: Subckt that is instantiated
		attr		: Instance attributes
		is_pri		: Instance is primitive
	'''

	def __init__(self, name, nets, subckt, master, attr):
		self.name = name
		self.nets = nets
		self.subckt = subckt
		self.master = master
		self.attr = attr
		self.is_pri = False

	def __repr__(self):
		return self.name

	def write(self, f):
		'''
		Description:
			Write instance into output file
		Args:
			File handler
		Return:
		'''
		line = self.name
		for net in self.nets:
			line += ' ' + net
		master = self.attr['val'] if 'val' in self.attr else str(self.master)
		line += ' ' + master
		for var in self.attr:
			if var == 'val': continue
			line += ' ' + var + '=' + self.attr[var]
		f.write(line + '\n')
