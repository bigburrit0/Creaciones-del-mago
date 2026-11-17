// =====================================================================
//  BIC slide-out holster with lever lock  ("Creaciones del Mago")
//  Original design inspired by the "GRABICY for BIC" reel (nokt.xyz):
//  a lighter carriage slides inside a body, driven by a thumb knob;
//  a side lever pivoting at the bottom locks the knob in either the
//  RETRACTED (stowed) or EXTENDED (ready) position.
//  Material: PLA.  Hardware: 1x M3x12 screw + 1x M3 DIN 9021 washer.
//
//  Render one part:
//    openscad -D 'part="body"' -o body.stl bic-slide-holster.scad
// =====================================================================

/* [Output] */
// body | carriage | lever | coupon_body | coupon_carriage | coupon_pivot |
// closed_retracted | open_retracted | open_extended | closed_extended |
// exploded | print_layout
part = "closed_extended";
show_lighter = true;

/* [Lighter - MEASURE YOURS WITH CALIPERS] */
// maxi (J26, EU/LatAm) | j6 (US Maxi) | slim (J23) | mini (J25)
lighter = "maxi";

/* [Fits (per side, mm)] */
fit      = 0.25;  // lighter inside carriage (crush ribs take up the rest)
rib_h    = 0.45;  // crush-rib protrusion
sg       = 0.30;  // carriage sliding in body
slot_c   = 0.30;  // knob stem in slot
g        = 0.25;  // lever above body face
hub_c    = 0.25;  // lever hub hole around boss (radial)

/* [Design] */
cw        = 1.6;   // carriage wall
cf        = 2.0;   // carriage floor
bw        = 2.4;   // body wall (6 perimeters @0.4)
floor_h   = 13;    // solid body foot (holds pivot screw + lanyard hole)
recess    = 5;     // lighter top sits this far below the rim when stowed
hood_clear= 19;    // PLA rim -> bottom of metal hood when extended (>=15!)
lt        = 3.2;   // lever thickness
theta     = 14;    // lever opening angle (deg)
pad_w     = 7;     // thumb pad width
pad_h     = 10;    // thumb pad height
stem_w    = 4;     // knob stem width (through the slot)
ridge_p   = 0.75;  // detent ridge protrusion from face
groove_w  = 2.6;   // detent groove width in lever
groove_d  = 0.9;   // detent groove depth
boss_d    = 6;     // pivot boss OD
pilot_d   = 2.5;   // M3 self-tapping pilot (use 4.0 for a heat-set insert)
ring_r    = 6.0;   // lever hub outer radius
pivot_z   = 6.5;
texture   = true;  // hex dimples on the lever

$fn = 48;

// ---------------- lighter presets [length, width, thickness, corner r, hood h]
LP = lighter=="j6"   ? [81,25,14.5,6.0,14] :
     lighter=="slim" ? [76,22,11.0,4.5,13] :
     lighter=="mini" ? [62,22,11.0,4.5,12] :
                       [82,25,15.0,6.0,14];
LL=LP[0]; LW=LP[1]; LT=LP[2]; LR=LP[3]; hood_h=LP[4];

// ---------------- derived
travel = recess + hood_h + hood_clear;   // carriage stroke
Wi=LW+2*fit; Ti=LT+2*fit; Ri=LR+fit;     // carriage inside
Wc=Wi+2*cw;  Tc=Ti+2*cw;  Rc=Ri+cw;      // carriage outside
Wk=Wc+2*sg;  Tk=Tc+2*sg;  Rk=Rc+sg;      // body cavity
W =Wk+2*bw;  T =Tk+2*bw;  Ro=2.5;        // body outside (flat faces)
ch = round(LL*0.48);                     // carriage height
H  = floor_h + cf + LL + recess;         // body height

xs   = Wc/2 - Rc;                        // knob / slot / pivot x
pv   = [xs, pivot_z];                    // pivot (x,z)
k_lo = floor_h + pad_h/2;                // knob centre, stowed
k_hi = k_lo + travel;                    // knob centre, extended
y1   = -T/2 - g;                         // lever underside plane
x_e  = xs - pad_w/2 - 0.3;               // lever edge beside the pad path
tip  = xs - 1.0;                         // tooth tip (2.5 mm over the pad)
x_stop = xs + pad_w/2 + 0.6;             // closing stop block
xL   = -W/2 + 0.8;                       // lever left edge
P    = [-W/2 + 5, 46];                   // detent ridge position (x,z)

