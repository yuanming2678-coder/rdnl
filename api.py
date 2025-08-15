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
# Description	: Read spice netlist into Python object (API only)
# =====================================================================
import os
import rdnl.func as func
import rdnl.vsnl as vsnl

# ---------------------------------------------------------------------
# read netlist
# ---------------------------------------------------------------------
def read_netlist(file_path, rowcmt = '*', inline = '$'):
	'''
	Description:
		Read Spice netlist
	Args:
		Netlist file path
	Return:
		Netlist
	'''
	file_path = os.path.realpath(file_path)
	tmp_file_path = '/tmp/' + os.path.basename(file_path) + '.tmp'
	func.proc_netlist(file_path, tmp_file_path, rowcmt, inline)
	os.system(f'sed -i \'1d\' {tmp_file_path}')
	netlist = func.parse_netlist(tmp_file_path, file_path)
	return netlist

# ---------------------------------------------------------------------
# show netlist in GUI
# ---------------------------------------------------------------------
def show_netlist(netlist):
	'''
	Description:
		Visualize netlist in GUI
	Args:
		Netlist
	Return:
	'''
	vsnl.vsnl_gui(netlist)
