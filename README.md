

Start `Debugserver` and `LLDB`，attatch the process you want to debug.

## How to use

#### 1. Import the scripts

`command script import ~/Path/To/breakpoint.py`

`command script import ~/Path/To/objc_msgSend.py`

Also, you can put these command above into the file `~/.lldbinit` 


#### 2. Use the imported Debugger commands

`(lldb) help`

```
Current user-defined commands:
  iaslr                 -- Print specified module's ASLR. iaslr [module]
  ibreak                -- Set specified module breakpoint that plus ASLR. ibreak [address] [module]
  ievaluate_instruction -- Evaluate current instruction.
  ifaddress             -- Translate specified module fixed address that minus ASLR. ifaddress [address] [module]
  iobjc_msgSend         -- Break at / Step to next objc_msgSend.
  iprint_arguments      -- Print current objc_msgSend arguments.
  iraddress             -- Translate specified module runtime address that plus ASLR. iraddress {address} [module]
  ishow_disassemble     -- Print current disassemble instructions.
```

`(lldb) process interrupt`

`(lldb) iaslr`

`(lldb) iaslr UIKit`

`(lldb) ibreak 0x00000001234567 Foundation`		`// 0x00000001234567 Copied from IDA/Hopper`

`(lldb) iobjc_msgSend`

`(lldb) ishow_disassemble`


#### 3. Tips

Full enter the commad characters is not necessary , use the `Tab` keyboard key. Take `iobjc_msgSend` as an example:

`(lldb) io + [Tab] + [Enter]`

or if just only one command with prefix `io`:

`(lldb) io + [Enter]`

