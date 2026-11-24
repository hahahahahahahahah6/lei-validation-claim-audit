"""Static documentation and Python source inspection."""
import ast
import os
import re
from pathlib import Path

from .phrases import GENERIC_NAMES, LEIVALIDATION, NOLEIVALIDATION


def _pattern(phrases):
    return re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(p) for p in sorted(phrases, key=lambda p: (-len(p), p))) + r')(?!\w)')

YES = _pattern(LEIVALIDATION)
NO = _pattern(NOLEIVALIDATION)


def doc_claims(text):
    """Return whether prose contains an affirmative and/or denial phrase."""
    lines = []
    fence = None
    for line in text.splitlines():
        m = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        lines.append(line)
    yes = no = False
    for paragraph in re.split(r'\n\s*\n', '\n'.join(lines)):
        normalized = re.sub(r'\s+', ' ', paragraph.lower().replace('n\u2019t', ' not').replace("n't", ' not').replace('-', ' '))
        no |= bool(NO.search(normalized))
        yes |= bool(YES.search(NO.sub(' ', normalized)))
    return yes, no


def source_evidence(source):
    """Return whether a single Python module contains a supported call."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return False
    imports = {}
    defined = set()
    bound = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split('.')[0]
                imports[name] = alias.name if alias.asname else alias.name.split('.')[0]
                if alias.name == 'stdnum.lei' and not alias.asname:
                    imports[name] = 'stdnum'
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            for alias in node.names:
                if alias.name != '*':
                    imports[alias.asname or alias.name] = (node.module or '') + '.' + alias.name
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                bound.update(n.id for n in ast.walk(target) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store))
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars:
                    bound.update(n.id for n in ast.walk(item.optional_vars) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store))
    shadow = defined | bound
    def resolve(node):
        if isinstance(node, ast.Name):
            if node.id in shadow:
                return None
            return imports.get(node.id)
        if isinstance(node, ast.Attribute):
            base = resolve(node.value)
            return base + '.' + node.attr if base else None
        return None
    def base_name(node):
        while isinstance(node, ast.Attribute):
            node = node.value
        return node.id if isinstance(node, ast.Name) else None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            resolved = resolve(func)
            if resolved in ('stdnum.lei.validate', 'stdnum.lei.is_valid'):
                return True
            if resolved and resolved.rsplit('.', 1)[-1] in GENERIC_NAMES and resolved.rsplit('.', 1)[-1] not in defined:
                return True
        elif isinstance(func, ast.Attribute):
            base = base_name(func.value)
            if base in imports and base in shadow:
                continue
            if func.attr in defined:
                continue
            if func.attr in GENERIC_NAMES:
                return True
            if func.attr in ('validate', 'is_valid') and resolve(func.value) == 'stdnum.lei':
                return True
    return False


def audit(root='.', ignore=()):
    """Inspect a repository and return a list of finding dictionaries."""
    root = Path(root)
    if not root.is_dir() or not os.access(str(root), os.R_OK | os.X_OK):
        raise OSError('repository is not a readable directory: ' + str(root))
    ignore = tuple(p.replace('\\', '/').strip('/') for p in ignore)
    yes = no = production = tests = False
    for current, dirs, files in os.walk(str(root), followlinks=False, onerror=lambda e: (_ for _ in ()).throw(e)):
        current = Path(current)
        def excluded(path):
            rel = path.relative_to(root).as_posix()
            return path.is_symlink() or any(rel == p or rel.startswith(p + '/') for p in ignore if p)
        dirs[:] = sorted(d for d in dirs if not excluded(current / d))
        for name in sorted(files):
            path = current / name
            if excluded(path):
                continue
            rel = path.relative_to(root)
            parts = rel.parts
            if (rel.as_posix() == 'README.md' or ('docs' in parts[:-1] and path.suffix == '.md')):
                a, b = doc_claims(path.read_text(encoding='utf-8'))
                yes |= a
                no |= b
            if path.suffix != '.py' or any(p in ('fixtures', 'docs', 'examples') for p in parts[:-1]):
                continue
            is_test = 'tests' in parts[:-1] or name.startswith('test_') or name.endswith('_test.py')
            evidence = source_evidence(path.read_text(encoding='utf-8'))
            if is_test:
                tests |= evidence
            else:
                production |= evidence
    findings = []
    if yes and not production:
        findings.append({'id': 'documented-lei-validation-claim-false', 'severity': 'MEDIUM' if tests else 'HIGH', 'message': 'Documented claim has ' + ('only test evidence.' if tests else 'no production evidence.')})
    if no and production:
        findings.append({'id': 'documented-no-lei-validation-claim-false', 'severity': 'HIGH', 'message': 'Documented denial contradicts production evidence.'})
    return findings
