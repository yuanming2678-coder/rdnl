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
# Description	: Read spice netlist into Python object (netlist visualization)
# =====================================================================
import os, sys, tkinter as tk
from tkinter import ttk
from tkinter import filedialog
sys_path = os.path.abspath(os.path.dirname(__file__) + '../../../')
sys.path.append(sys_path)
import rdnl.core as core
import rdnl.api as api

# ---------------------------------------------------------------------
# select file
# ---------------------------------------------------------------------
def select_file(label, combo):
	global netlist
	file_path = filedialog.askopenfilename()
	label.config(text = file_path)
	netlist = api.read_netlist(label.cget('text'))
	subckts = [subckt.name for subckt in netlist.subckts]
	combo.config(values = subckts)

# ---------------------------------------------------------------------
# subckt show
# ---------------------------------------------------------------------
def subckt_show(combo):
	global netlist
	subckt = netlist.get_subckt(combo.get())
	subckt.show()

# ---------------------------------------------------------------------
# netlist visualization GUI
# ---------------------------------------------------------------------
def vsnl_gui(netlist):

	# setup window
	window = tk.Tk()
	window.title('Netlist Visualization')
	window.geometry('550x400')

	# setup tab
	notebook = ttk.Notebook(window)
	notebook.pack(expand=True, fill="both")
	#notebook.grid(row = 0, column = 0, columnspan = 2)
	tab1 = ttk.Frame(notebook)
	tab2 = ttk.Frame(notebook)
	notebook.add(tab1, text = 'Subckt')
	notebook.add(tab2, text = 'TBD')
	bold = ('Arial', 12, 'bold')

	# netlist label
	nl_labal = tk.Label(tab1, text = 'Netlist', font = bold)
	nl_labal.grid(row = 1, column = 0, columnspan = 2,
				  sticky = 'w', padx = 10, pady = 10)

	# netlist browse
	nl_browse_button = tk.Button(tab1, text = 'Browse', width = 8,
								 command = lambda:select_file(nl_path_label, subckt_sel_combo))
	nl_browse_button.grid(row = 2, column = 0, padx = 10, sticky = 'w')

	# netlist path label
	nl_path_label = tk.Label(tab1, text = netlist.path if netlist else '')
	nl_path_label.grid(row = 2, column = 1, sticky = 'w')

	# subckt label
	subckt_labal = tk.Label(tab1, text = 'Subckt', font = bold)
	subckt_labal.grid(row = 3, column = 0, columnspan = 2,
				  	  sticky = 'w', padx = 10, pady = 10)

	# subckt show button
	subckt_show_button = tk.Button(tab1, text = 'Show', width = 8,
								   command = lambda:subckt_show(subckt_sel_combo))
	subckt_show_button.grid(row = 4, column = 0, padx = 10, sticky = 'w')

	# subckt select combobox
	subckts = [subckt.name for subckt in netlist.subckts] if netlist else []
	subckt_sel_combo = ttk.Combobox(tab1, values = subckts, width = 40)
	subckt_sel_combo.grid(row = 4, column = 1, sticky = 'w')

	# start GUI
	window.mainloop()

# ---------------------------------------------------------------------
# main function
# ---------------------------------------------------------------------
if __name__ == '__main__':
	global netlist
	netlist = api.read_netlist(sys.argv[1]) if len(sys.argv) == 2 else None
	vsnl_gui(netlist)
