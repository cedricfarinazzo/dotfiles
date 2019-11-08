set history save on

set $64BITS = 1

set prompt \033[31mgdb$ \033[0m

# These make gdb never pause in its output
set height 0
set width 0

# ______________process information____________
define argv
    show args
end
document argv
Print program arguments.
end


define stack
    if $argc == 0
        info stack
    end
    if $argc == 1
        info stack $arg0
    end
    if $argc > 1
        help stack
    end
end
document stack
Print backtrace of the call stack, or innermost COUNT frames.
Usage: stack <COUNT>
end


define frame
    info frame
    info args
    info locals
end
document frame
Print stack frame.
end


define func
    if $argc == 0
        info functions
    end
    if $argc == 1
        info functions $arg0
    end
    if $argc > 1
        help func
    end
end
document func
Print all function names in target, or those matching REGEXP.
Usage: func <REGEXP>
end


define lib
    info sharedlibrary
end
document lib
Print shared libraries linked to target.
end


define sig
    if $argc == 0
        info signals
    end
    if $argc == 1
        info signals $arg0
    end
    if $argc > 1
        help sig
    end
end
document sig
Print what debugger does when program gets various signals.
Specify a SIGNAL as argument to print info on that signal only.
Usage: sig <SIGNAL>
end


define threads
    info threads
end
document threads
Print threads in target.
end


define ascii_char
    if $argc != 1
        help ascii_char
    else
        # thanks elaine :)
        set $_c = *(unsigned char *)($arg0)
        if ($_c < 0x20 || $_c > 0x7E)
            printf "."
        else
            printf "%c", $_c
        end
    end
end
document ascii_char
Print ASCII value of byte at address ADDR.
Print "." if the value is unprintable.
Usage: ascii_char ADDR
end


