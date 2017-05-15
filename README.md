

Start `Debugserver` and `LLDB`，attatch the process you want to debug.

## How to use

#### 1. Import the scripts

`command script import ~/Path/To/objc_msgSend.py`

`command script import ~/Path/To/objc_msgSend.py`

Also, you can put these command above into the file `~/.lldbinit` .

#### 2. Use the imported Debugger commands

`(lldb) help`

```
Current user-defined commands:
  iaslr                 -- Print specified module ASLR.
  ibreak                -- Set specified module breakpoint plus ASLR.
  ievaluate_instruction -- Evaluate current instruction.
  ifaddress             -- Get specified module breakpoint minus ASLR.
  iobjc_msgSend         -- Break at next objc_msgSend.
  iprint_arguments      -- Print current objc_msgSend arguments.
  iraddress             -- Get specified module breakpoint minus ASLR.
  ishow_disassemble     -- Show current disassemble instructions.
```

`(lldb) process interrupt`

`(lldb) iaslr`

`(lldb) iaslr UIKit`

`(lldb) iobjc_msgSend`

`(lldb) ishow_disassemble`
