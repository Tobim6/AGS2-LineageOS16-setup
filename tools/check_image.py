#!/usr/bin/env python3
"""Static sanity checks of out/target/product/AGS2: (1) every ELF's DT_NEEDED resolves in the namespace it can load from,
(2) every service started by a known-good boot log is defined by an .rc in the image.
usage: check_image.py <PRODUCT_OUT> <known-good dmesg/logcat>"""
import os, re, subprocess, sys
out = sys.argv[1]; good = sys.argv[2] if len(sys.argv) > 2 else None
def needed(path):
    try:
        r = subprocess.run(['readelf', '-d', path], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return None
    return re.findall(r'\(NEEDED\)\s+Shared library: \[(.+?)\]', r)
dirs = {'lib64': [], 'lib': []}
have = {}
for part in ('system', 'vendor'):
    for sub in ('lib64', 'lib'):
        for root, _, files in os.walk(os.path.join(out, part, sub)):
            for f in files:
                have.setdefault((sub, f), []).append(os.path.join(root, f))
missing = {}
for part in ('vendor',):
    for root, _, files in os.walk(os.path.join(out, part)):
        for f in files:
            p = os.path.join(root, f)
            if os.path.islink(p) or not (f.endswith('.so') or '/bin/' in p): continue
            if not open(p, 'rb').read(4) == b'\x7fELF': continue
            n = needed(p)
            if n is None: continue
            bits = 'lib64' if ('/lib64/' in p or subprocess.run(['readelf', '-h', p], capture_output=True, text=True).stdout.count('ELF64')) else 'lib'
            for lib in n:
                if (bits, lib) not in have:
                    missing.setdefault((bits, lib), []).append(os.path.relpath(p, out))
print('== unresolved DT_NEEDED in /vendor (excluding bionic/ndk libs that live in /system):', len(missing))
for (b, lib), users in sorted(missing.items()):
    print(f'  {lib} ({b}) <- {users[0]}' + (f' (+{len(users)-1})' if len(users) > 1 else ''))
# services
defs = set()
for part in ('system', 'vendor', 'odm', 'product', 'root'):
    for root, _, files in os.walk(os.path.join(out, part)):
        for f in files:
            if f.endswith('.rc'):
                try: txt = open(os.path.join(root, f), errors='replace').read()
                except Exception: continue
                defs |= set(re.findall(r'^service\s+(\S+)\s', txt, re.M))
if good:
    started = set(re.findall(r"starting service '([^']+)'", open(good, errors='replace').read()))
    nodef = sorted(started - defs)
    print('== services started in the known-good boot but not defined in this image:', len(nodef))
    for s in nodef: print('  ', s)
