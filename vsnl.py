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
from tkinter import messagebox
sys_path = os.path.abspath(os.path.dirname(__file__) + '/../')
sys.path.append(sys_path)
import rdnl.core as core
import rdnl.api as api

# ---------------------------------------------------------------------
# select file
# ---------------------------------------------------------------------
def select_file():
	global netlist, nl_path_label, subckt_sel_combo
	file_path = filedialog.askopenfilename()
	nl_path_label.config(text = file_path)
	netlist = api.read_netlist(nl_path_label.cget('text'))
	subckts = [subckt.name for subckt in netlist.subckts]
	subckt_sel_combo.config(values = subckts)

# ---------------------------------------------------------------------
# select dir
# ---------------------------------------------------------------------
def select_dir():
	global save_path_label
	dir_path = filedialog.askdirectory()
	save_path_label.config(text = dir_path)

# ---------------------------------------------------------------------
# subckt show
# ---------------------------------------------------------------------
def subckt_show():
	global netlist, subckt_sel_combo, scale_entry, offset_entry
	global save_path_label, save
	subckt_name = subckt_sel_combo.get()
	scale = float(scale_entry.get())
	offset = float(offset_entry.get())
	subckt = netlist.get_subckt(subckt_name)
	dir_path = save_path_label.cget('text')
	if subckt != None:
		if save.get() and dir_path:
			file_name = 'subckt_' + subckt_name + '.jpg'
			path = dir_path + '/' + file_name
			messagebox.showinfo('Info', f'\"{file_name}\" is saved')
		else:
			path = None
		subckt.show(scale, offset, path)
	else:
		messagebox.showwarning('Warning', f'Subckt \"{subckt_name}\" not exist')

# ---------------------------------------------------------------------
# netlist visualization GUI
# ---------------------------------------------------------------------
def vsnl_gui(netlist):
	global subckt_sel_combo, nl_path_label, subckt_sel_combol
	global scale_entry, offset_entry, save_path_label, save

	# setup window
	window = tk.Tk()
	window.title('Netlist Visualization')
	window.geometry('550x400')

	# setup tab
	notebook = ttk.Notebook(window)
	notebook.pack(expand=True, fill="both")
	tab1 = ttk.Frame(notebook)
	tab2 = ttk.Frame(notebook)
	notebook.add(tab1, text = 'Subckt')
	notebook.add(tab2, text = 'TBD')
	bold = ('Arial', 12, 'bold')

	# netlist label (0, 1, 0-1)
	nl_labal = tk.Label(tab1, text = 'Netlist', font = bold)
	nl_labal.grid(row = 1, column = 0, columnspan = 2,
				  sticky = 'w', padx = 10, pady = 10)

	# netlist browse button (0, 2, 0)
	nl_browse_button = tk.Button(tab1, text = 'Browse', width = 8,
								 command = lambda:select_file())
	nl_browse_button.grid(row = 2, column = 0, padx = 10, sticky = 'w')

	# netlist path label (0, 2, 1)
	nl_path_label = tk.Label(tab1, text = netlist.path if netlist else '')
	nl_path_label.grid(row = 2, column = 1, sticky = 'w', columnspan = 2)

	# subckt label (0, 3, 0-1)
	subckt_labal = tk.Label(tab1, text = 'Subckt', font = bold)
	subckt_labal.grid(row = 3, column = 0, columnspan = 2,
				  	  sticky = 'w', padx = 10, pady = 10)

	# subckt show button (0, 4, 0)
	subckt_show_button = tk.Button(tab1, text = 'Show', width = 8,
								   command = lambda:subckt_show())
	subckt_show_button.grid(row = 4, column = 0, padx = 10, sticky = 'w')

	# subckt select combobox (0, 4, 1)
	subckts = [subckt.name for subckt in netlist.subckts] if netlist else []
	subckt_sel_combo = ttk.Combobox(tab1, values = subckts, width = 40)
	subckt_sel_combo.grid(row = 4, column = 1, sticky = 'w', columnspan = 2)

	# save browse button (0, 5, 0)
	save_browse_button = tk.Button(tab1, text = 'Browse\nSave Path', width = 8, height = 2,
								   command = lambda:select_dir())
	save_browse_button.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = 'w')

	# save path label (0, 5, 1)
	save_path_label = tk.Label(tab1)
	save_path_label.grid(row = 5, column = 1, sticky = 'w')

	# save label (0, 6, 0)
	save_label = tk.Label(tab1, text = 'Save Schem')
	save_label.grid(row = 6, column = 0, padx = 10, sticky = 'w')

	# save check (0, 6, 1)
	save = tk.IntVar(value = 0)
	save_check = tk.Checkbutton(tab1, variable = save)
	save_check.grid(row = 6, column = 1, sticky = 'w')

	# option label (0, 7, 0-1)
	opt_labal = tk.Label(tab1, text = 'Options', font = bold)
	opt_labal.grid(row = 7, column = 0, columnspan = 2,
				   sticky = 'w', padx = 10, pady = 10)

	# scale label (0, 8, 0)
	scale_labal = tk.Label(tab1, text = 'Scale')
	scale_labal.grid(row = 8, column = 0, sticky = 'w', padx = 10)

	# scale entry (0, 8, 1)
	scale_entry = tk.Entry(tab1, width = 10)
	scale_entry.insert(0, 2.5)
	scale_entry.grid(row = 8, column = 1, sticky = 'w')

	# offset label (0, 9, 0)
	offset_label = tk.Label(tab1, text = 'Offset')
	offset_label.grid(row = 9, column = 0, sticky = 'w', padx = 10)

	# offset entry (0, 9, 1)
	offset_entry = tk.Entry(tab1, width = 10)
	offset_entry.insert(0, 0.5)
	offset_entry.grid(row = 9, column = 1, sticky = 'w')

	# start GUI
	window.mainloop()

# ---------------------------------------------------------------------
# main function
# ---------------------------------------------------------------------
if __name__ == '__main__':
	global netlist
	netlist = api.read_netlist(sys.argv[1]) if len(sys.argv) == 2 else None
	vsnl_gui(netlist)
