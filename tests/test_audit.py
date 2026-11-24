import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from lei_validation_claim_audit.audit import audit, doc_claims, source_evidence
from lei_validation_claim_audit.__main__ import main
from lei_validation_claim_audit.phrases import GENERIC_NAMES, LEIVALIDATION, NOLEIVALIDATION


class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual((len(set(LEIVALIDATION)), len(set(NOLEIVALIDATION)), len(set(GENERIC_NAMES))), (50, 24, 24))
        for phrase in LEIVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertEqual(doc_claims(phrase), (True, False))
        for phrase in NOLEIVALIDATION:
            with self.subTest(phrase=phrase):
                self.assertTrue(any(p in phrase for p in LEIVALIDATION))
                self.assertEqual(doc_claims(phrase), (False, True))
        self.assertEqual(doc_claims('```\nvalidate lei\n```\n\n`lei validation`'), (True, False))
        self.assertEqual(doc_claims('prevalidate lei suffix'), (False, False))
        self.assertEqual(doc_claims("doesn't validate-lei"), (False, True))

    def test_library_routes(self):
        for method in ('validate', 'is_valid'):
            for code in ('import stdnum.lei\nstdnum.lei.%s(x)', 'import stdnum.lei as le\nle.%s(x)', 'from stdnum import lei\nlei.%s(x)', 'import stdnum\nstdnum.lei.%s(x)', 'from stdnum.lei import %s\n%s(x)', 'from stdnum.lei import %s as v\nv(x)'):
                count = code.count('%s')
                with self.subTest(method=method, code=code):
                    self.assertTrue(source_evidence(code % ((method,) * count)))

    def test_generic_routes_and_shadow(self):
        for name in GENERIC_NAMES:
            for code in ('obj.%s(x)' % name, 'from other import %s as v\nv(x)' % name, 'obj = make()\nobj.%s(x)' % name):
                with self.subTest(code=code):
                    self.assertTrue(source_evidence(code))
            for code in ('%s(x)' % name, 'def %s(x): pass\nobj.%s(x)' % (name, name), 'from other import %s as v\nv = 1\nv(x)' % name):
                with self.subTest(code=code):
                    self.assertFalse(source_evidence(code))
        for code in ('from stdnum import lei\nlei = 1\nlei.validate(x)', 'from stdnum import lei\nwith ctx() as lei:\n lei.validate(x)', 'from stdnum import lei\nasync def f():\n async with ctx() as lei:\n  lei.validate(x)', 'from stdnum.lei import validate\ndef validate(x): pass\nvalidate(x)'):
            with self.subTest(code=code):
                self.assertFalse(source_evidence(code))

    def test_not_evidence(self):
        cases = ['import stdnum.lei', 'lei(x)', 'validate(x)', 'is_valid(x)', 'compact(x)', 'obj.lei(x)', 'obj.validate(x)', 'obj.is_valid(x)', 'obj.compact(x)', 'import stdnum.lei\nstdnum.lei.compact(x)', 'from stdnum.iso7064 import mod_97_10\nmod_97_10.validate(x)', 'mod_97_10.checksum(x)', 'mod_97_10.calc_check_digits(x)', 're.match(pattern, x)', 're.search(pattern, x)', 're.fullmatch(pattern, x)', 'len(x) == 20', 'x[:4] in lou', 'gleif.lookup(x)', 'api.isin_to_lei(x)', 'api.register_lei(x)', 'validators.lei(x)', '"validate lei"', '# lei validation', 'obj.validate_lei', 'subprocess.run(["validate lei"])', 'def broken(:']
        for code in cases:
            with self.subTest(code=code):
                self.assertFalse(source_evidence(code))
        self.assertFalse(source_evidence('from stdnum import lei'))
        self.assertFalse(source_evidence('lei.validate(x)'))

    def test_findings_and_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text('validate lei', encoding='utf8')
            self.assertEqual(audit(root)[0]['severity'], 'HIGH')
            (root / 'tests').mkdir()
            (root / 'tests' / 'test_it.py').write_text('obj.validate_lei(x)', encoding='utf8')
            self.assertEqual(audit(root)[0]['severity'], 'MEDIUM')
            for folder in ('fixtures', 'docs', 'examples'):
                (root / folder).mkdir()
                (root / folder / 'code.py').write_text('obj.validate_lei(x)', encoding='utf8')
            self.assertEqual(audit(root)[0]['severity'], 'MEDIUM')
            (root / 'src.py').write_text('obj.validate_lei(x)', encoding='utf8')
            self.assertEqual(audit(root), [])
            (root / 'README.md').write_text('no lei validation', encoding='utf8')
            self.assertEqual(audit(root)[0]['severity'], 'HIGH')
            self.assertEqual(audit(root, ['src.py']), [])
            (root / 'src.py').unlink()
            (root / 'link.py').symlink_to(root / 'tests' / 'test_it.py')
            self.assertEqual(audit(root), [])

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            Path(tmp, 'README.md').write_text('validate lei', encoding='utf8')
            self.assertEqual(main(['audit', tmp, '--json']), 2)
            self.assertEqual(main(['audit', tmp, '--ignore', 'README.md', '--verbose']), 0)
            with self.assertRaises(SystemExit) as caught:
                with contextlib.redirect_stderr(io.StringIO()):
                    main(['audit', tmp, '--fail-on', 'HIGH'])
            self.assertEqual(caught.exception.code, 1)
