#!/usr/bin/env python3
from pathlib import Path

from speedy_antlr_tool import generate

PARENT_DIR = Path(__file__).parent.absolute()

generate(
    py_parser_path=str(PARENT_DIR / "src" / "jast" / "_parser" / "JavaParser.py"),
    cpp_output_dir=str(PARENT_DIR / "_cpp_parser"),
    entry_rule_names=["compilationUnit"],
)
