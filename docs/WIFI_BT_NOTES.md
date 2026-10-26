# Hotspot and hardware MAC addresses

## Bluetooth/wifi MAC
`mac_addr_normalization` reads `MACBT`/`MACWLAN` from NV through `libnvme`, which talks to the `oeminfo_nvm_server`
socket (`/dev/socket/oeminfo_nvm`). Our (LineageOS) ramdisk has no `/sbin/oeminfo_nvm_server`, so every NV read failed and the tool
fell back to random addresses. `init.hi6250.rc` now starts `/vendor/bin/oeminfo_nvm_server` at `post-fs`, and
`ro.bt.bdaddr_path=/data/misc/bluedroid/macbt` / `ro.wifi.wifiaddr_path=/data/misc/wifi/macwifi` point the stack at the files.

## Soft AP (hotspot)
Three independent problems:
1. The wifi HAL is Android 8.0's: `configureChip` fails with NOT_SUPPORTED when the chip is already in a mode, but the Android 9
   framework reconfigures in place. Fix: `frameworks/opt/net/wifi` fork tears down the client iface first so the HAL is stopped
   and restarted before the AP iface is created.
2. The HAL names the AP iface `ap0`; the Hi110x driver only has `wlan0` (firmware mode switch). `tools/patch_wifi_hal_apname.py`
   rewrites the tiny name function in `vendor.huawei.hardware.wifi@1.1-service` to return `wlan0`.
3. The Android 9 framework talks to a HIDL `hostapd`; the EMUI8 one has none. Build the AOSP `hostapd` (board config:
   `WPA_SUPPLICANT_VERSION`, `BOARD_HOSTAPD_DRIVER`, `WPA_BUILD_HOSTAPD`), drop the legacy `service hostapd` from the vendor
   connectivity rc files and declare `android.hardware.wifi.hostapd@1.0` in the vendor *and ODM* manifests (the ODM manifest wins).
   The vendor `libwpa_client` prebuilt is renamed `libwpa_client_emui8` to avoid colliding with wpa_supplicant_8.
Tested: hostapd reaches `AP-ENABLED` and the status bar shows the hotspot icon; a real client connection has not been tested.
