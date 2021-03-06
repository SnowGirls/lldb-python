

Start `debugserver` and `LLDB`，attatch the process you want to debug.

## How to use

### 1. Import the scripts

`command script import ~/Path/To/Your/breakpoint.py`

`command script import ~/Path/To/Your/objc_msgSend.py`

Also, you can put these commands above into the file `~/.lldbinit` 

### 2. Commands

Command       | Options  | Functionality
:------------ | :------: | ----
iobjc_msgSend |          | Break before every `objc_msgSend` message.
iarguments    |          | Print arguments of `objc_msgSend` message.
ievaluate     |          | Print return value of `objc_msgSend` message.
idisassemble  |          | Show dissassemble around pc.
iunicode      | {register\|address} | Print unicode (i.e. Chinese) output.
iaslr  		  | [module] | Print ASLR of specified module.
ibreak  	  | [module]\|{fixed_address} | Set a breakpoint with a fixed address.
iraddress     | [module]\|{fixed_address} | Print the runtime/virtual address.
ifaddress  |  [module]\|[runtime_address] | Print the fixed address.

### 3. Commands examples

```
(lldb) process interrupt
(lldb) help

(lldb) iobjc_msgSend
(lldb) iarguments
(lldb) ievaluate

(lldb) idisassemble

(lldb) iaslr
(lldb) iaslr UIKit

(lldb) ibreak Foundation 0x00000001234567   // 0x00000001234567 is Copied from IDA/Hopper
(lldb) ibreak 0x00000001234567	  // (for convenience, share library omitted)
// Note, use 'bt' to check selected/top frame's module(target module/image/share library/) is this address's owner.(Take 'Foundation' for an example here)

(lldb) iraddress your.dylib 0x00000007654321 
(lldb) iraddress 0x00000007654321	// (for convenience, share library omitted)

(lldb) ifaddress your.dylib 0x00000009876543
(lldb) ifaddress 0x00000009876543	// (for convenience, share library omitted)
(lldb) ifaddress	// show current 'pc' fixed address corresponding in IDA/Hopper

(lldb) iunicode $x1
(lldb) iunicode 0x0000000abc123
(lldb) iunicode 0xffffffffa1...
```


## Explanation

#### iobjc_msgSend
Will break before every `objc_msgSend` message, or stop when encounter:

`b` 、 `bl` 、 `blr` 、 `cbz` 、 `cbnz` 、 `tbnz` 、 `tbz` 、 `cmp`

but skip `objc_release` and `objc_retainAutorelease` messages.

#### iaslr、ibreak、iraddress、ifaddress
Arguments `[module]` (aka `shared library` or `dylib` or `framework` or `targe`t or `image` some how) is optional, when current `[module]` is the address owner. 



## Tips

Full enter the commad characters is not necessary , use the `Tab` keyboard key. Take `iobjc_msgSend` as an example:

`(lldb) io + [Tab] + [Enter]`

or, if only one command with prefix `io` in lldb environment, just issue:

`(lldb) io + [Enter]`