echo(str("Body ", W, " x ", T, " x ", H, " mm; stroke ", travel,
         " mm; carriage ", Wc, " x ", Tc, " x ", ch));
echo(str("Rim-to-hood clearance when extended: ", travel - recess - hood_h, " mm"));

// ===================================================================== helpers
module rr(w,t,r){ r2=min(r,w/2-0.01,t/2-0.01); offset(r=r2) square([w-2*r2,t-2*r2],center=true); }
module rbox(w,t,r,h,cb=0,ct=0){
  hull(){
    if(cb>0) linear_extrude(0.01) rr(w-2*cb,t-2*cb,max(r-cb,0.1));
    translate([0,0,cb]) linear_extrude(h-cb-ct) rr(w,t,r);
    if(ct>0) translate([0,0,h-0.01]) linear_extrude(0.01) rr(w-2*ct,t-2*ct,max(r-ct,0.1));
  }
}
// extrude a 2D profile drawn in (y,z) along +x
module yz_extrude(x0,len) translate([x0,0,0]) rotate([90,0,90]) linear_extrude(len) children();

// ===================================================================== BODY
module body(){
  difference(){
    union(){
      rbox(W,T,Ro,H,cb=0.6,ct=0.8);
      // pivot boss
      translate([xs,-T/2+0.01,pivot_z]) rotate([90,0,0]) cylinder(d=boss_d,h=g+lt+0.15+0.01);
      // detent ridge (vertical, rounded ends)
      hull() for(z=[P.y-3,P.y+3]) translate([P.x,-T/2+1.4-ridge_p,z]) sphere(r=1.4,$fn=24);
      // closing stop block (45° underside, no support)
      sp = g+lt-0.4;
      yz_extrude(x_stop, W/2-0.6-x_stop)
        polygon([[-T/2+0.5,H-26-sp],[-T/2+0.5,H-0.8],[-T/2-sp,H-0.8],[-T/2-sp,H-26]]);
    }
    // cavity + entry chamfer
    translate([0,0,floor_h]) linear_extrude(H) rr(Wk,Tk,Rk);
    translate([0,0,H-1.2]) hull(){
      linear_extrude(0.01) rr(Wk,Tk,Rk);
      translate([0,0,1.21]) linear_extrude(0.01) rr(Wk+2.4,Tk+2.4,Rk+1.2);
    }
    // knob slot (open at the top so the carriage can be pulled out)
    translate([xs-stem_w/2-slot_c,-T/2-5,floor_h-0.4]) cube([stem_w+2*slot_c,5+bw+1,H]);
    // slot mouth chamfer at the top
    translate([xs,-T/2,H]) rotate([90,0,0]) linear_extrude(10,center=true)
      polygon([[-stem_w/2-slot_c-1,0.01],[stem_w/2+slot_c+1,0.01],[stem_w/2+slot_c,-1],[-stem_w/2-slot_c,-1]]);
    // M3 pilot through boss into the foot
    translate([xs,-T/2+10,pivot_z]) rotate([90,0,0]) cylinder(d=pilot_d,h=10+g+lt+1,$fn=24);
    // lanyard hole (teardrop, along X, near the back)
    translate([-W/2-1,T/2-4.2,6.5]) hull(){
      rotate([0,90,0]) cylinder(r=1.8,h=W+2,$fn=32);
      translate([0,-0.01,1.8*1.414]) cube([W+2,0.02,0.02]);
    }
  }
}

