#!/usr/bin/env python3
"""Generates a PRODUCT_COPY_FILES block for odm/ blobs, since this
extract_utils.sh version has no native odm support."""

with open("/home/tobim6/AGS2_LOS16/work/odm-files.txt") as f:
    files = [l.strip() for l in f if l.strip()]

out = "/home/tobim6/AGS2_LOS16/lineage-16.0/vendor/huawei/AGS2/AGS2-vendor-odm.mk"
with open(out, "w") as f:
    f.write("# Copyright (C) 2026 The LineageOS Project\n"
            "#\n"
            "# Licensed under the Apache License, Version 2.0 (the \"License\");\n"
            "# you may not use this file except in compliance with the License.\n"
            "# You may obtain a copy of the License at\n"
            "#\n"
            "#      http://www.apache.org/licenses/LICENSE-2.0\n"
            "#\n"
            "# Unless required by applicable law or agreed to in writing, software\n"
            "# distributed under the License is distributed on an \"AS IS\" BASIS,\n"
            "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
            "# See the License for the specific language governing permissions and\n"
            "# limitations under the License.\n"
            "#\n"
            "# Hand-generated: lineage-16.0's extract_utils.sh has no native /odm\n"
            "# partition support, so these are plain PRODUCT_COPY_FILES into\n"
            "# $(TARGET_COPY_OUT_ODM) rather than proper PRODUCT_PACKAGES modules\n"
            "# (no symlink/multilib handling, but odm/ here is almost entirely\n"
            "# config/calibration data and a handful of libs, not binaries that\n"
            "# need HAL registration).\n\n")
    f.write("PRODUCT_COPY_FILES += \\\n")
    lines = [
        f"    vendor/huawei/AGS2/proprietary/odm/{p}:$(TARGET_COPY_OUT_ODM)/{p}"
        for p in files
    ]
    f.write(" \\\n".join(lines) + "\n")

print(f"{len(files)} odm entries -> {out}")
