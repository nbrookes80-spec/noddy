"""Generate engines/constants.py from the ORIGINAL module's plain-data constants.

Only str/int/float/bool/None and list/tuple/dict/set of those are exported.
Usage: python3 -I gen_constants.py "<app .pyc>" "<output .py>"
"""
import os
import sys
import types
import pprint

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle  # noqa: E402

PLAIN = (str, int, float, bool, type(None))


def is_plain(v):
    if isinstance(v, PLAIN):
        return True
    if isinstance(v, (list, tuple, set, frozenset)):
        return all(is_plain(x) for x in v)
    if isinstance(v, dict):
        return all(is_plain(k) and is_plain(x) for k, x in v.items())
    return False


def main(pyc, out):
    mod = oracle.load_original(pyc)
    names = sorted(k for k, v in vars(mod).items()
                   if not k.startswith('__') and is_plain(v))
    lines = ['"""Constants generated from the ORIGINAL module (do not edit by hand).',
             '',
             'Regenerate with tests/gen_constants.py. Values are exact copies of the',
             'original module-level data.',
             '"""', '']
    for k in names:
        v = getattr(mod, k)
        lines.append(f'{k} = ' + pprint.pformat(v, width=100, sort_dicts=False))
        lines.append('')
    open(out, 'w').write('\n'.join(lines))
    print('exported', len(names), 'constants to', out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
