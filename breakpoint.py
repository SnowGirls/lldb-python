#!/usr/bin/python
#coding:utf-8

import optparse
import shlex
import lldb
import re
import os


# get ASLR of specified module. i.e. iaslr UIKit
def iaslr(debugger, command, result, internal_dict):
	interpreter = debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('image list -o -f', returnObject)
	output = returnObject.GetOutput();

	#if no module specified in first argument, use the first/selected frame's module
	if not command:
		stream = lldb.SBStream()
		lldb.debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame().GetModule().GetDescription(stream)
		module_arch_path = stream.GetData()
		module = module_arch_path.split('/')[-1].split('(')[0]
	else:
		module = command

	p = re.compile(r'(0x[0-9a-fA-F]+).*%s' % module)
	m = p.search(output)
	aslr = m.group(1)

	print('%s ASLR: %s' % (module, aslr))

	return aslr


# set break point on fixed address with ASLR
def ibreak(debugger, command, result, internal_dict):
	address = iraddress(debugger, command, result, internal_dict)
	returnObject = lldb.SBCommandReturnObject()
	debugger.GetCommandInterpreter().HandleCommand('br set -a %s' % address, returnObject)
	output = returnObject.GetOutput();
	print(output)

# get the runtime address that fixed address plus ASLR
def iraddress(debugger, command, result, internal_dict):
	args = shlex.split(command)
	if len(args) == 1:
		module = None
		address = args[0]
	elif len(args) == 2:
		address = args[1]
		module = args[0]
	else:
		address = None
		module = None

	if not address:
		print('Failed: Please input the fixed address (i.e. address from IDA) .')
		return

	ASLR = iaslr(debugger, module, result, internal_dict)
	returnObject = lldb.SBCommandReturnObject()
	debugger.GetCommandInterpreter().HandleCommand('p/x %s+%s' % (address, ASLR), returnObject)
	output = returnObject.GetOutput()
	print('Runtime address: ' + output)
	return output.split(' ')[-1]

# get the fixed address that runtime address minus ASLR
def ifaddress(debugger, command, result, internal_dict):
	args = shlex.split(command)
	if len(args) == 1:
		module = None
		address = args[0]
	elif len(args) == 2:
		address = args[1]
		module = args[0]
	else:
		address = None
		module = None

	if not address:
		gprs = get_GPRs(lldb.debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame())
		for value in gprs:
			if 'pc' == value.GetName():
				address = value.GetValue()
				print('pc : %s' % address)
				break

	ASLR = iaslr(debugger, module, result, internal_dict)
	returnObject = lldb.SBCommandReturnObject()
	debugger.GetCommandInterpreter().HandleCommand('p/x %s-%s' % (address, ASLR), returnObject)
	output = returnObject.GetOutput()
	print('Fixed address: ' + output)
	return output.split(' ')[-1]


def get_registers(frame, kind):
    registerSet = frame.GetRegisters()
    for value in registerSet:
        if kind.lower() in value.GetName().lower():
            return value

    return None

def get_GPRs(frame):
    return get_registers(frame, 'general purpose')


def __lldb_init_module(debugger, dict):
	command = 'iaslr'
	helpText = "Print specified module's ASLR. iaslr [module]"
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(__name__, command), name=command))
	print('The "%s" python command has been installed and is ready for use.' % command)

	command = 'ibreak'
	helpText = "Set specified module breakpoint that plus ASLR. ibreak [module] {address}"
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(__name__, command), name=command))
	print('The "%s" python command has been installed and is ready for use.' % command)

	command = 'iraddress'
	helpText = "Translate specified module runtime address that plus ASLR. iraddress [module] {address}"
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(__name__, command), name=command))
	print('The "%s" python command has been installed and is ready for use.' % command)

	command = 'ifaddress'
	helpText = "Translate specified module fixed address that minus ASLR. ifaddress [module] [address]"
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(__name__, command), name=command))
	print('The "%s" python command has been installed and is ready for use.' % command)


