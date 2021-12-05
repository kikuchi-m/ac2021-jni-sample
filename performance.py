#!/usr/bin/env python

import argparse
import datetime as dt
import os
import pathlib
import re
import shutil
import subprocess
import sys

from math import isnan

ROOT_DIR = pathlib.Path(__file__).absolute().parent
PROJECTS = [
    'perform-array',
    'perform-stream',
    'perform-stream-chunk',
]


def main(argv):
    p = argparse.ArgumentParser()
    subp = p.add_subparsers(dest='cmd', required=True)

    pre = subp.add_parser('prepare')
    pre.add_argument('--variant', default='release', choices=['debug', 'release'])

    perf = subp.add_parser('perform')
    perf.add_argument('-n', '--count', default=3, choices=list(range(1, 6)))
    perf.add_argument('-s', '--data-size', default=1000000, type=int)
    perf.add_argument('-c', '--chunk-size', default=10000, type=int)
    perf.add_argument('-m', '--heap', default=256, type=int, help='unit MB')
    perf.add_argument('-f', '--output-format', default='console', choices=['console', 'md-table'])

    c = subp.add_parser('cross')
    c.add_argument('-f', '--output-format', default='console', choices=['console', 'md-table'])

    artifacts = ROOT_DIR / 'artifacts'
    print(artifacts)
    artifacts.mkdir(exist_ok=True)

    args = vars(p.parse_args(argv))
    {
        'prepare': prepare,
        'perform': perform,
        'cross': perform_cross,
    }[args.pop('cmd')](output_dir=artifacts, **args)

    return 0


def prepare(variant, output_dir):
    build_native(variant, output_dir)
    build_app(output_dir)


def gradle(*args):
    return ['./gradlew', *args]


def build_native(variant, output_dir):
    assemble = {
        'debug': 'assembleDebug',
        'release': 'assembleRelease',
    }[variant]

    cmd = gradle(f'lib-native:{assemble}')
    print('[', *cmd, ']')
    proc = subprocess.run(cmd, cwd=ROOT_DIR)
    proc.check_returncode()

    name = 'jni-performance-sample'
    pf = {
        'linux': ('linux', 'lib', '.so'),
        'darwin': ('macos', 'lib', '.dylib')
    }[sys.platform]
    lib = ROOT_DIR / 'lib-native' / 'build' / 'lib' / 'main' / variant / pf[0] / f'{pf[1]}{name}{pf[2]}'
    dst = output_dir / lib.name
    print('copy', lib, '->', dst)
    shutil.copy2(lib, dst)


def build_app(output_dir):
    tasks = [f'app:{p}:assemble' for p in PROJECTS]
    cmd = gradle(*tasks)
    print('[', *cmd, ']')
    proc = subprocess.run(cmd, cwd=ROOT_DIR)
    proc.check_returncode()

    lib_jni = ROOT_DIR / 'lib-jni' / 'build' / 'libs' / 'lib-jni.jar'
    artifacts = [ROOT_DIR / 'app' / p / 'build' / 'libs' / f'{p}.jar' for p in PROJECTS]
    for a in [*artifacts, lib_jni]:
        dst = output_dir / a.name
        print('copy', a, '->', dst)
        shutil.copy2(a, dst)


def perform(output_dir, count, data_size, chunk_size, heap, output_format, output_file=sys.stdout):
    lib_path = f'-Djava.library.path={output_dir}'
    heap_opt = f'-Xmx{heap}m'
    time_p = re.compile('^([0-9.]+)S.*')
    results = {t: [float('NaN') for _ in range(count)] for t in PROJECTS}

    for target in PROJECTS:
        cmd = ['java', lib_path, heap_opt, '-jar', f'{target}.jar', str(data_size), str(chunk_size)]
        n = dt.datetime.now().strftime('%H:%M:%S')
        print('[', *cmd, ']', f'({n})')

        for trial in range(count):
            fn = output_dir / f'{target}.d{data_size}.c{chunk_size}.h{heap}.{trial}'
            ef = f'{fn}.err.log'
            of = f'{fn}.log'
            with open(ef, 'w') as efp, open(of, 'wb') as ofp:
                proc = subprocess.Popen(cmd, cwd=output_dir, stdout=subprocess.PIPE, stderr=efp)
                for line in proc.stdout:
                    ofp.write(line)
                    m = time_p.match(line.decode())
                    if m is not None:
                        results[target][trial] = float(m.group(1))

    def dump(*args, **kwargs):
        print(*args, file=output_file, **kwargs)

    title = f'## Data {data_size} / Chunk {chunk_size} / Heap {heap}'
    {
        'console': dump_console,
        'md-table': dump_md,
    }[output_format](title, results, count, dump)


def dump_console(title, results, count, dump):
    sep = ' |'
    sepw = 2
    end = sep + os.linesep
    col0 = 'metrics'
    nw = max([len(p) for p in [*PROJECTS, col0]]) + 3
    vw = 8 + 1
    w = nw + sepw + (vw + sepw) * (count + 1)

    dump(title)
    dump('-' * w)
    dump(f'| {col0}'.ljust(nw),
         *[str(c).rjust(vw) for c in range(1, count + 1)],
         'avg.'.rjust(vw),
         sep=sep, end=end)
    dump('|' + '-' * (nw - 1), *['-' * vw for _ in range(count + 1)],
         sep=sep, end=end)
    for p in PROJECTS:
        res = results[p]
        valids = [v for v in res if not isnan(v)]
        dump(f'| {p}'.ljust(nw),
             *[('NaN' if isnan(v) else str(v)).rjust(vw) for v in res],
             ('NaN' if len(valids) == 0 else str(sum(valids) / len(valids)))[:vw - 1].rjust(vw),
             sep=sep, end=end)
    dump('-' * w)


def dump_md(title, results, count, dump):
    sep = ' | '
    end = ' |' + os.linesep
    col0 = 'metrics'

    dump(title)
    dump(col0, *[str(c) for c in range(1, count + 1)], 'avg.',
         sep=sep, end=end)
    dump(*['---' for _ in range(count + 2)],
         sep=sep, end=end)
    for p in PROJECTS:
        res = results[p]
        valids = [v for v in res if not isnan(v)]
        dump(p,
             *['NaN' if isnan(v) else str(v) for v in res],
             ('NaN' if len(valids) == 0 else str(sum(valids) / len(valids)))[:8],
             sep=sep, end=end)


def perform_cross(output_dir, output_format):
    common = {
        'count': 5,
        'output_dir': output_dir,
        'output_format': output_format,
    }
    ds = [
        (10 ** 6),
        (10 ** 6) * 2,
        (10 ** 6) * 3,
        (10 ** 6) * 5,
        (10 ** 7),
        (10 ** 7) * 2,
    ]
    cs = [
        (10 ** 3),
        (10 ** 3) * 5,
        (10 ** 4),
        (10 ** 4) * 2,
        (10 ** 4) * 5,
        (10 ** 5),
    ]
    heap = [256, 512, 1024]
    args = [{'data_size': d, 'chunk_size': c, 'heap': h, **common}
            for d in ds
            for c in cs
            for h in heap]
    with open(output_dir / 'perform-cross.log', 'w') as ofp:
        for a in args:
            perform(output_file=ofp, **a)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
