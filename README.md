# KASM
## An assembly stub code generation tool for kernels

## Index

 - [Brief](#Brief)
 - [Examples](#Examples)

## Brief

## Examples

### The barest of bones

Using the following script:

```py
from kasm import OutputStub, Architecture, Multiboot2

head = OutputStub(
    multiboot_info=Multiboot2(arch=Architecture.i386),
    target=Architecture.x86_64
)

print(head.generate_assembly(mangle_names=False))
```

kasm will generate the fillowing bare minimum NASM assembly:

```nasm
SECTION .kasm.multiboot

%define _kasm_multiboot_header_length (_kasm_multiboot_header_end - _kasm_multiboot_header_start)

_kasm_multiboot_header_start:
    dd 0xe85250d6
    dd 0
    dd _kasm_multiboot_header_start
    dd 0x100000000 - (0xe85250d6 + 0 + _kasm_multiboot_header_length)
    dw 0
    dw 0
    dd 0
_kasm_multiboot_header_end:

SECTION .kasm

BITS 64

_kasm_start:
_kasm_halt_spin:
    hlt
    jmp _kasm_halt_spin
```
