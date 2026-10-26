#!/usr/bin/env python3
"""Make EMUI8's audio.primary.hisi.so report audio_hw_device API 2.0 instead of 3.0.

With 3.0 the P framework drives routing through create_audio_patch(), and this HAL's
implementation rejects every call (it tries to release a stale patch handle first and returns
-EINVAL), so no output device ever reaches the HAL. With 2.0 AudioFlinger falls back to the
classic routing=<device> set_parameters path, which the HAL also implements.

adev_open() contains exactly one `orr w13, wzr, #0x300` (bytes ed 07 18 32) at file offset 0x278f8.
Usage: patch_audio_primary_version.py <in.so> <out.so>
"""
import sys
src, dst = sys.argv[1:3]
d = bytearray(open(src, 'rb').read())
off = 0x278f8
if d[off:off+4] == bytes.fromhex('ed031732'):
    print("already patched")
else:
    assert d[off:off+4] == bytes.fromhex('ed071832'), d[off:off+4].hex()
    d[off:off+4] = bytes.fromhex('ed031732')   # orr w13, wzr, #0x200
open(dst, 'wb').write(d)