// ===================================================================== CARRIAGE
module carriage(){
  difference(){
    union(){
      rbox(Wc,Tc,Rc,ch,cb=0.4);
      // stem through the slot (starts at the bed: no overhang)
      translate([xs-stem_w/2,y1-0.01,0]) cube([stem_w,(-Tc/2+0.9)-y1+0.01,pad_h]);
      // thumb pad (in the lever plane)
      hull(){
        translate([xs-pad_w/2+0.4,y1-lt+0.4,0]) cube([pad_w-0.8,lt-0.4,0.01]);
        translate([xs-pad_w/2,y1-lt,0.4]) cube([pad_w,lt,pad_h-0.4]);
      }
      // grip ribs (triangular, 45° flanks)
      for(z=[2.5,5,7.5]) yz_extrude(xs-pad_w/2+0.5,pad_w-1)
        polygon([[y1-lt+0.01,z-1.1],[y1-lt-1.1,z],[y1-lt+0.01,z+1.1]]);
    }
    translate([0,0,cf]) linear_extrude(ch) rr(Wi,Ti,Ri);
    // inner top chamfer
    translate([0,0,ch-0.8]) hull(){ linear_extrude(0.01) rr(Wi,Ti,Ri);
      translate([0,0,0.81]) linear_extrude(0.01) rr(Wi+1.6,Ti+1.6,Ri+0.8); }
    // push-out hole
    translate([0,0,-1]) cylinder(d=min(10,Ti-3),h=cf+2);
  }
  // crush ribs
  rr_ = 0.7;
  ribs = [[ Wi/5, Ti/2], [-Wi/5, Ti/2], [ Wi/5,-Ti/2], [-Wi/5,-Ti/2], [Wi/2,0], [-Wi/2,0]];
  for(p=ribs){
    d = p.y==0 ? [sign(p.x),0] : [0,sign(p.y)];
    translate([p.x+d.x*(rr_-rib_h), p.y+d.y*(rr_-rib_h), cf-0.01])
      hull(){ cylinder(r=rr_,h=ch-cf-4,$fn=16); translate([0,0,ch-cf-2]) cylinder(r=0.05,h=0.01); }
  }
}

// ===================================================================== LEVER
module lever_core2d(){
  polygon([[xL,36],[xL,H-2],[x_e,H-2],[x_e,pv.y],[pv.x-ring_r+0.5,pv.y-2]]);
}
module lever2d(){
  difference(){
    offset(r=0.8) offset(delta=-0.8) union(){
      lever_core2d();
      translate(pv) circle(ring_r);
      // stowed notch: lower tooth (merges into hub) + upper tooth
      translate([x_e-1,pv.y]) square([tip-x_e+1, k_lo-pad_h/2-0.3-pv.y]);
      translate([x_e-1,k_lo+pad_h/2+0.3]) square([tip-x_e+1,4.5]);
      // extended notch: lower tooth (takes the load while lighting)
      translate([x_e-1,k_hi-pad_h/2-0.3-5]) square([tip-x_e+1,5]);
      // head = upper tooth of extended notch, reaches the stop block
      translate([x_e-1,k_hi+pad_h/2+0.3]) square([x_stop-0.3-(x_e-1), H-2-(k_hi+pad_h/2+0.3)]);
      // thumb tab overhanging the left edge
      translate([xL-2.2,H-18]) square([4,16]);
    }
    translate(pv) circle(r=boss_d/2+hub_c);
  }
}
module hexgrid2d(){
  s=4.2; for(i=[-12:12], j=[-30:30]) translate([i*s*0.866*1.0, j*s + (i%2)*s/2]) circle(r=1.45,$fn=6);
}
module lever(){ // local frame: z=0 is the underside (on the bed), z=lt outer face
  difference(){
    linear_extrude(lt) lever2d();
    if(texture) translate([0,0,lt-0.5]) linear_extrude(1)
      intersection(){ offset(delta=-2.4) lever_core2d(); hexgrid2d(); }
    // detent grooves: closed + open
    for(a=[0,theta]) translate([pv.x,pv.y,0]) rotate([0,0,-a]) translate([-pv.x,-pv.y,0])
      translate([P.x-groove_w/2,P.y-5,-0.1]) cube([groove_w,10,groove_d+0.1]);
  }
}
// place lever on the body, a = opening angle
module lever_placed(a=0){
  translate([pv.x,0,pv.y]) rotate([0,-a,0]) translate([-pv.x,0,-pv.y])
    translate([0,y1,0]) rotate([90,0,0]) lever();
}

// ===================================================================== LIGHTER (dummy, for views)
module lighter_dummy(){
  color([0.08,0.08,0.09]) linear_extrude(LL-hood_h) rr(LW,LT,LR);
  color([0.75,0.75,0.78]) translate([0,0,LL-hood_h]) difference(){
    linear_extrude(hood_h-3) rr(LW-2,LT-1,LR-1);
    translate([0,0,2]) linear_extrude(hood_h) rr(LW-4,LT-3,LR-2);
  }
  color([0.4,0.4,0.42]) translate([-LW/2+7,0,LL-4]) rotate([90,0,0]) cylinder(r=4,h=6,center=true);
  color([0.85,0.1,0.05]) translate([LW/2-10,-4,LL-hood_h-2]) cube([8,8,4]);
}

