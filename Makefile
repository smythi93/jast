# Fandango Makefile. For development only.

# Settings
MAKEFLAGS=--warn-undefined-variables

# Programs
PYTHON = python
PYTEST = pytest
ANTLR = antlr
BLACK = black
PIP = pip
SED = sed
PAGELABELS = $(PYTHON) -m pagelabels


# Default targets
web: requirements.txt parser html
all: web pdf

.PHONY: web all parser install dev-tools docs html latex pdf


## Requirements

requirements.txt:	pyproject.toml
	pip-compile $<

# Install tools for development
UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
# Mac
SYSTEM_DEV_TOOLS = antlr
SYSTEM_DEV_INSTALL = brew install
else
# Linux
SYSTEM_DEV_TOOLS = antlr
SYSTEM_DEV_INSTALL = apt-get install
endif


dev-tools: system-dev-tools
	pip install -U black

system-dev-tools:
	$(SYSTEM_DEV_INSTALL) $(SYSTEM_DEV_TOOLS)


## Parser

PARSER = src/jast/_parser
CPP_PARSER = _cpp_parser
LEXER_G4 = antlr/java/JavaLexer.g4
PARSER_G4 = antlr/java/JavaParser.g4

PARSERS = \
	$(PARSER)/JavaLexer.py \
	$(PARSER)/JavaParser.py \
	$(PARSER)/JavaParserVisitor.py

parser: $(PARSERS)

$(PARSERS) &: $(LEXER_G4) $(PARSER_G4)
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER) \
		-visitor -no-listener $(LEXER_G4) $(PARSER_G4)
	rm $(PARSER)/JavaParserListener.py
	$(BLACK) $(PARSER)

cpp-parser: $(LEXER_G4) $(PARSER_G4)
	$(ANTLR) -Dlanguage=Cpp -Xexact-output-dir -o $(CPP_PARSER) \
		-visitor -no-listener $(LEXER_G4) $(PARSER_G4)
	$(PYTHON) generate-parser.py
	$(BLACK) $(PARSER)



## Test
test tests:
	$(PIP) install -e . --config-settings=build_ext=-j4
	$(PYTEST) tests


## Installation

install:
	$(PIP) install -e . --config-settings=build_ext=-j4