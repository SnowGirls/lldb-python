

Start `Debugserver` and `LLDB`，attatch the process you want to debug.

## How to use

### 1. Import the scripts

`command script import ~/Path/To/breakpoint.py`

`command script import ~/Path/To/objc_msgSend.py`

Also, you can put these commands above into the file `~/.lldbinit` 


### 2. Commands example

```
(lldb) process interrupt
(lldb) help

(lldb) iobjc_msgSend
(lldb) iarguments
(lldb) ievaluate

(lldb) idisassemble

(lldb) iaslr
(lldb) iaslr UIKit

(lldb) ibreak Foundation 0x00000001234567   // 0x00000001234567 Copied from IDA/Hopper
(lldb) ibreak 0x00000001234567  // 'bt' selected frame's module is address owner (i.e Foundation)

(lldb) iraddress your.dylib 0x00000007654321 
(lldb) iraddress 0x00000007654321

(lldb) ifaddress

(lldb) iunicode $x1

```


## Tips

Full enter the commad characters is not necessary , use the `Tab` keyboard key. Take `iobjc_msgSend` as an example:

`(lldb) io + [Tab] + [Enter]`

or, if only one command with prefix `io` in lldb environment, just issue:

`(lldb) io + [Enter]`



## Explanation

#### iobjc_msgSend
Break before every `objc_msgSend` message, or stop when encounter:

`b` 、 `bl` 、 `blr` 、 `cbz` 、 `cbnz` 、 `tbnz` 、 `tbz` 、 `cmp`


#### iarguments
print the arguments before `objc_msgSend` message.

#### ievaluate
print the return value after `objc_msgSend` message.

#### idisassemble
show dissassemble around `pc`.

#### iunicode {...}
print the unicode (for example, Chinese) output.

#### iaslr [module]
print ASLR of specified module.

#### ibreak [module] {fixed_address}
set a breakpoint from fixed address.

#### iraddress [module] {fixed_address}
print the runtime address.

#### ifaddress [module] [runtime_address]
print the fixed address.