// ===================================================================== ASSEMBLY
C_BODY=[0.13,0.13,0.15]; C_CAR=[0.25,0.25,0.28]; C_LEV=[0.78,0.92,0.35];
module screw_hw(){
  color([0.6,0.6,0.62]) translate([xs,y1-lt-0.15,pivot_z]) rotate([90,0,0]){
    cylinder(d=9,h=0.8); translate([0,0,0.8]) cylinder(d=5.7,h=1.65); }
}
module assembly(ext=0, a=0){
  zc = floor_h + ext*travel;
  color(C_BODY) body();
  color(C_CAR) translate([0,0,zc]) carriage();
  if(show_lighter) translate([0,0,zc+cf]) lighter_dummy();
  color(C_LEV) lever_placed(a);
  screw_hw();
}
module exploded(){
  color(C_BODY) body();
  color(C_CAR) translate([0,0,H+25]) carriage();
  if(show_lighter) translate([0,0,H+25+ch+30]) lighter_dummy();
  color(C_LEV) translate([0,-25,0]) lever_placed(0);
  translate([0,-40,0]) screw_hw();
}

// ===================================================================== COUPONS
// short body slice (same slot + cavity) to test the carriage slide
module coupon_body(){
  hc=22;
  difference(){
    rbox(W,T,Ro,hc,cb=0.6);
    translate([0,0,2]) linear_extrude(hc) rr(Wk,Tk,Rk);
    translate([xs-stem_w/2-slot_c,-T/2-5,1.6]) cube([stem_w+2*slot_c,5+bw+1,hc]);
  }
}
// bottom 14 mm of the carriage: tests lighter grip AND slide in coupon_body
module coupon_carriage(){ intersection(){ carriage(); translate([-50,-50,0]) cube([100,100,14]); } }
// pivot: boss + pilot on a small block, plus a lever hub stub
module coupon_pivot(){
  difference(){
    union(){
      translate([-8,0,0]) cube([16,12,14]);
      translate([0,0.01,7]) rotate([90,0,0]) cylinder(d=boss_d,h=g+lt+0.15+0.01);
    }
    translate([0,10,7]) rotate([90,0,0]) cylinder(d=pilot_d,h=20,$fn=24);
  }
  translate([20,0,0]) difference(){
    hull(){ cylinder(r=ring_r,h=lt); translate([0,18,0]) cylinder(r=3,h=lt); }
    translate([0,0,-1]) cylinder(r=boss_d/2+hub_c,h=lt+2);
  }
}

// ===================================================================== PRINT ORIENTATIONS
module body_print(){ body(); }
module carriage_print(){ carriage(); }
module lever_print(){ translate([-pv.x,-pv.y,0]) lever(); }

// ===================================================================== DISPATCH
if      (part=="body")             body_print();
else if (part=="carriage")         carriage_print();
else if (part=="lever")            lever_print();
else if (part=="coupon_body")      coupon_body();
else if (part=="coupon_carriage")  coupon_carriage();
else if (part=="coupon_pivot")     coupon_pivot();
else if (part=="closed_retracted") assembly(0,0);
else if (part=="open_retracted")   assembly(0,theta);
else if (part=="open_extended")    assembly(1,theta);
else if (part=="closed_extended")  assembly(1,0);
else if (part=="exploded")         exploded();
else if (part=="print_layout"){
  body_print();
  translate([W+10,0,0]) carriage_print();
  translate([-W-30,-20,0]) lever_print();
}

// ---- analysis helpers (used by the collision check script)
probe_ext = 0;   // carriage position 0..1
probe_ang = 0;   // lever angle
if (part=="probe_carriage") translate([0,0,floor_h+probe_ext*travel]) carriage();
if (part=="probe_lever")    lever_placed(probe_ang);
if (part=="probe_lighter")  translate([0,0,floor_h+probe_ext*travel+cf]) linear_extrude(LL) rr(LW,LT,LR);
