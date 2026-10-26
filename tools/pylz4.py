"""Minimal pure-Python LZ4 block decompressor, matching the vanilla
format used by fs/erofs/generic/lz4.h (standard LZ4 block format:
1-byte token, high nibble literal-length, low nibble match-length,
RUN_MASK/ML_MASK=15 extension bytes, 2-byte LE offset)."""


def lz4_decompress(src: bytes, max_out: int) -> bytes:
    out = bytearray()
    i = 0
    n = len(src)
    while i < n:
        token = src[i]
        i += 1
        lit_len = token >> 4
        if lit_len == 15:
            while True:
                b = src[i]
                i += 1
                lit_len += b
                if b != 255:
                    break
        out += src[i:i + lit_len]
        i += lit_len
        if i >= n:
            break  # end of block (trailing literals only)
        offset = src[i] | (src[i + 1] << 8)
        i += 2
        match_len = (token & 0xF) + 4
        if (token & 0xF) == 15:
            while True:
                b = src[i]
                i += 1
                match_len += b
                if b != 255:
                    break
        start = len(out) - offset
        for k in range(match_len):
            out.append(out[start + k])
        if len(out) > max_out:
            raise ValueError("output exceeded max_out")
    return bytes(out)
