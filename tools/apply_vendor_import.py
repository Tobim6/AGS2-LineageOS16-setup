import os,re,shutil,sys,collections
V=sys.argv[1]; W='/home/tobim6/AGS2_LOS16/work'
src=W+'/emui8_vendor_tree/'
files=[l.strip() for l in open(W+'/want2.txt') if l.strip()]
mk=open(V+'/Android.mk').read()
names=set(re.findall(r'^LOCAL_MODULE := (\S+)',mk,re.M))
srcs=set(re.findall(r'^LOCAL_SRC_FILES(?:_\d+)? := (\S+)',mk,re.M))
new=[]
for f in files:
    d=V+'/proprietary/'+f
    if not os.path.exists(d): new.append(f)
    os.makedirs(os.path.dirname(d),exist_ok=True)
    shutil.copy2(src+f,d)          # EMUI8 wins over HMOS-era copy
blocks=[];pk=[];skipped=[]
libs=collections.OrderedDict()
def add(name,body):
    blocks.append("include $(CLEAR_VARS)\nLOCAL_MODULE := %s\nLOCAL_MODULE_OWNER := huawei\nLOCAL_PROPRIETARY_MODULE := true\n%sLOCAL_MODULE_TAGS := optional\ninclude $(BUILD_PREBUILT)\n"%(name,body)); pk.append(name)
for f in new:
    if 'proprietary/'+f in srcs: continue
    d,b=os.path.split(f)
    if d in('lib','lib64','lib/hw','lib64/hw'):
        key=('hw/' if d.endswith('/hw') else '')+b
        libs.setdefault(key,{})[32 if d.startswith('lib/') or d=='lib' else 64]=f
    elif d.startswith('bin'):
        n=b
        if n in names: skipped.append(f);continue
        add(n,"LOCAL_SRC_FILES := proprietary/%s\nLOCAL_MODULE_CLASS := EXECUTABLES\n%s"%(f,"LOCAL_MODULE_RELATIVE_PATH := hw\n" if d=='bin/hw' else ""))
    else:
        n=re.sub(r'\.(rc|xml|bks)$','',b)
        n=('rc_' if d.startswith('etc/init') else 'perm_' if 'permissions' in d else 'emui8_')+n
        if n in names: skipped.append(f);continue
        suf=os.path.splitext(b)[1]
        rel=d[len('etc/'):]
        add(n,"LOCAL_SRC_FILES := proprietary/%s\nLOCAL_MODULE_CLASS := ETC\nLOCAL_MODULE_STEM := %s\nLOCAL_MODULE_SUFFIX :=\n%s"%(f,b,"LOCAL_MODULE_RELATIVE_PATH := %s\n"%rel if rel!='.' and d!='etc' else ""))
for key,a in libs.items():
    b=os.path.basename(key)[:-3]
    if b in names: skipped.append(key);continue
    body="LOCAL_MODULE_CLASS := SHARED_LIBRARIES\nLOCAL_MODULE_SUFFIX := .so\n"
    if 64 in a: body+="LOCAL_SRC_FILES_64 := proprietary/%s\n"%a[64]
    if 32 in a: body+="LOCAL_SRC_FILES_32 := proprietary/%s\n"%a[32]
    body+="LOCAL_MULTILIB := %s\n"%("both" if len(a)==2 else str(list(a)[0]))
    if key.startswith('hw/'): body+="LOCAL_MODULE_RELATIVE_PATH := hw\n"
    add(b,body)
tail="\n# EMUI8 vendor import (HAL services, rc, libs, permissions) - see work/tools/apply_vendor_import.py\n"+"\n".join(blocks)
mk=mk.rstrip()
assert mk.endswith('endif')
mk=mk[:-5]+tail+"\nendif\n"
open(V+'/Android.mk','w').write(mk)
open(V+'/../work/new_packages.txt','w').write("\n".join(pk))
print("new files",len(new),"modules",len(pk),"skipped",skipped)
