#!/usr/bin/python
#coding:utf-8

import commands
import optparse
import shlex
import lldb
import re
import os


def iobjc_msgSend(debugger, command, result, internal_dict):
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread()
	#thread.StepOver()
	thread.StepInstruction(True)
	while True:
		interpreter.HandleCommand('dis -p -c 10', returnObject)
		disassemble = returnObject.GetOutput();
		p = re.compile(r'->.*')
		m = p.search(disassemble)
		c = m.group(0)

		if any(re.findall(r'objc_release|objc_retainAutorelease', c, re.IGNORECASE)):
			#thread.StepOver()
			thread.StepInstruction(True)

		elif any(re.findall(r'\sbl\s|\sblr\s|\sb\s\s|\sb\.|\scbz\s|\scbnz\s|\stbnz\s|\stbz\s|\scmp\s', c, re.IGNORECASE)):
			print 'objc_msgSend Hited!'
			print disassemble
			break

		else:
			#thread.StepOver()
			thread.StepInstruction(True)

	iarguments(debugger, command, result, internal_dict)


def idisassemble(debugger, command, result, internal_dict):
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


def ievaluate(debugger, command, result, internal_dict):
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
	iunicode(debugger, '$x0', result, internal_dict)
	print 'Instruction Return Value : %s' % ret


def iarguments(debugger, command, result, internal_dict):
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('po $x0', returnObject)
	object_name = returnObject.GetOutput().strip()
	interpreter.HandleCommand('p (char *)$x1', returnObject)
	method_name = returnObject.GetOutput().strip()

	print '[%s %s]' % (object_name, method_name)

	objc_message = '['
	objc_message += '%s ' % iunicode(debugger, '$x0', result, internal_dict)
	p = re.compile('"(.*)"')
	m = p.search(method_name)
	if m is not None:
		selectors = m.group(1)
		names = selectors.split(':')
		if len(names) > 1:
			for i in range(len(names) - 1):
				interpreter.HandleCommand('po $x%d' % (i + 2), returnObject)
				value = returnObject.GetOutput().strip()
				sel = names[i]
				sel = iunicode(debugger, '"'+sel+'"', result, internal_dict)

				objc_message += '%s:%s ' % (sel, value)
		else:
			sel = selectors
			sel = iunicode(debugger, '"'+sel+'"', result, internal_dict)
				
			objc_message += sel
	

	objc_message += ']'
	print objc_message


def iunicode(debugger, command, result, internal_dict):
	args = shlex.split(command)
	first_parameter = args[0]
	if r"\xffffff" in first_parameter:		# unicode string
		unicode_string = first_parameter.replace("ffffff", "")
		unicode_escaped = unicode_string.decode('string-escape')
		print unicode_string + ' -> ' + unicode_escaped
		return unicode_escaped

	## for address
	elif first_parameter.startswith("0x"):
		interpreter = lldb.debugger.GetCommandInterpreter()
		returnObject = lldb.SBCommandReturnObject()
		meta_class_address = first_parameter
		## p (char *)class_getName((struct objc_class *)0x00000001047eb440)
		interpreter.HandleCommand('p (char *)class_getName((void *)[%s class])' % meta_class_address, returnObject)
		meta_class_name = returnObject.GetOutput().strip()
		index_start = meta_class_name.find('"')
		if index_start >= 0:
			index_end = meta_class_name.find('"', index_start + 1)
			unicode_string = meta_class_name[index_start : index_end + 1]
			return iunicode(debugger, unicode_string, result, internal_dict)

	## for class
	elif first_parameter.startswith("$x"):
		interpreter = lldb.debugger.GetCommandInterpreter()
		returnObject = lldb.SBCommandReturnObject()
		register = first_parameter
		interpreter.HandleCommand('p/x %s' % register, returnObject)
		object_address = returnObject.GetOutput().strip()
		object_address = object_address.split('=')[-1]
		return iunicode(debugger, object_address, result, internal_dict)

	## for argument/selector
	## usage: iunicode "(char *)$x5"
	## to do ...
	elif first_parameter.startswith("(char *)$x"):
		interpreter = lldb.debugger.GetCommandInterpreter()
		returnObject = lldb.SBCommandReturnObject()
		register = first_parameter
		interpreter.HandleCommand('p %s' % register, returnObject) ## p (char *)$x5
		address_content = returnObject.GetOutput().strip()  ## (char *) $496 = 0x00000001047cbf61 "\xffffffe4\xffffffb8\xffffff80"
		address_content = address_content.split('=')[-1]
		content = address_content.split(' ')[-1]
		return iunicode(debugger, content, result, internal_dict)

	return first_parameter
		


def __lldb_init_module(debugger, dict):
	filePath = os.path.realpath(__file__)
	basename = os.path.basename(filePath)
	filename = os.path.splitext(basename)[0]

	command = 'iobjc_msgSend'
	helpText = "Break at / Step to next objc_msgSend."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

	command = 'idisassemble'
	helpText = "Print current disassemble instructions."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

	command = 'ievaluate'
	helpText = "Evaluate current instruction."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

	command = 'iarguments'
	helpText = "Print current objc_msgSend arguments."
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

	command = 'iunicode'
	helpText = "Print the unicode encoding string. iunicode address/string"
	debugger.HandleCommand('command script add --help "{help}" --function {function} {name}'.format(help=helpText, function='%s.%s'%(filename, command), name=command))
	print 'The "%s" python command has been installed and is ready for use.' % command

