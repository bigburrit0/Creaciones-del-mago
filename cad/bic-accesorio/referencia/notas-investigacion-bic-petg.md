# Research notes (from Haiku teams; snippet-level, mostly unverified)

## Team A — Carabiner
- Shape: D / asymmetric D best for plastic (load to thick spine). Oval weakest. Keylock (smooth, notch-free) nose snags less.
- Mini carabiner size: 40-70 mm long; BD Micron 63x42.5 mm, 15 mm gate. Gate openings of minis: 12-22 mm. Target gate 13-18 mm.
- Popular printed designs: Print-in-Place Spring-Gate (Printables 1754910, PETG; thick spine + thin tapered leaf flank + Z-step lap latch), Compliant carabiner (0.3 mm hinge gap), Utility Carabiner v2 (hook latch + twist lock, 6+ walls on gate), Flexi Carabiner (MakerWorld, 6x4 cm, 0.2/0.3 mm gap; tight gap sticks), Suicide Carabiner (PETG ~165 kg maker test).
- Failure modes: thin spring root + thin latch base crack first -> taper + root fillet. Hinges fuse if gap tight (PETG wants ~0.3-0.45 mm). Gate overhang sags.
- Strength: printed PETG hooks 10-165 kg. Lighter ~0.2 kgf, 10x drop ~2 kgf -> huge margin. PETG yields/stretches rather than snapping.
- Flexure: strain eps = 1.5*t*d/L^2. PETG allowable: 1.5-2% conservative, ~1% for thousands of cycles. Halve if bending across layers. Print flat so bending is in-plane (along roads).
  - Example t1.2 L25 d5 -> 1.44% (marginal). t1.0 L20 d3 -> 1.1%.
  - PETG living-hinge (thin 0.4 mm folding) only ~857 cycles -> avoid thin living hinges; use thicker, longer leaf springs in bending.
- Creep: PETG Tg ~78C; keep sustained load < 60C. Gate should rest unstressed (no preload) when closed. Car at 70C = risk.
- Gate stop: gate must seat in nose notch/slot so it can't swing outward; lap/Z-step latch; gate tongue outboard of nose.
- Pivot (if separate gate): M3 screw + nut preferred over printed pin. Print-in-place gap 0.3 mm/side.
- Gate fully solid (100% infill / 4-6 walls).

## Team B — Magnets
- Pull vs steel (vendor, ideal): 6x3 N52 ~1.1-1.3 kg; 8x3 N35 ~1.0-1.4; 10x3 N35 ~1.5, N52 ~2.1-2.3; 12x3 N35 ~3.5.
- 1 mm plastic gap loses ~30-70%. Keep cover skin 0.4-0.6 mm (2-3 layers) if embedded.
- Load: lighter+sleeve ~40 g; with 3:1 SF -> need ~0.3 kg derated pull. 8x3 / 10x3 comfortable.
- SHEAR is only ~15-25% of pull (magnet-magnet ~50%). => mechanical feature (boss-in-socket, lip, dovetail, hook) must take all shear; magnet only resists axial separation.
- Magnet-to-magnet: self-centers. Magnet-to-steel: may stick off-axis, needs steel >=1-1.9 mm thick; cheaper, avoids magnet-magnet slam/chipping.
- Two magnets opposite polarity side by side => keyed orientation, self-aligning.
- Polarity: mark faces, test before gluing; compass test.
- Retention: embed via print pause (>=2 cover layers; watch steel nozzle attraction) OR press-fit (+0.1-0.15 mm dia, +0.1-0.2 depth) + epoxy (scuff nickel). CA weak. Friction alone loosens (creep). Lip/ledge blocks pull-out. >=3 wall loops around pockets, 2-3 mm wall.
- Coatings: NiCuNi chips; epoxy-coated better for sweat. Sealed pocket protects.
- Heat: N52 max ~60-80 C (permanent loss above). BIC hood hits 60 C in ~15 s sideways, >50 s upright. PETG HDT 62-76 C. Car dash ~69 C avg. => keep PETG/magnets >=10-15 mm from hood; magnets at bottom end. PETG is UL94 HB (PETG-V0 exists).
- Safety: pacemaker 15 cm; swallowing hazard -> fully enclose magnets.
- Commercial: pure-magnet keychains = accidental release complaints (lost keys). Winners: Fidlock (magnet guides + mechanical snap, slide release), KeySmart MagConnect Pro (dovetail slide + magnets), Nite Ize 360 (magnet + twist). => magnet + mechanical retention, deliberate release direction.
- Bayonet+magnet: retention good but bulky/slow; overhangs in slots.
- Dovetail + magnet: PETG slide 0.2 mm/side start (coupon 0.1-0.3); 45° flanks print w/o supports; gravity-seated dovetail resists pull-out; magnet stops it sliding up on jolts; add end stop not magnet.

