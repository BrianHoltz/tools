#!/usr/bin/env python3
"""Synchronize Shuzijun's Vditor theme with IDEA, including delayed initialization."""
import argparse
import hashlib
import io
from pathlib import Path
import zipfile

MARKER = '__shuzijunIdeaAppearance__'
SYNC = '''
    // __shuzijunIdeaAppearance__: IDEA's generated stylesheet is authoritative.
    let ideaThemeReady = false;
    function applyIdeaTheme() {
        if (!ideaThemeReady) return;
        vditor.setTheme(darcula ? "dark" : "light", darcula ? "idea-dark" : "idea-light", darcula ? "dracula" : "github", vditorThemeCDN);
    }
    function syncIdeaTheme() {
        const style = document.getElementById('ideaStyle');
        if (style && /^\\s*\\.vditor(?:--dark)?\\s*\\{/.test(style.textContent)) {
            darcula = /^\\s*\\.vditor--dark\\s*\\{/.test(style.textContent);
        }
        applyIdeaTheme();
    }
    const ideaStyleObserver = new MutationObserver((records) => {
        if (records.some(record => record.target.id === 'ideaStyle' ||
            (record.target.parentElement && record.target.parentElement.id === 'ideaStyle') ||
            Array.from(record.addedNodes).some(node => node.id === 'ideaStyle'))) {
            syncIdeaTheme();
        }
    });
    ideaStyleObserver.observe(document.documentElement, {childList: true, subtree: true, characterData: true});
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) syncIdeaTheme();
    });
    window.addEventListener('pageshow', syncIdeaTheme);
'''
OLD_UPDATE = '''    function updateStyle(style, darcula) {
        let newStyle = document.createElement('style');
        newStyle.id = 'ideaStyle';
        newStyle.innerHTML = style;
        let oldStyle = document.getElementById('ideaStyle');
        oldStyle.parentNode.replaceChild(newStyle, oldStyle);
        vditor.setTheme(darcula ? "dark" : "light", darcula ? "idea-dark" : "idea-light", darcula ? "dracula" : "github", vditorThemeCDN)
    }'''
NEW_UPDATE = '''    function updateStyle(style, darkTheme) {
        let newStyle = document.createElement('style');
        newStyle.id = 'ideaStyle';
        newStyle.textContent = style;
        let oldStyle = document.getElementById('ideaStyle');
        if (oldStyle) oldStyle.parentNode.replaceChild(newStyle, oldStyle);
        else document.head.appendChild(newStyle);
        darcula = darkTheme;
        applyIdeaTheme();
    }'''


def patch_html(html):
    if MARKER in html:
        return html
    replacements = [
        ('    const darcula = "{{darcula}}" === "true";', '    let darcula = "{{darcula}}" === "true";\n' + SYNC),
        ('        after() {\n            fileValue = vditor.getValue()\n        },', '        after() {\n            fileValue = vditor.getValue();\n            ideaThemeReady = true;\n            setTimeout(syncIdeaTheme, 0);\n        },'),
        (OLD_UPDATE, NEW_UPDATE),
    ]
    for old, new in replacements:
        if html.count(old) != 1:
            raise ValueError('Unsupported template: expected exactly one patch anchor; no files changed')
        html = html.replace(old, new, 1)
    return html


def patch_jar(path, dry_run=False):
    path = path.resolve(strict=True)
    original = path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(original)) as source:
        html = source.read('template/default.html').decode()
        patched = patch_html(html)
        if patched == html:
            print(f'Already patched: {path}')
            return
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w') as target:
            target.comment = source.comment
            for entry in source.infolist():
                value = patched.encode() if entry.filename == 'template/default.html' else source.read(entry)
                target.writestr(entry, value)
    with zipfile.ZipFile(io.BytesIO(output.getvalue())) as check:
        assert check.testzip() is None
    if dry_run:
        print(f'Would patch: {path}')
        return
    backup = path.with_name(path.name + '.bak-theme-' + hashlib.sha256(original).hexdigest()[:12])
    if not backup.exists():
        with backup.open('xb') as stream:
            stream.write(original)
    if path.read_bytes() != original:
        raise RuntimeError('Plugin changed during preparation; retry from the new version')
    inode = path.stat().st_ino
    with path.open('wb') as stream:
        stream.write(output.getvalue())
    assert path.stat().st_ino == inode
    print(f'Patched: {path}\nBackup: {backup}\nRestart IDEA to load the patched plugin resources.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('jar', type=Path, help='Installed markdown-editor plugin JAR')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    patch_jar(args.jar, args.dry_run)
