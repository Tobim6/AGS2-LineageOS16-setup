#!/bin/bash
# `make bootimage` says "no work to do" and never rebuilds the kernel. Use this instead (run from the tree root).
# py2shim: a directory with `python`/`python2` wrappers pointing at python2.7 (the 16.0 build needs it).
export PATH="$PWD/py2shim:$PATH"
source build/envsetup.sh
lunch lineage_AGS2-userdebug
rm -f out/target/product/AGS2/obj/KERNEL_OBJ/arch/arm64/boot/Image.gz out/target/product/AGS2/kernel
make "$PWD/out/target/product/AGS2/kernel" -j"$(nproc)"
