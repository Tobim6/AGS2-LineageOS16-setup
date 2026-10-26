#!/bin/bash
# Usage: ./setup.sh <workdir>   -- sync LineageOS 16.0 + the AGS2 repos and fetch the large files
set -e
W=${1:?workdir}
mkdir -p "$W" && cd "$W"
[ -d .repo ] || repo init -u https://github.com/LineageOS/android -b lineage-16.0 --depth=1
mkdir -p .repo/local_manifests
cp "$(dirname "$0")/../local_manifests/ags2.xml" .repo/local_manifests/
repo sync -c -j8 --force-sync --no-clone-bundle
"$(dirname "$0")/fetch_large_files.sh" "$W"
echo "Done. Next: cd $W && source build/envsetup.sh && lunch lineage_AGS2-userdebug && mka bacon  (see README)"
