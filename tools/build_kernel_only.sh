#!/bin/bash
export PATH="/home/tobim6/AGS2_LOS16/work/py2shim:$PATH"
cd /home/tobim6/AGS2_LOS16/lineage-16.0
source build/envsetup.sh
lunch lineage_AGS2-userdebug
make $PWD/out/target/product/AGS2/kernel -j$(nproc)
