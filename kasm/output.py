from dataclasses import dataclass
from typing import Optional

from kasm import Architecture, AssemblyStub


@dataclass
class OutputStub:
    target: Architecture
    multiboot_info: Optional["Multiboot2"] = None

    def generate_assembly(self, *, mangle_names: bool = True) -> str:
        """Generate the source assembly represented by the stub."""
        source = AssemblyStub()

        if self.multiboot_info is not None:
            multiboot_info = self.multiboot_info

            with source.section(".kasm.multiboot") as cursor:
                cursor.preprocessor.define(
                    "_kasm_multiboot_header_length",
                    "(_kasm_multiboot_header_end - _kasm_multiboot_header_start)\n",
                )

                cursor.label("_kasm_multiboot_header_start")

                multiboot_info_magic = f"{multiboot_info.magic}"
                multiboot_info_arch = f"{multiboot_info.architecture}"

                multiboot_info_fields = [
                    multiboot_info_magic,
                    multiboot_info_arch,
                    "_kasm_multiboot_header_length",
                ]

                header_values = [
                    multiboot_info_magic,
                    multiboot_info_arch,
                    f"_kasm_multiboot_header_start",
                    f"0x100000000 - ({' + '.join(multiboot_info_fields)})",
                ]

                for header_value in header_values:
                    cursor.inline_asm(f"    dd {header_value}")

                tags = [(0, 0, 0)]

                for kind, flags, size, in tags:
                    cursor.inline_asm(f"    dw {kind}")
                    cursor.inline_asm(f"    dw {flags}")
                    cursor.inline_asm(f"    dd {size}")

                cursor.label("_kasm_multiboot_header_end")

        with source.section(".kasm") as cursor:
            cursor.inline_asm("BITS 64\n")

            cursor.label("_kasm_start")

            cursor.label("_kasm_halt_spin")
            cursor.inline_asm("    hlt")
            cursor.inline_asm("    jmp _kasm_halt_spin")

        return "\n".join(map((lambda x: f"{x.source()}\n"), source.sections)).strip()
