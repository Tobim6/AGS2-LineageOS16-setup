import sys,os,subprocess,re
root=sys.argv[1]; arch=sys.argv[2]  # proprietary dir, lib64|lib
visible=set(open(sys.argv[3]).read().split())   # libs visible from vendor ns (vndk/llndk/ndk)
have=set()
for d in (arch,arch+'/hw',arch+'/egl',arch+'/soundfx'):
    p=os.path.join(root,d)
    if os.path.isdir(p): have|=set(os.listdir(p))
missing={}
for sub,ext in ((arch,'.so'),(arch+'/hw','.so'),('bin',''),('bin/hw','')):
    p=os.path.join(root,sub)
    if not os.path.isdir(p): continue
    for f in os.listdir(p):
        fp=os.path.join(p,f)
        if not os.path.isfile(fp) or os.path.islink(fp): continue
        try: out=subprocess.run(['readelf','-d',fp],capture_output=True,text=True).stdout
        except Exception: continue
        for n in re.findall(r'NEEDED.*\[(.*)\]',out):
            if n not in have and n not in visible: missing.setdefault(n,[]).append(f)
for n,u in sorted(missing.items()): print(n,len(u),' '.join(u[:4]))
