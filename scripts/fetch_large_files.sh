#!/bin/bash
# Files that are too big for git: the EMUI8 ISP dts image and the Cromite WebView.
set -e
W=${1:?workdir}
# 1) ISP dts image (157 MB) -> vendor tree (built into /system/etc/firmware, linked from /vendor/firmware)
D="$W/vendor/huawei/AGS2/proprietary/system/etc/firmware"; mkdir -p "$D"
[ -f "$D/isp_dts.img" ] || curl -L -o "$D/isp_dts.img" \
  https://github.com/Tobim6/AGS2-LineageOS16-setup/releases/download/large-files/isp_dts.img
echo "5707b719c1f718f9229a34e03f3640a1  $D/isp_dts.img" | md5sum -c -
# 2) Cromite WebView 138.0.7204.97 (newest Cromite with minSdk 26; v140+ needs Android 10)
A="$W/external/chromium-webview/prebuilt/arm64/webview.apk"
echo "efc0a5c5a66055578e296fc37e6c0982  $A" | md5sum -c - 2>/dev/null || {
  curl -L -o "$A" https://github.com/uazo/cromite/releases/download/v138.0.7204.97-418943de425329115e0783375c12ee5aec36e2b6/arm64_SystemWebView.apk
  echo "efc0a5c5a66055578e296fc37e6c0982  $A" | md5sum -c -
}
# 3) install the Cromite WebView into /system instead of the product partition (the OTA does not flash product.img, the stock product partition
#    is too small and init hides /product/app). The patch lives in the device tree; GNU patch needs --follow-symlinks for repo's linkfiles.
P="$W/device/huawei/AGS2/webview/chromium-webview-system.patch"
if [ -f "$P" ] && grep -q '^LOCAL_PRODUCT_MODULE := true' "$W/external/chromium-webview/Android.mk"; then
  (cd "$W/external/chromium-webview" && patch -p1 --follow-symlinks < "$P")
fi
