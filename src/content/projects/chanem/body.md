* [Thesis](https://dspace.mit.edu/handle/1721.1/85698)

chanem is a high-bandwidth channel emulator for observing the effects of
Doppler shifting on an input signal.

This project constituted my master's thesis for the [Department of Electrical
Engineering and Computer Science](https://www.eecs.mit.edu/) at
[MIT](https://mit.edu).  It was conducted as part of the [MIT
VI-A](https://6a.mit.edu/) co-op program with [MIT Lincoln
Laboratory](https://www.ll.mit.edu/), for which it received The J. Francis
Reintjes Excellence in 6-A Industrial Practice Award.

chanem was a full-stack project, in that its construction involved

* creation of a high-speed digital interface to control an ADC/DAC daughter card,
* design, simulation, and implementation of high-speed DSP algorithms on an FPGA,
* implementation of complex state-full control logic with a soft-processor, and
* construction of a software framework to interface with an input stream (such
  as a flight simulator), calculate Doppler shift commands, and send them to
  the FPGA

In addition, during construction of chanem, a number of infrastructure tools
were built to aid the development process, such as

* a build system to wrap around the Xilinx toolchain,
* a method for preprocessing VHDL inputs,
* a high-level assembly language and compiler that produces Picoblaze assembly
  code, and
* a Python framework for plotting simulated and captured spectral data to a
  format suitable for print
