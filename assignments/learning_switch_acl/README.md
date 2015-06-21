## NetASM Assignment

In this exercise, you will learn how to define new data-plane layouts, add custom state elements like tables, and control how each packet is processed in the data plane. To do so, you will be learning and using **NetASM**, a new domain-specific language for configuring programmable data planes on a variety of targets.

NetASM is analogous to an x86 or MIPS-like instructions set.  However, unlike updating main memory and registers, it defines the layout (i.e., control-flow and states) of the data plane. Control-flow defines how the packet is traversed through the data plane, and state refers to the type of memory element (i.e., tables). These state elements have a well-defined data structure and type declaration in NetASM, which makes it easy to identify bugs early in the compilation process.

The syntax of the NetASM language is defined in the [`netasm/core/syntax.py`](https://github.com/NetASM/NetASM-python/blob/master/netasm/netasm/core/syntax.py) file.

### Overview

For more information about the NetASM language read the following material:

* [NetASM-python Wiki](https://github.com/NetASM/NetASM-python/wiki)
* The Case for an Intermediate Representation for Programmable Data Planes: [`paper`](http://www.cs.princeton.edu/~mshahbaz/papers/sosr15-netasm.pdf) [`slides`](http://www.cs.princeton.edu/~mshahbaz/slides/sosr15-netasm.pptx)


