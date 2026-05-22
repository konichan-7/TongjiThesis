#!/usr/bin/env python3
"""Count Chinese characters and ASCII words in .tex files.

Usage: python3 scripts/wordcount.py
"""
import os
import re
import sys


def strip_tex(text: str) -> str:
    # remove comments (percent not preceded by backslash)
    text = re.sub(r'(?m)(?<!\\)%.*$', '', text)

    # remove common math/code/figure environments
    envs = [
        'equation', 'align', 'align*', 'equation*', 'alignat', 'multline',
        'gather', 'eqnarray', 'displaymath', 'lstlisting', 'minted', 'verbatim',
        'tikzpicture', 'figure', 'table', 'table*'
    ]
    for env in envs:
        # build a regex that matches \begin{env} ... \end{env}
        pat = re.compile(r"\\\\begin\{" + re.escape(env) + r"\}.*?\\\\end\{" + re.escape(env.split('*')[0]) + r"\}", re.S)
        text = pat.sub('', text)

    # remove display math and inline math
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.S)
    text = re.sub(r'\$.*?\$', '', text, flags=re.S)
    text = re.sub(r'\\\[.*?\\\]', '', text, flags=re.S)

    # remove LaTeX commands like \command[...]{...} or \command
    text = re.sub(r'\\[a-zA-Z@]+(\s*\[[^\]]*\])?(\s*\{[^}]*\})?', '', text)

    # remove remaining braces
    text = re.sub(r'[\{\}]', '', text)

    return text


def count_text(text: str):
    # CJK Unified Ideographs ranges
    cjk_re = re.compile(r'[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]')
    cjk_count = len(cjk_re.findall(text))

    # ASCII words / numbers
    word_count = len(re.findall(r'[A-Za-z0-9]+', text))

    return cjk_count, word_count


def find_tex_files(root: str):
    texs = []
    skip_dirs = set(['_minted', 'tmp', '.git', 'build', 'out', 'dist', 'node_modules'])
    for dirpath, dirs, files in os.walk(root):
        parts = dirpath.split(os.sep)
        if any(p in skip_dirs for p in parts):
            continue
        for f in files:
            if f.endswith('.tex'):
                texs.append(os.path.join(dirpath, f))
    return sorted(texs)


def main(root: str = '.') -> int:
    files = find_tex_files(root)
    totals_cjk = 0
    totals_word = 0
    results = []

    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                txt = fh.read()
        except Exception:
            continue
        clean = strip_tex(txt)
        cjk, words = count_text(clean)
        results.append((fp, cjk, words))
        totals_cjk += cjk
        totals_word += words

    # print per-file and totals
    print('Per-file counts (CJK chars | ASCII words):')
    for fp, c, w in results:
        rel = os.path.relpath(fp, root)
        print(f"{rel}: {c} | {w}")

    print('\nTotals:')
    print(f'Total CJK characters: {totals_cjk}')
    print(f'Total ASCII words: {totals_word}')
    print(f'Combined total (CJK + ASCII words): {totals_cjk + totals_word}')

    return 0


if __name__ == '__main__':
    root = os.getcwd()
    sys.exit(main(root))
