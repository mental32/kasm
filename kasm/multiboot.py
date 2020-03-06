from dataclasses import dataclass, field, InitVar

from kasm import Architecture

__all__ = ("Multiboot2",)


@dataclass
class Multiboot2:
    """A class representing some multiboot2 compatability.

    An OS image must contain an additional header called Multiboot2 header,
    besides the headers of the format used by the OS image. The Multiboot2
    header must be contained completely within the first 32768 bytes of the OS
    image, and must be 64-bit aligned. In general, it should come as early as
    possible, and may be embedded in the beginning of the text segment after
    the real executable header.
    """

    arch: InitVar[Architecture]

    architecture: int = field(init=False, default=None)
    magic: str = field(init=False, default=hex(0xE85250D6))

    def __post_init__(self, arch: Architecture):
        if not arch in (Architecture.i386, Architecture.MIPS):
            raise ValueError("Architecture target must be either i386 or MIPS")

        self.architecture = 0 if arch == Architecture.i386 else 4
