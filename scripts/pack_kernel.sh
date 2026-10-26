#!/bin/bash
# Wrap the built kernel into a flashable boot image with Android-Image-Kitchen (AIK-Linux).
# Always flash AIK's image-new.img (never a raw cpio). Keep a stock/last-good KERNEL image to rollback.
#   ./pack_kernel.sh <AIK dir> <base KERNEL image (last good)> <built kernel> <out.img>
set -e
AIK=$1; BASE=$2; K=$3; OUT=$4
cd "$AIK"; ./cleanup.sh --nosudo >/dev/null 2>&1 || true
cp "$BASE" base.img; ./unpackimg.sh --nosudo base.img >/dev/null
cp "$K" split_img/base.img-kernel; ./repackimg.sh --nosudo | tail -1
cp image-new.img "$OUT"; md5sum "$OUT"
echo "Flash (device in TWRP/with adb root):  adb push $OUT /data/local/tmp/ ;"
echo "  adb shell 'dd if=/data/local/tmp/$(basename $OUT) of=/dev/block/mmcblk0p30 bs=2048; sync'   # kernel partition = mmcblk0p30"
echo "Verify by reading it back and comparing md5 before rebooting."
