"""vendor.huawei.hardware.wifi@1.1-service reports the soft-AP interface as "ap0", but the Hi110x driver has a single
netdev (wlan0) that changes firmware mode, so wificond never finds "ap0". Rewrite the tiny AP-name function
(returns an SSO std::string) so that it returns "wlan0". usage: patch_wifi_hal_apname.py <in> <out>"""
import struct, sys
d = bytearray(open(sys.argv[1], 'rb').read())
START = 0x18cd4
orig = [0x321f07e9, 0x321c07ea, 0x528e0c2b, 0xa900fd1f, 0xf900011f, 0x39000109, 0x39000d0a, 0x7800110b, 0x3900111f, 0xd65f03c0]
cur = list(struct.unpack_from('<10I', d, START))
assert cur == orig, [hex(x) for x in cur]
def movz(rd, imm): return 0x52800000 | (imm << 5) | rd
def movk16(rd, imm): return 0x72a00000 | (imm << 5) | rd
def strb(rt, off): return 0x39000000 | (off << 10) | (8 << 5) | rt      # strb wt,[x8,#off]
new = [movz(9, 0xa),                  # SSO size byte: 5 << 1
       movz(10, 0x6c77), movk16(10, 0x6e61),   # "wlan"
       movz(11, 0x30),                # '0'
       0xa900fd1f,                    # stp xzr,xzr,[x8,#8]
       0xf900011f,                    # str xzr,[x8]   (zeroes bytes 0..7, incl. the terminator at [6])
       strb(9, 0),                    # [x8]   = 0x0a
       0xb800110a,                    # stur w10,[x8,#1] = "wlan"
       strb(11, 5),                   # [x8+5] = '0'
       0xd65f03c0]                    # ret
struct.pack_into('<10I', d, START, *new)
open(sys.argv[2], 'wb').write(d)
