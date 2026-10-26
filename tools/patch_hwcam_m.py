import sys
src, dst = sys.argv[1], sys.argv[2]
d = bytearray(open(src, 'rb').read())
for old, new in ((b'_ZN7android18CameraBufferMapper4lockEPK13native_handlejRKNS_4RectEPPv',
                  b'_ZN7android18CameraBufferMapper4lockEPK13native_handlemRKNS_4RectEPPv'),
                 (b'_ZN7android18CameraBufferMapper9lockYCbCrEPK13native_handlejRKNS_4RectEP13android_ycbcr',
                  b'_ZN7android18CameraBufferMapper9lockYCbCrEPK13native_handlemRKNS_4RectEP13android_ycbcr')):
    assert d.count(old) == 1, old
    d = d.replace(old, new)
open(dst, 'wb').write(d)
