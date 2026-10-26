---
name: ags2-vxd-hw-video-decode
description: Hardware H.264 decode on AGS2 works only with the D5500_DRM IMG VXD kernel driver; how it was found and how to test it
metadata:
  type: project
---

Shipped userland `libomx_vxd.so` (HMOS and EMUI8 copies both) is built against the **D5500_DRM** variant of the IMG VXD driver (BufInfo has `i32FileDescriptor`, extra CRC/ErrorLevel/bInterlacedFields fields in `VDEC_sDecPictInfo`). Kernel `drivers/Makefile` only builds it when `BOARD_CHARGER_ENABLE_DRM=true`; plain `D5500` gives mismatched structs (buffers map 1 page long, MMU faults, then nFilledLen==0 / black video).

**Fix (committed 916dbf985 in kernel_huawei_AGS2):** copy the complete `D5500_DRM` tree from the HMOS source drop (EMUI8 drop's copy is incomplete) and select it unconditionally in `drivers/Makefile`. Image: `work/out_flashable/KERNEL-emui8-drm.img` (kernel #34), flashed and verified. No libomx_vxd swap needed (original HMOS libs in vendor source work).

**Why:** days lost on a hand-patched struct in D5500 before realising the wrong driver variant was built.
**How to apply:** test by pushing a clip to /sdcard/Movies and launching VLC via `am start ... VideoPlayerActivity` myself (user dislikes being asked to do it); success = `/proc/interrupts` goldfish_device (IRQ 289) counter rising + SurfaceView layer `activeBuffer` 1920x1088 fmt 0x300 + screencap shows frames. HEVC and the VXE encoder are untested. See [[ags2-los16-port]].
