# LineageOS 16.0 for the Huawei MediaPad T5 (AGS2 / "Dallas", Kirin 659 / hi6250)

Setup help and glue for the AGS2 port. Everything needed to build lives in these repos (all under
[Tobim6](https://github.com/Tobim6)):

| Repo | Path in tree | Branch |
|---|---|---|
| `android_device_huawei_AGS2` | `device/huawei/AGS2` | `lineage-16.0` |
| `android_device_huawei_hi6250-common` (fork) | `device/huawei/hi6250-common` | `lineage-16.0` |
| `android_kernel_huawei_AGS2` | `kernel/huawei/AGS2` | `lineage-16.0` |
| `proprietary_vendor_huawei_AGS2` | `vendor/huawei/AGS2` | `lineage-16.0` |
| `android_frameworks_av_los16` (fork) | `frameworks/av` | `lineage-16.0-ags2` |
| `android_frameworks_native_los16` (fork) | `frameworks/native` | `lineage-16.0-ags2` |
| `android_frameworks_opt_net_wifi_los16` (fork) | `frameworks/opt/net/wifi` | `lineage-16.0-ags2` |

Large files that cannot live in git are fetched by `scripts/fetch_large_files.sh`
(`isp_dts.img` from this repo's `large-files` release, Cromite WebView from upstream).

## Quick start

```sh
git clone https://github.com/Tobim6/AGS2-LineageOS16-setup && cd AGS2-LineageOS16-setup
scripts/setup.sh ~/lineage-16.0        # repo init/sync + local manifest + large files
cd ~/lineage-16.0 && source build/envsetup.sh && lunch lineage_AGS2-userdebug && mka bacon
```
The 16.0 build needs Python 2 (`python`/`python2` must resolve to python2.7; a small PATH shim works).

## Boot chain: EMUI8, not HarmonyOS (important)
HarmonyOS 2.0's bootloader rejects custom kernels, so the **boot chain (xloader/fastboot/kernel/ramdisk/TEEOS) is the
EMUI8 one** (Linux 4.4.23, ramdisk-based, not system-as-root). Only the Android userland is LineageOS 16.
`docs/PORT_NOTES.md` has the full history, partition table and the exact per-partition flash state.
Bootloader cannot be unlocked with fastboot; images are written with `dd` from TWRP/adb root (see below).

## Kernel
`make bootimage` does **not** rebuild the kernel. Use `scripts/build_kernel.sh` (from the tree root), then
`scripts/pack_kernel.sh` (Android-Image-Kitchen wrapper) and `dd` the result to the kernel partition (`mmcblk0p30`),
reading it back to check the md5 before rebooting. Keep the last known-good `KERNEL-*.img` for rollback.
Notable kernel changes: `D5500_DRM` IMG VXD video-decoder driver selected (matches the shipped userland ABI),
wifi EAPOL TX fix for the AOSP wpa_supplicant.

## What works (verified on an AGS2-W09)
Boot to launcher, USB/adb, wifi, Bluetooth, audio, landscape default (+ boot animation), hardware TEE,
hardware H.264/HEVC video decoding (VXD), back camera preview, JPEG capture and 1080p30 video recording,
Cromite WebView 138, hardware Bluetooth/wifi MAC addresses (from NV via the oeminfo server), Wi-Fi hotspot.

## Known gaps
Front camera and camera video/ZSL modes beyond the basics untested; radio/telephony; `perfgenius`;
`libcontrastCal` (needs libgui); no `odm.img` rule in this 16.0 `build/make` (ODM files are installed via
`AGS2-vendor-odm.mk`); first full image build/flash from these repos is still to be validated -- see
`docs/PORT_NOTES.md` ("never rebuilt system.img" section) before flashing, and take a TWRP backup first.

## Layout
- `local_manifests/ags2.xml` -- repo local manifest (replaces frameworks/av and native with the patched forks)
- `scripts/` -- setup, large-file fetch, kernel build/pack
- `patches/` -- the framework patches as plain diffs (already contained in the forks)
- `tools/` -- extraction/analysis helpers (EROFS VLE extractor, vendor makefile generators, symbol checkers,
  ELF patchers, Ghidra headless scripts)
- `docs/` -- notes: port history/gotchas, camera bring-up, video decode

## Camera in one paragraph
The EMUI8 camera userland is used (the kernel DT sets `huawei,binderized=1`). `CameraDaemon hi6250 AGASSI2` hosts the HAL
and registers `ICameraProvider/legacy/0` itself. Android 9's cameraserver needs two tweaks (forks above): ignore status
callbacks during `setUpVendorTags()` and skip the HAL flush before draining. `libui` must pass the HAL's vendor gralloc
usage bits. `SceneDetection` is disabled in `/odm/etc/camera/ippalgoconfig*.xml` (crashes the daemon on video).
Details: `docs/CAMERA_NOTES.md`.