## Team C — BIC lighter fit
- Official: J26 Maxi 82 x 25 x 15 mm, 24.7 g (BIC Graphic). J23 Slim 76 x 22 x 11. J25 Mini 62 x 22 x 11, 13 g. J6 (US Maxi) no official sheet; trade listings ~81 x 25 x 14 mm. => use 25.2 x 14.6 body, measure with calipers.
- Djeep D1 63x36x14 (flat). Clipper cylindrical ~16 dia. Cricket ~80x23x10. => common magnetic interface module + per-lighter sleeve.
- Market UY/AR: BIC major; Mercado Libre top sellers Shark, Zengaz, Candela.
- Sleeve designs: friction open-top, snug ~0.2 mm/side, bottom push-out hole (chopstick), retention ridges/compliant tabs near base, 3+ walls. Stickers/wraps change fit (~0.5 mm batch variation) -> compliant ribs absorb it. Complaints: too tight (pliers), too loose.
- Fuel window useless on opaque J6. Grip/thumb recess more useful.
- Safety: never cover/press fork or child guard (pocket ignition per patents). Sleeve top well below hood with air gap. Hood reaches 60 C in 15 s sideways. BIC storage max 50 C. No lit use inside sleeve recommended... keep top open.
- Commercial: Exotac fireSLEEVE (TPE, 2 lashing points), LighterBro (steel, stop), leashes attach at bottom. Lashing/key point expected.
- EDC: wants low profile, protection, secure quick release, quiet; complaints bulk, fit, magnet glue failure, scuffing, slipping off belt loop.
- Attachment at bottom end keeps wheel free; lighter hangs flame-end-down? (hanging from bottom = flame end down; fine, gravity).

## Team D — PETG printability
- Overhang <=45 deg (PETG worse than PLA); bridges <=10-12 mm; walls multiples of 0.4, >=1.2 mm load-bearing; flexure >=1.2 mm.
- Elephant foot: PETG most prone -> 0.3-0.5 mm first-layer inset/chamfer on mating edges & slot mouths.
- Fits per side: press 0.05-0.15, snug 0.10-0.15, sliding 0.15-0.30, loose 0.25-0.45. Holes print undersized ~0.1-0.2 dia. Print a coupon.
- Z strength ~60-90% of XY for PETG. Print carabiner flat: loop & flexure bend along the extrusion lines.
- Thin parts: perimeters >> infill; 1-1.5 mm flexure = all walls; 0.2 mm layers; 0.42-0.45 line width. Brick layers +10%.
- Fatigue data scarce; one folding test: PETG ~857 cycles for thin living hinge -> don't use thin hinges, use long leaf springs; test coupons.
- Settings: 240-250 C nozzle, 70 C bed, textured PEI + glue stick release, fan 20-40%, slower outer walls; dry 65 C 6-8 h.
- Pause for magnets: Bambu Studio layer slider "add pause" at capping layer; >=2-3 cover layers; PETG oozes on pause -> small gap; CA drop to seat. 
- Materials: unfilled PETG better than PETG-CF for flexure. PETG HF lower Z impact. PCTG much tougher (bends instead of snapping) -> best upgrade for gate. Annealing: not worth it (dimensional change).
