<div align="center">

# Sockets with TCP and UDP!
by: Michael Zhang
</div>

## Contents
<ul>
  <li>Installation Prerequisites
  <li>Usage
  <li>Testing
</ul>

## Installation Prerequisites

**Version:** Python 3.7.7 

**Libraries/Frameworks:** unittest, mock, sys, socket, time, subprocess

## Usage

To run the program itself, using command-line<sup>[1](#myfootnote1)</sup>, enter
<div align="center">

```python server_python_tcp.py [port number]```
</div>

The server must be running before attempting to start the client. Then,
on a different terminal, enter
<div align="center">

```python client_python_tcp.py```
</div>


to start the TCP client. It will prompt you for an IP address, port
number, and command. 

Assuming the three inputs are valid, it will
execute the program and a file named <span>`output.txt`</span> will be
created on the server side while one named <span>`[command].txt`</span>
will be created on the client-side (where <span>`command`<span> is the command you
inputted). You can verify that the file transmission completed
successfully when the contents and properties of
<span>`output.txt`</span> are the exact same as
<span>`[command.txt]`</span> aside from the name of the file.

Similarly, the UDP server/client are run in the same manner:

<div align="center">

```python server_python_udp.py [port number]```
</div>
<div align="center">

```python client_python_udp.py```
</div>

Note that the port number is passed as a command-line argument for
servers; there exists the possibility that the port is already in use.
In such a case, an ```OSError``` will be thrown which will be caught and our program
will print ```Port in use``` and terminate.

## Testing

I have included 4 unit-test files under the names as specified. Each can
be run by using the command 
<div align="center">

```python test_client_udp.py```
</div>

where you replace <span>`udp`</span> in <span>`test_client_udp.py`</span> with whichever file
you wish to test.

As I use Mock, each of the unittests can be ran separately - I mock
sockets depending on what is needed in my tests. I have documented my
code fairly thoroughly both in unit testing and the program code itself
so that it’s clear which test cases are being tested and the purpose of
each snippet of code. Furthermore, my program code has been modularized
for easy readability.

For manual testing, you can follow the **Usage** instructions

### Test Case Example
In a test case where the socket fails
to connect to the given IP and port, <span>`Could not connect to server.`<span>
would be printed and the unittest would pass as the function correctly
prints out what it should. 

<a name="myfootnote1"><sup>1</sup></a> Note that you may need to use the command python3 instead of python
    as I have an alias on my configuration
