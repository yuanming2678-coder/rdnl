 CONFIDENTIAL AND PROPRIETARY CODE

 =====================================================================
 Copyright (c) 2025 [Yuan Ming Yu]. All rights reserved.
 This code is confidential and proprietary to [Yuan Ming Yu].

 Unauthorized copying, modification, distribution, or disclosure of this
 code is strictly prohibited.

 This code is provided "as-is" without any warranty, express or implied.
 Use at your own risk.

 For any inquiries regarding usage or licensing, please contact:
 [Contact Information or Legal Team Email]

 =====================================================================

Author: Yuan Ming Yu
Date: 2025/08/01
Description: Read spice netlist into Python class object for postproceesing

Hierarchy Description:
	|_ rdnl: Top-level package
		|_ func.py: Function only
		|_ core.py: Class definition with methods
		|_ api.py:	RDNL APIs
		|_ globalvar.py: Global variables across modules
		|_ test: Testing directory
			|_ test_rdnl.py: Pytest
			|_ out: Output file directory
			|_ ref: Reference file directory

Python3 path: /usr/bin/python3

Used library:
	- sys
	- os
	- re
	- time
	- tracemalloc
	- subprocess

Usage:
	python3 -m pydoc rdnl
	python3 -m pydoc rdnl.api
	python3 -m pydoc rdnl.core

Example:
	./test/test_rdnl.py

Contact:
	Email: yuanming2678@gmail.com
