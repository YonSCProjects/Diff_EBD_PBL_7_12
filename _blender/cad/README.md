# _blender/cad — real component models

Fourteen CAD outlines from the KiCad `packages3D` library, vendored so the figure pipeline builds
without a network. They replace the boxes and cylinders that used to stand in for through-hole
parts, which is what made a header read as a slotted block and a DIP as a slab with square stubs.

| file | part | used on |
| --- | --- | --- |
| `dip28.wrl` | DIP-28, 0.6″ | ATmega328P on the Uno |
| `dip8.wrl` | DIP-8 | LM393 on the TCRT5000 carrier |
| `sock1x06/08/10.wrl` | female header strips | the Uno's four header runs |
| `hdr1x08/1x15/2x03.wrl` | male pin strips | L298N logic, ESP32 edges, ICSP |
| `cap63.wrl` | 6.3 mm radial electrolytic | the Uno's two caps |
| `xtal.wrl` | HC-49 crystal | *not used* — KiCad's is the tall vertical variant |
| `pot.wrl` | Bourns 3296W trimmer | *not used* — same reason, 17 mm standing proud |
| `btn.wrl` | 6 mm tact switch | Uno reset, ESP32 BOOT/EN |
| `sot223.wrl` | SOT-223 | the Uno's 5 V regulator |
| `barrel.wrl` | 2.1 mm DC jack | the Uno's power jack |

`wrl.py` reads them (Blender as a Python module has no VRML importer, and the subset KiCad writes
is small). `cadparts.py` fixes each part's real millimetre size and its colours; every strip
package in this library runs along Y, which is why the call sites turn them 90°.

Three parts on these boards are still built by hand in `pcb.py`, because KiCad publishes nothing
this pipeline can read for them: the USB-B receptacle, the micro-USB, and the 5.08 mm screw
terminal. They are built up from their real features rather than blocked out.

## Licence

KiCad's libraries are CC-BY-SA 4.0 with an explicit exception: the copyright holder waives the
share-alike article for designs and renders that merely *use* the models, so a figure built with
them carries no obligation back onto this curriculum. Full text in `LICENSE.txt`.
