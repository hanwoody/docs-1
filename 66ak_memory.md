# 66ak内存布局

00 6000 0000 00 7FFF FFFF 512M DDR3B data(2)(3) DDR3B data(4) DDR3B data
00 8000 0000 00 FFFF FFFF 2G DDR3A data/DDR3B data(2)(5) DDR3B data DDR3A data(6)
01 0000 0000 01 2100 FFFF 528M+64K Reserved Reserved Reserved
01 2101 0000 01 2101 01FF 512 DDR3A EMIF configuration(7) DDR3A EMIF configuration(8) DDR3A EMIF configuration(9)
01 2101 0200 07 FFFF FFFF 32G-512 Reserved Reserved Reserved
08 0000 0000 09 FFFF FFFF 8G DDR3A data DDR3A data(8) DDR3A data(9)
0A 0000 0000 FF FFFF FFFF 984G Reserved Reserved Reserved

(2) No IO coherency supported for this region (see the KeyStone II Architecture ARM CorePac User's Guide).
(3) This region is mapped to DDR3B. It is aliased of 00 8000 0000 to 00 9FFF FFFF (the first 512MB of DDR3B) if the state of DDR3A REMAP EN pin at boot time is ‘0’.
(4) This region is aliased of 00 8000 0000 to 00 9FFF FFFF (the first 512MB of DDR3B).
(5) This region is mapped to DDR3A or DDR3B depending on the state of DDR3A REMAP EN pin at boot time. If the pin is ‘1’, this region is mapped to the first 2GB of DDR3A which is aliased of 08 0000 0000 to 08 7FFF FFFF. If the pin is ‘0’, this region is mapped as 2GB of DDR3B.
(6) MPAX from SES port extends the address to this region.
(7) This region is aliased to 00 2101 0000-00 2101 01FF.
(8) Access to 40-bit address requires XMC MPAX programmation.
(9) Access to 40-bit address requires MSMC MPAX programmation. MPAX from SES port need to remap the region of 00 2101 0000-00 2101 01FF to this region.

* 8G DDR 0-2G arm linux, 其中保留两端地址: 0x3000000-0x40000000 256M opencl, 0x40000000-0x60000000 512M RapidIO,对应到dsp core 的0xc0000000-0xe0000000 空间

* 8G DDR 2-8G dsp systembios, 目前把2-4G区间划分为8个256M, 分别映射到每个dsp的0x80000000-0x90000000空间
