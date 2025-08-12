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
import rdnl.func as func

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

	def get_path(self, path):
		'''
		Description:
			Get instance/net path from string path
		Args:
			String path
		Return:
			Instance/net path
		'''
		return self.top_subckt.get_path(self, path)

	def write(self, f, max_len = 80):
		'''
		Description:
			Write netlist into output file
		Args:
			File handler
		Return:
			None
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

	def get_pri_paths(self, net_path):
		'''
		Description:
			Get all primitive paths connected to net path
		Args:
			Net path
		Return:
			Generator of instance paths and terminals
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
		yield from self._get_pri_paths_rcs(subckt, net, path)

	def get_inst_paths(self, subckt_name):
		'''
		Description:
			Get all instance paths from subckt name
		Args:
			Subckt name
		Return:
			Generator of instance paths
		'''
		subckt_dict = func.get_subckt_dict(self)
		yield from self._get_inst_paths_rcs(subckt_name, subckt_dict)

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

	def get_net_path(self, inst_path, term):
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

	def get_net_paths(self, net_path):
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

	def _get_pri_paths_rcs(self, subckt, port, path):
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
						yield from self._get_pri_paths_rcs(inst.master, inst.master.ports[i], path)
						path.pop()

	def _get_inst_paths_rcs(self, subckt_name, dict, path = []):
		if subckt_name == '':
			yield path
		for upper in dict:
			if subckt_name in dict[upper]:
				for inst in upper.insts:
					master = inst.master if inst.is_pri else inst.master.name
					if master == subckt_name:
						yield from self._get_inst_paths_rcs(upper.name, dict, [inst] + path)

	def _sort_subckt(self):
		self.subckts = sorted(self.subckts, key = lambda subckt:subckt.name)

	def _get_pri_paths_rcs(self, subckt, port, path):
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
						yield from self._get_pri_paths_rcs(inst.master, inst.master.ports[i], path)
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
	'''

	def __init__(self, name, ports, insts, attr):
		self.name = name
		self.ports = ports
		self.insts = sorted(insts, key = lambda inst:inst.name)
		self.attr = attr

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
			None
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

	def get_path(self, netlist, path):
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
		path = path.split(netlist.deli)
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
			None
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
