 ### CONFIDENTIAL AND PROPRIETARY CODE
 ### =====================================================================
 ### Copyright (c) 2025 [Yuan Ming Yu]. All rights reserved.
 ### This code is confidential and proprietary to [Yuan Ming Yu].

 ### Unauthorized copying, modification, distribution, or disclosure of this
 ### code is strictly prohibited.

 ### This code is provided "as-is" without any warranty, express or implied.
 ### Use at your own risk.

 ### For any inquiries regarding usage or licensing, please contact:
 ### [Contact Information or Legal Team Email]
 ### =====================================================================

Author: Yuan Ming Yu
Date: 2025/08/01
Description: Read spice netlist into Python class object for postproceesing

Hierarchy Description:
&nbsp|_ rdnl: Top-level package<br>
&nbsp&nbsp|_ func.py: Function only<br>
&nbsp&nbsp|_ core.py: Class definition with methods<br>
&nbsp&nbsp|_ api.py: RDNL APIs<br>
&nbsp&nbsp|_ globalvar.py: Global variables across modules<br>
&nbsp&nbsp|_ test: Testing directory<br>
&nbsp&nbsp&nbsp|_ test_rdnl.py: Pytest<br>
&nbsp&nbsp&nbsp|_ out: Output file directory<br>
&nbsp&nbsp&nbsp|_ ref: Reference file directory<br>

Python3 path: /usr/bin/python3

Used library:<br>
&nbsp- sys<br>
&nbsp- os<br>
&nbsp- re<br>
&nbsp- time<br>
&nbsp- tracemalloc<br>
&nbsp- subprocess<br>

Usage:<br>
&nbsppython3 -m pydoc rdnl<br>
&nbsppython3 -m pydoc rdnl.api<br>
&nbsppython3 -m pydoc rdnl.core<br>

Example:<br>
&nbsp./test/test_rdnl.py

Contact:<br>
&nbspEmail: yuanming2678@gmail.com
