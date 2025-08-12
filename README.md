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

Author: Yuan Ming Yu<br>
Date: 2025/08/01<br>
Description: Read spice netlist into Python class object for postproceesing<br>

Hierarchy Description:<br>
&nbsp;&nbsp;|_ rdnl: Top-level package<br>
&nbsp;&nbsp;&nbsp;&nbsp;|_ func.py: Function only<br>
&nbsp;&nbsp;&nbsp;&nbsp;|_ core.py: Class definition with methods<br>
&nbsp;&nbsp;&nbsp;&nbsp;|_ api.py: RDNL APIs<br>
&nbsp;&nbsp;&nbsp;&nbsp;|_ globalvar.py: Global variables across modules<br>
&nbsp;&nbsp;&nbsp;&nbsp;|_ test: Testing directory<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_ test_rdnl.py: Pytest<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_ out: Output file directory<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_ ref: Reference file directory<br>

Python3 path: /usr/bin/python3<br>

Used library:<br>
&nbsp;&nbsp;- sys<br>
&nbsp;&nbsp;- os<br>
&nbsp;&nbsp;- re<br>
&nbsp;&nbsp;- time<br>
&nbsp;&nbsp;- tracemalloc<br>
&nbsp;&nbsp;- subprocess<br>

Usage:<br>
&nbsp;&nbsp;python3 -m pydoc rdnl<br>
&nbsp;&nbsp;python3 -m pydoc rdnl.api<br>
&nbsp;&nbsp;python3 -m pydoc rdnl.core<br>

Example:<br>
&nbsp;&nbsp;./test/test_rdnl.py<br>

Contact:<br>
&nbsp;&nbsp;Email: yuanming2678@gmail.com<br>
