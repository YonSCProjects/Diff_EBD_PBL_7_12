---
name: chassis-frame-research-2026-08-20
description: "P4/5/7 chassis + battery research results (complete, decision pending with Yon) and the confirmed Felchao 100mm frame findings (P8 doc adjustment DONE 2026-08-20)"
metadata:
  type: reference
---

Hardware research for the P5-P8 build-out, 2026-08-20. All four research agents complete.

## Battery (COMPLETE - answered Yon's "use 2?": YES)
2x 3.7V li-ion **in series** (7.4V nominal): L298N drops ~1.4-1.8V at TT-motor currents
-> motors see 5.6-6.0V. **Cap PWM at ~200/255** in all car sketches (fresh 8.4V pack).
L298N 5V jumper powers the Uno safely (disconnect battery when USB plugged). Format:
**2x18650 spring-contact holder with switch + protected button-top cells** (~69mm -
test-fit before buying the class set); teacher charges in a 2-bay charger. **P7:**
ESP32-CAM gets its own MP1584/LM2596 buck (5.0-5.2V) + 470-1000uF cap at the CAM -
never the L298N regulator (brown-out trap); common ground.

## Chassis options (COMPLETE - awaiting Yon's decision)
Buy (all fit owned TT motors + 65mm wheels): **4WD two-layer acrylic kit ~20-36 ILS
(recommended)** - 4 spare motors/wheels, no fragile tabs, two decks, camera-ready;
classic 2WD acrylic ~12-28 ILS (brittle tabs); Magician-style two-deck $8-15 (hard to
source); aluminum 2WD ~22 ILS chassis-only (unbreakable; verify TT holes; insulate under
boards). DIY: **kanplast folded tray ~5-8 ILS (best DIY)** - zero glue, zip ties, PP
springs back (hot glue does NOT bond PP); kapa double-deck (easiest cut, weakest);
pre-cut MDF/plywood flat-pack (teacher batch-cuts, low-frustration tier); upcycled
lunchbox (ownership hook, Tier-3 personalization only). No chassis matches 2x18650
holder holes - cards use zip ties/foam tape. Recommendation given: 4WD kit standard +
kanplast optional DIY card + lunchbox personalization. **After Yon decides -> adjust
P4/P5/P7 plans**: master doc SS6.8-6.11 hardware lists, budget rows ~1320-1323, shopping
rows ~1383 (replace 4xAA/rechargeable-AA scheme with 2x18650), HE overview rows 148-151
+ 335-338, P4's existing task cards (T1_M3 assemble-chassis, battery mentions).

## P8 Felchao frame (CONFIRMED + doc adjustment DONE 2026-08-20)
**Frame:** FEICHAO/JMT hollow-cup carbon frame kit, 100mm wheelbase (AliExpress
32950607425, ~$4.40-6.60 at mirrors; JMT SKU F26165). **100mm variant = the 8520
version** - press-fit: rubber grommets in arm rings, 8.5mm motors push through, no
screws/glue. Kit (9g measured): 2 carbon plates 1.5mm, 4 grommets, 4 rubber motor caps
(= crash bumpers/landing feet), standoffs + M2-class screws (#00 Phillips), 2 battery
O-rings. NOT included: motors, props, **prop guards**, electronics.
**Props:** vendor says 50-65mm (prefer 50-60); 65mm = max (5.7mm tip clearance).
**1.0mm bore required** (Gemfan 1.5mm-bore whoop props do NOT fit) - buy "8520 CW/CCW +
65mm prop" sets; brushed motors last 5-10 flight hours, order spares.
**Weight/thrust reality:** realistic AUW 70-73g -> in-system T/W ~1.7-2.0 (bench up to
2.5-3.0); keep AUW <= 75g; battery 450-600mAh with genuine >=25-35C beats low-C 600mAh.
**TB6612 is the weak link:** 1.2A cont/channel vs 8520 ~1.8-2.5A near full throttle ->
thermal limiting + ~1V drop at 2A; mitigations: PWM cap, airflow, hover-focused goals;
4x SI2302 MOSFET board is the standard brushed-quad alternative if redesign wanted.
**Guard policy decision pending with Yon** (before P8 safety cards): clip-on Q100-class
guard set (+4-6g) vs 55mm props during learning. MT3608 never feeds motors (2A limit).
**Doc adjustment applied 2026-08-20:** master doc lines ~927/1125/1129/1136/1324/1381 +
HE overview rows 339/396 swapped popsicle->Felchao (incl. Tier 1 change: teacher
pre-screws plates, STUDENT press-fits motors tool-free); builds regenerated.

## 4WD kit — dimensions + deals (researched 2026-08-20, Yon leaning to this option)
**Dimensions:** plates ~255-260 x 147-150mm (x2, identical), thickness varies by seller
(2/3/4-5mm — prefer 3mm+); assembled ~260 x 155 x 67-69mm but REAL over-wheel width
~180-200mm (allow 20cm track width); deck spacing = 30mm standoffs (canonical; 25/40mm
variants exist); wheels 65x27mm; bare chassis+motors ~450g; full car with 2x18650 +
Uno + L298N + breadboard ≈ 1.05-1.15kg (within 2.5kg/wheel rating). **Wheelbase NOT
published anywhere** — est. ~150-160mm; measure the physical kit before any card
depends on it. Usable deck: central ~110-120mm strip full-length; L298N goes TOPSIDE
(too tall for under-deck); 18650 holder in bottom-deck center between motors (zip
ties/foam tape). Seller traps: single-deck kits mislabeled 4WD (must see 2 plates + 6
standoffs in photos); hole patterns vary batch-to-batch — never pre-print hole coords
in cards. Seeed datasheet = canonical parts list (16x M3x25 etc.).
**Deals (Aug 2026):** AliExpress IL gateway: ₪27.45 (500+ sold, 4.8★, item
1005007362602598 — best), ₪23.30 (451 sold 4.9★), ₪32.43 (5-color decks — one color
per student idea). Israeli storefront: Sucaria ₪40.55 (double-deck spec confirmed in
text, ILS billing). Robokit.co.il full electronics kit ₪295 (backorder). Ignore fake
-80% anchors. **VAT: $75 exemption restored 2026-06-02** — 9 units at $8-11 straddles
it → SPLIT into two orders (5+4, a day apart), one seller for identical batch; ask
seller for multi-unit coupon; buy 9 for 4-8 students (motor gearboxes + acrylic tabs
are the breakage points).
