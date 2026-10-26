import sys,re
s=open(sys.argv[1]).read()
for n in('android.hardware.audio','android.hardware.audio.effect'):
    a="<name>%s</name>\n        <transport>hwbinder</transport>\n        <version>2.0</version>"%n
    if a in s: s=s.replace(a,a.replace('2.0','4.0'))
if 'android.hardware.soundtrigger' not in s:
    blk="    <hal format=\"hidl\">\n        <name>android.hardware.soundtrigger</name>\n        <transport>hwbinder</transport>\n        <version>2.0</version>\n        <interface>\n            <name>ISoundTriggerHw</name>\n            <instance>default</instance>\n        </interface>\n    </hal>\n"
    i=s.index('</hal>\n')+len('</hal>\n'); s=s[:i]+blk+s[i:]
open(sys.argv[1],'w').write(s)
