import sys,os,subprocess,re,functools
V=sys.argv[1]+'/lib64'; SYS=sys.argv[2]+'/lib64'; targets=sys.argv[3:]
dirs=[V,V+'/hw',V+'/egl',V+'/soundfx',SYS,SYS+'/vndk-28',SYS+'/vndk-sp-28']
@functools.lru_cache(None)
def find(n):
    for d in dirs:
        p=os.path.join(d,n)
        if os.path.isfile(p): return p
@functools.lru_cache(None)
def defs(p):
    o=subprocess.run(['nm','-D','--defined-only',p],capture_output=True,text=True).stdout
    return frozenset(l.split()[-1].split('@')[0] for l in o.splitlines() if l.strip())
@functools.lru_cache(None)
def needed(p):
    return re.findall(r'NEEDED.*\[(.*)\]',subprocess.run(['readelf','-d',p],capture_output=True,text=True).stdout)
def closure(p):
    seen={};stack=[p]
    while stack:
        x=stack.pop()
        for n in needed(x):
            q=find(n)
            if q and q not in seen: seen[q]=1; stack.append(q)
    return list(seen)
for t in targets:
    p=t if os.path.exists(t) else find(t)
    if not p: print("NOTFOUND",t); continue
    d=set()
    for q in closure(p)+[p]: d|=defs(q)
    und=[l for l in subprocess.run(['nm','-D','--undefined-only','--no-demangle',p],capture_output=True,text=True).stdout.splitlines() if l.strip() and l.split()[0]!='w']
    bad=[l.split()[-1].split('@')[0] for l in und if not l.split()[-1].endswith('@LIBC') and l.split()[-1].split('@')[0] not in d]
    bad=[b for b in bad if not b.startswith('__cxa') and not b.startswith('_Unwind') and not b.startswith('__gxx')]
    print(os.path.basename(p), len(bad), ' '.join(bad[:3]))
