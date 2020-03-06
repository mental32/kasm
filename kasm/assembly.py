from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class AssemblyPreprocessor:
    section: "AssemblySection"
    __defines: Dict[str, str] = field(init=False, repr=False, default_factory=dict)

    def define(self, name, value):
        self.__defines[name] = value
        self.section.inline_asm(f"%define {name} {value}")


@dataclass
class AssemblySection:
    name: str
    stub: "AssemblyStub"
    __lines: List[str] = field(init=False, repr=False, default_factory=list)

    def __post_init__(self):
        self.preprocessor = AssemblyPreprocessor(self)

    def __enter__(self) -> "AssemblySection":
        return self

    def __exit__(self, *_):
        pass

    # Public

    def source(self) -> str:
        return "\n".join(self.__lines)

    def inline_asm(self, source: str):
        self.__lines.append(source)

    def label(self, name: str):
        self.inline_asm(f"{name!s}:")


@dataclass
class AssemblyStub:
    sections: List[AssemblySection] = field(init=False, default_factory=list)

    def section(self, name: str) -> AssemblySection:
        section = AssemblySection(stub=self, name=name)
        section.inline_asm(f"SECTION {name}\n")
        self.sections.append(section)
        return section
