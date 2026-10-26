#!/usr/bin/env python3
"""Post-processes vendor/huawei/AGS2/Android.mk after write_makefiles runs.

This LineageOS 16.0 extract_utils.sh never sets LOCAL_PROPRIETARY_MODULE/
LOCAL_PRODUCT_MODULE on the BUILD_PREBUILT stanzas it generates for
SHARED_LIBRARIES-class modules (the vendor-placement override is
literally commented out in write_packages() in that script) -- every
vendor/product .so prebuilt module is implicitly tagged "native:platform"
instead of "native:vendor"/"native:product". This went unnoticed until
libril specifically, because it's the first vendor .so with an explicit
vendor-side consumer declared elsewhere in the tree (hardware/ril/
reference-ril's LOCAL_SHARED_LIBRARIES) that triggers build/make's
check_link_type.py Treble consistency check -- "libreference-ril
(native:vendor) should not link to libril (native:platform)". The same
latent mismatch exists on all ~278 other SHARED_LIBRARIES stanzas in this
file; fixing just libril would only mask the next one that happens to
get a consumer.

Scans every "include $(CLEAR_VARS)" ... "include $(BUILD_PREBUILT)"
stanza; for ones with LOCAL_MODULE_CLASS := SHARED_LIBRARIES, inserts
LOCAL_PROPRIETARY_MODULE := true (vendor) or LOCAL_PRODUCT_MODULE := true
(product) right after LOCAL_MODULE_OWNER, based on whether its
LOCAL_SRC_FILES* path contains "proprietary/product/".
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/tobim6/AGS2_LOS16/lineage-16.0/vendor/huawei/AGS2/Android.mk"

with open(path) as f:
    text = f.read()

stanza_re = re.compile(
    r"(include \$\(CLEAR_VARS\)\n.*?include \$\(BUILD_PREBUILT\)\n)",
    re.DOTALL)

fixed = 0

def patch(m):
    global fixed
    stanza = m.group(1)
    if "LOCAL_MODULE_CLASS := SHARED_LIBRARIES" not in stanza:
        return stanza
    if "LOCAL_PROPRIETARY_MODULE" in stanza or "LOCAL_PRODUCT_MODULE" in stanza:
        return stanza
    is_product = "proprietary/product/" in stanza
    flag = "LOCAL_PRODUCT_MODULE := true\n" if is_product \
        else "LOCAL_PROPRIETARY_MODULE := true\n"
    fixed += 1
    return stanza.replace(
        "LOCAL_MODULE_OWNER := huawei\n",
        "LOCAL_MODULE_OWNER := huawei\n" + flag,
        1)

text = stanza_re.sub(patch, text)

with open(path, "w") as f:
    f.write(text)

print(f"fix_prebuilt_partition_flags: patched {fixed} SHARED_LIBRARIES stanzas in {path}")
