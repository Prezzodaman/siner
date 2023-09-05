# Siner
Finds the sine or cosine of a wave file.

## How it works
First, the program takes each audio byte, and converts it to a value between 0 and 2pi. In the case of an 8-bit file, the byte is converted to a signed value first:

```(((byte+128) & 255)/255)*2*pi```

In the case of a 16-bit file, each pair of bytes is ORed together first to create a 16-bit value, which is then converted to an unsigned value:

```((((byte_low | (byte_high<<8))+32768) & 65535)/65535)*2*pi```

Then, the sine/cosine of the value is found, and the result will be a floating-point value from -1 to 1. This value is multiplied according to the wave file's bit depth. For instance, an 8-bit file will use this formula:

```floor(byte*128) & 255```

After multiplying the value by 128, the result is a signed value (-128 to 127), so it's ANDed with 255 which converts it to an unsigned byte between 0 and 255.