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
# Description	: Read spice netlist into Python object (testing)
# =====================================================================
import sys, os, time, copy, tracemalloc, subprocess as sp
sys.path.append('../..')
import rdnl

time_start = time.time()
tracemalloc.start()
netlist_path = '../netlist/alu4_logic_netlist.sp'
netlist = rdnl.api.rd_netlist(netlist_path)
os.system('rm -rf out')
os.makedirs('out')

# subckt
subckt_name = 'XOR2'
subckt = netlist.get_subckt(subckt_name)

# subckt (invalid)
subckt_name_inv = 'dummy_subckt'
subckt_inv = netlist.get_subckt(subckt_name_inv)

# instance
inst_name = 'xalu4'
inst = netlist.top_subckt.get_inst(inst_name)

# instance (invalid)
inst_name_inv = 'dummy_inst'
inst_inv = netlist.top_subckt.get_inst(inst_name_inv)

# primitive
pri_name = 'NMOS'

# net
net = 'a0'
net_inv = 'a5'

# net path
str_net_path = 'xalu4.XFA1.A'
str_up_path = 'xalu4.A1'
str_top_path = 'a1'
net_path = netlist.get_path(str_net_path)
top_net_path = netlist.get_top_path(net_path)
up_net_path = netlist.get_up_path(net_path)

# net path (invalid)
str_net_path_inv = 'xalu4.XFA2.dummy_inst.dummy_net'
net_path_inv = netlist.get_path(str_net_path_inv)
top_net_path_inv = netlist.get_top_path(net_path_inv)
up_net_path_inv = netlist.get_up_path(net_path_inv)

# primitive path
str_pri_path = 'xalu4.XMUX2.X2.M1'
pri_path = netlist.get_path(str_pri_path)
top_pri_path = netlist.get_top_path(pri_path)
up_pri_path = netlist.get_up_path(pri_path)

# primitive path (invalid)
str_pri_path_inv = 'xalu4.XMUX2.X2.m123'
pri_path_inv = netlist.get_path(str_pri_path_inv)
top_pri_path_inv = netlist.get_top_path(pri_path_inv)
up_pri_path_inv = netlist.get_up_path(pri_path_inv)

# instance path
str_inst_path = 'xalu4.XNOT1'
inst_path = netlist.get_path(str_inst_path)
top_inst_path = netlist.get_top_path(inst_path)
up_inst_path = netlist.get_up_path(inst_path)
str_inst_path_term_0 = 'xalu4.B1'
str_inst_path_term_1 = 'xalu4.NB1'

# instance path
str_inst_path_inv = 'xalu4.x123'
inst_path_inv = netlist.get_path(str_inst_path_inv)
top_inst_path_inv = netlist.get_top_path(inst_path_inv)
up_inst_path_inv = netlist.get_up_path(inst_path_inv)

# short net to net
short_subckt_name = 'ALU4'
short_master_net = 'A1'
short_slave_net = 'A0'

# ---------------------------------------------------------------------
# Class: netlist
# ---------------------------------------------------------------------
def test_netlist_get_subckt():
	assert subckt.name == subckt_name
	assert not subckt_inv

def test_netlist_get_path():
	assert netlist.get_str_path(net_path) == str_net_path
	assert netlist.get_str_path(net_path_inv) == ''
	assert netlist.get_str_path(pri_path) == str_pri_path
	assert netlist.get_str_path(pri_path_inv) == ''
	assert netlist.get_str_path(inst_path) == str_inst_path
	assert netlist.get_str_path(inst_path_inv) == ''

def test_netlist_write():
	file_name = os.path.basename(netlist_path)
	with open('out/' + file_name, 'w') as f:
		netlist.write(f)
	diff = sp.getoutput(f'diff out/{file_name} ref/{file_name}')
	assert not diff

def test_netlist_get_top_path():
	assert netlist.get_str_path(top_net_path) == str_top_path
	assert not netlist.get_str_path(top_net_path_inv)
	assert not netlist.get_str_path(top_pri_path)
	assert not netlist.get_str_path(top_pri_path_inv)
	assert not netlist.get_str_path(top_inst_path)
	assert not netlist.get_str_path(top_inst_path_inv)

def test_netlist_get_up_path():
	assert netlist.get_str_path(up_net_path) == str_up_path
	assert not netlist.get_str_path(up_net_path_inv)
	assert not netlist.get_str_path(up_pri_path)
	assert not netlist.get_str_path(up_pri_path_inv)
	assert not netlist.get_str_path(up_inst_path)
	assert not netlist.get_str_path(up_inst_path_inv)

