---
name: ags2-camera-bringup
description: AGS2 camera works (live preview + JPEG) only with the EMUI8 camera userland on the EMUI8 kernel; list of live-only changes still to be put in source
metadata:
  type: project
---

Camera needs the **EMUI8** userland (kernel DT has huawei,binderized=1; HMOS libcamerabuffer needs /dev/hicam_buf which EMUI8 kernel lacks). The vendor `CameraDaemon hi6250 AGASSI2` hosts the HAL and registers ICameraProvider/legacy/0 itself -- do NOT add a standalone camera.provider service.

Live-on-device (NOT yet in source/vendor tree): EMUI8 files for CameraDaemon, lib*/hwcam/*, libcamerabuffer, libHWCamCfgSvr, camera.hi6250 (+patchelf NEEDED libfence_compat), camera algo libs (libispenhnc, libSmartAE, libfacedetection, libmrc_*, ...), mediacomm@2.0 libs, /vendor/etc/camera, /odm/lib64/hwcam/* (EMUI8 m-module patched: NEEDED libtinyxml2_emui8), EMUI8 isp_fw.elf + isp_dts.img (bind-mounted from /data/local/tmp via /vendor/etc/init/zz_ags2_isp_dts.rc because /vendor is too small), vendor copies of libsensor (patched to NEEDED libfence_compat), libstdc++. Backups in /data/local/tmp/hmos_cam_backup. libgui missing for libcontrastCal (minor).
Framework patches (applied in tree, saved in device_huawei_AGS2/*.patch): cameraservice ignore status during setUpVendorTags + skip flush in Camera2Client; libui allow vendor gralloc usage bits. Need `make libui libcameraservice` + push to /system/lib{,64}.
**Why:** HAL drops metadata on flush; Android 9 cameraserver flushes before createJpegStream. **How to apply:** test with Snap via `am start -a android.media.action.STILL_IMAGE_CAMERA` and `input tap 600 1780`. Related: [[ags2-vxd-hw-video-decode]].

Update: camera changes are now in vendor_huawei_AGS2 (commits eb71e8d..). isp_dts.img lives in system/etc/firmware with a build-time symlink /vendor/firmware/isp_dts.img (vendor too small; kernel only searches /system/vendor/firmware). Video recording needed SceneDetection switcher=0 in /odm/etc/camera/ippalgoconfig{,_ram2g}.xml (daemon crashed in HwaStatInfo::getFaceInfo). Recording validated: 1080p30 H.264+AAC. Test dark scenes look black (lens/lighting), not a fault.
