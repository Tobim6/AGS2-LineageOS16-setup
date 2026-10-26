#!/bin/bash
# Mirror vendor_huawei_AGS2 into the build tree WITHOUT preserving mtimes: the firmware blobs carry 2021 timestamps, so
# make would never re-copy a changed blob over an older obj/ intermediate (stale prebuilts end up in the image).
set -e
rsync -rlpgoD --checksum --exclude .git /home/tobim6/AGS2_LOS16/vendor_huawei_AGS2/ /home/tobim6/AGS2_LOS16/lineage-16.0/vendor/huawei/AGS2/
