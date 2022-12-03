# Compiler-Design

- Fall 2022
- Contributors: Hamila Mailee - Sepehr Ilami

In this project, we implement a one-pass compiler for a slightly modified version of C-minus, which is a simplified version of the C programming language. The compiler will include four main modules for lexical analysis, syntax analysis, semantic analysis, and intermediate code generation.

## Phase 1

In the first phase, we implement a "Scanner" to tokenize a C-minus code. Aside from that, lexical errors are detected and written in a file. After tokenizing and error handling, a symbol table is generated from the keywords and IDs present in code.
