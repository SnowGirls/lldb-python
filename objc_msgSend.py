#!/usr/bin/python

import commands
import optparse
import shlex
import lldb
import re
import os

def ishow_disassemble(debugger, command, result, internal_dict):
	args = shlex.split(command)
	count = 20
	if len(args) > 0:
		count = args[0]

	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('dis -s `$pc-0x8` -c %d' % (count), returnObject)
	output = returnObject.GetOutput();
	error = returnObject.GetError()
	print output + '' + error


def iobjc_msgSend(debugger, command, result, internal_dict):
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread()
	thread.StepOver()
	while True:
		interpreter.HandleCommand('dis -p -c 10', returnObject)
		disassemble = returnObject.GetOutput();
		p = re.compile(r'->.*')
		m = p.search(disassemble)
		c = m.group(0)

		if any(re.findall(r'objc_release|objc_retainAutorelease', c, re.IGNORECASE)):
			thread.StepOver()

		elif any(re.findall(r'\sbl\s|\sb\s\s|\sb\.|\scbz\s|\scbnz\s|\scmp\s', c, re.IGNORECASE)):
			print 'objc_msgSend Hited!'
			print disassemble
			break

		else:
			thread.StepOver()

	iprint_arguments(debugger, command, result, internal_dict)

def ievaluate_instruction(debugger, command, result, internal_dict):
	per_instruction_len = 0x4
	show_instructions_len = 5

	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread()
	thread.StepOver()
	print 'Instruction Evaluated!'

	interpreter.HandleCommand('dis -s `$pc-%d` -c %d' % (per_instruction_len, show_instructions_len), returnObject)
	disassemble = returnObject.GetOutput()
	print disassemble

	interpreter.HandleCommand('po $x0', returnObject)
	ret = returnObject.GetOutput().strip()
	print 'Instruction Return Value : %s' % ret


def iprint_arguments(debugger, command, result, internal_dict):
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('po $x0', returnObject)
	arg1 = returnObject.GetOutput().strip()
	interpreter.HandleCommand('p (char *)$x1', returnObject)
	arg2 = returnObject.GetOutput().strip()

	print '-[%s %s]' % (arg1, arg2)

	functionName = '['
	functionName += '%s ' % arg1
	p = re.compile('"(.*)"')
	m = p.search(arg2)
	if m is not None:
		s = m.group(1)
		names = s.split(':')
		if len(names) > 1:
			for i in range(len(names) - 1):
				interpreter.HandleCommand('po $x%d' % (i + 2), returnObject)
				value = returnObject.GetOutput().strip()
				name = names[i]
				functionName += ' %s:%s ' % (name, value)
		else:
			functionName += s
	

	functionName += ']'
	print functionName


def __lldb_init_module(debugger, dict):
	filePath = os.path.realpath(__file__)
	basename = os.path.basename(filePath)
	filename = os.path.splitext(basename)[0]

	command = 'ishow_disassemble'
	# debugger.HandleCommand('command script add %s -f %s.%s' % (command, filename, command))
	helpText = "Show current disassemble instructions."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

	command = 'iobjc_msgSend'
	# debugger.HandleCommand('command script add %s -f %s.%s' % (command, filename, command))
	helpText = "Break at next objc_msgSend."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

	command = 'ievaluate_instruction'
	# debugger.HandleCommand('command script add %s -f %s.%s' % (command, filename, command))
	helpText = "Evaluate current instruction."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

	command = 'iprint_arguments'
	# debugger.HandleCommand('command script add %s -f %s.%s' % (command, filename, command))
	helpText = "Print current objc_msgSend arguments."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

