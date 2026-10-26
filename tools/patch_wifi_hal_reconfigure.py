"""vendor.huawei.hardware.wifi@1.1-service embeds the Android 8.0 WifiChip::handleChipConfiguration, which returns
ERROR_NOT_SUPPORTED when the chip is already in a mode. Android 9's HalDeviceManager reconfigures the chip (STA ->
AP) without a full stop, so the hotspot could never start. Make the 'current mode != invalid' check never fail
(8.1+ behaviour: reconfigure in place). usage: patch_wifi_hal_reconfigure.py <in> <out>"""
import sys
d = bytearray(open(sys.argv[1], 'rb').read())
OFF = 0x15410
assert d[OFF:OFF + 4] == bytes.fromhex('60000054'), 'unexpected bytes (b.eq 1541c)'  # b.eq +0xc
d[OFF:OFF + 4] = bytes.fromhex('03000014')                                           # b   +0xc
open(sys.argv[2], 'wb').write(d)