def test_netlist_get_pri_paths():
	pri_paths = netlist.get_pri_paths(net_path)
	pri_paths_inv = netlist.get_pri_paths(net_path_inv)
	file_name = str_net_path + '_get_pri_paths'
	file_name_inv = str_net_path_inv + '_get_pri_paths'
	with open(f'out/{file_name}', 'w') as f:
		for pri_path, terms in pri_paths:
			f.write(f'{netlist.get_str_path(pri_path)} {terms}\n')
	with open(f'out/{file_name_inv}', 'w') as f:
		for pri_path_inv, terms in pri_paths_inv:
			f.write(f'{netlist.get_str_path(pri_path_inv)} {terms}\n')
	diff = sp.getoutput(f'diff out/{file_name} ref/{file_name}')
	diff_inv = sp.getoutput(f'diff out/{file_name_inv} ref/{file_name_inv}')	
	assert not diff
	assert not diff_inv

def test_netlist_get_inst_paths():
	inst_paths = netlist.get_inst_paths(subckt_name)
	inst_paths_inv = netlist.get_inst_paths(subckt_name_inv)
	inst_paths_pri = netlist.get_inst_paths(pri_name)
	file_name = subckt_name + '_get_inst_paths'
	file_name_inv = subckt_name_inv + '_get_inst_paths'
	file_name_pri = pri_name + '_get_inst_paths'
	with open(f'out/{file_name}', 'w') as f:
		for i in inst_paths:
			f.write(netlist.get_str_path(i) + '\n')
	with open(f'out/{file_name_inv}', 'w') as f:
		for i in inst_paths_inv:
			f.write(netlist.get_str_path(i) + '\n')
	with open(f'out/{file_name_pri}', 'w') as f:
		for i in inst_paths_pri:
			f.write(netlist.get_str_path(i) + '\n')
	diff = sp.getoutput(f'diff out/{file_name} ref/{file_name}')
	diff_inv = sp.getoutput(f'diff out/{file_name_inv} ref/{file_name_inv}')
	diff_pri = sp.getoutput(f'diff out/{file_name_pri} ref/{file_name_pri}')
	assert not diff
	assert not diff_inv
	assert not diff_pri

def test_netlist_is_same_net():
	assert netlist.is_same_net(up_net_path, net_path)
	assert not netlist.is_same_net(net_path_inv, net_path)

def test_netlist_get_net_path():
	path_term_0 = netlist.get_net_path(inst_path, 0)
	path_term_1 = netlist.get_net_path(inst_path, 1)
	path_term_0_inv = netlist.get_net_path(inst_path_inv, 0)
	assert netlist.get_str_path(path_term_0) == str_inst_path_term_0
	assert netlist.get_str_path(path_term_1) == str_inst_path_term_1
	assert not path_term_0_inv

def test_netlist_get_net_paths():
	net_paths = netlist.get_net_paths(net_path)
	net_paths_inv = netlist.get_net_paths(net_path_inv)
	file_name = str_net_path + '_get_net_paths'
	file_name_inv = str_net_path_inv + '_get_net_paths'
	with open(f'out/{file_name}', 'w') as f:
		for i in net_paths:
			f.write(netlist.get_str_path(i) + '\n')
	with open(f'out/{file_name_inv}', 'w') as f:
		for i in net_paths_inv:
			f.write(netlist.get_str_path(i) + '\n')
	diff = sp.getoutput(f'diff out/{file_name} ref/{file_name}')
	diff_inv = sp.getoutput(f'diff out/{file_name_inv} ref/{file_name_inv}')
	assert not diff
	assert not diff_inv

def test_netlist_short_by_term():
	copy_netlist = copy.deepcopy(netlist)
	copy_netlist.short_by_term('resistor', [0, 1])
	copy_netlist.short_by_term(subckt_name, [0, 1, 2])
	file_name = subckt_name + '_res_short_by_term'
	with open(f'out/{file_name}', 'w') as f:
		copy_netlist.write(f)
	diff = sp.getoutput(f'diff out/{file_name} ref/{file_name}')
	assert not diff

# ---------------------------------------------------------------------
# Class: subckt
# ---------------------------------------------------------------------
def test_subckt_get_inst():
	assert inst.name == inst_name
	assert not inst_inv

def test_subckt_has_net():
	assert netlist.top_subckt.has_net(net)
	assert not netlist.top_subckt.has_net(net_inv)

def test_subckt_replace_net():
	copy_netlist = copy.deepcopy(netlist)
	short_subckt = copy_netlist.get_subckt(short_subckt_name)
	short_subckt.replace_net(short_master_net, short_slave_net)
	file_name = short_subckt_name + '_replace_net'
	with open(f'out/{file_name}', 'w') as f:
		copy_netlist.write(f)
	diff = sp.getoutput(f'diff out/{file_name} ref/{file_name}')
	assert not diff

# ---------------------------------------------------------------------
# performance
# ---------------------------------------------------------------------
time_end = time.time()
time_run = round(time_end - time_start, 3)
curr_mem, peak_mem = tracemalloc.get_traced_memory()
curr_mem = round(curr_mem / (1024 ** 2), 3)
peak_mem = round(peak_mem / (1024 ** 2), 3)
print()
print('-' * 80)
print(f'Total run time: {time_run}s')
print(f'Current memory: {curr_mem}MB')
print(f'Peak memory: {peak_mem}MB')
print('-' * 80)
