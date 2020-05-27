#!/usr/bin/env python3
import os
from pathlib import Path

COMPILE_DIR = Path(__file__).parent

# must be relative b/c links on site are relative
os.chdir(COMPILE_DIR.parent)
ROOT_DIR = Path('.')


def main():
    headings, emoji = get_emoji_paths()
    emoji_html = format_emoji(headings, emoji)
    save_index(emoji_html)

def get_emoji_paths(dir=ROOT_DIR / 'emoji'):
    emoji = {}
    headings = {}
    for path in dir.iterdir():
        if path.name == 'private':
            continue
        if path.is_dir():
            headings[path.name] = get_emoji_paths(path)
        else:
            emoji[path.stem] = str(path)
    return headings, emoji


def format_emoji(headings, emoji):
    with open(COMPILE_DIR / 'emoji-tile.partial.html', 'r') as fp:
        template = fp.read()

    snippets = ['  <div class="emoji-list">']
    for name, path in sorted(emoji.items()):
        snippets.append(template.format(name=name, path=path))
    snippets.append('  </div>')

    for name, sub_emoji in sorted(headings.items()):
        snippets.append(f'  <h2 id={name}>{name}</h2>')
        snippets.append(format_emoji(*sub_emoji))

    return os.linesep.join(snippets)


def save_index(emoji_html):
    with open(COMPILE_DIR / 'template.html', 'r') as fp:
        template = fp.read()

    with open(ROOT_DIR / 'readme.md', 'r') as fp:
        disclaimer = fp.read()

    with open(ROOT_DIR / 'index.html', 'w') as fp:
        fp.write(template.format(emoji=emoji_html, disclaimer=disclaimer))


if __name__ == '__main__':
    main()
