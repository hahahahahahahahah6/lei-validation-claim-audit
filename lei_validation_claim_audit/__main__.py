"""Command-line interface."""
import argparse
import json
import sys
from . import __version__
from .audit import audit


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(1, '%s: error: %s\n' % (self.prog, message))


def main(argv=None):
    parser = Parser(prog='lei-validation-claim-audit')
    parser.add_argument('--version', action='version', version=__version__)
    sub = parser.add_subparsers(dest='command', required=True, parser_class=Parser)
    check = sub.add_parser('audit')
    check.add_argument('repo', nargs='?', default='.')
    check.add_argument('--fail-on', choices=('high', 'medium'), default='high')
    check.add_argument('--ignore', action='append', default=[])
    check.add_argument('--json', action='store_true')
    check.add_argument('--verbose', action='store_true')
    args = parser.parse_args(argv)
    try:
        findings = audit(args.repo, args.ignore)
    except (OSError, UnicodeError) as exc:
        print('error: %s' % exc, file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({'findings': findings}, indent=2))
    elif findings:
        for finding in findings:
            print('%s %s: %s' % (finding['severity'], finding['id'], finding['message']))
    else:
        print('PASS')
    if args.verbose and not args.json:
        print('Audited: %s' % args.repo)
    return 2 if any(f['severity'] == 'HIGH' or args.fail_on == 'medium' for f in findings) else 0


if __name__ == '__main__':
    sys.exit(main())
