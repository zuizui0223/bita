// BITA relative-route-cost artificial flower — parametric CAD scaffold v1
// Engineering scaffold only. Biological low/high levels are selected by Stage 0A/0B.

$fn = 96;

part = "assembly"; // body | sleeve | shutter | reservoir | assembly
sleeve_length = 6; // mm; engineering candidate 2..10
preview_legitimate_length = 6;
preview_bypass_length = 6;

// Literature-derived external reference values (Leonard et al. 2013)
top_disc_d = 50;
top_disc_t = 1.5;
visible_tube_len = 20;
entry_d = 2.5;
lateral_entry_below_top = 5;

// Engineering scaffold values; not biological freeze parameters
tube_outer_d = 30;
internal_socket_d = 3.6;
sleeve_outer_d = 3.4;
sleeve_inner_d = 2.5;
outer_gate_len = 1.5;
reward_plane_z = 14;
reservoir_outer_d = 6.0;
reservoir_socket_d = 6.2;
reservoir_depth = top_disc_t + visible_tube_len - reward_plane_z;
reservoir_cup_d = 2.0;
reservoir_cup_depth = 1.0; // ~3.14 mm^3 = ~3.14 uL
reservoir_flange_d = 8.0;
reservoir_flange_t = 1.0;
body_bottom_z = top_disc_t + visible_tube_len;

function vsub(a,b) = [a[0]-b[0], a[1]-b[1], a[2]-b[2]];
function vadd(a,b) = [a[0]+b[0], a[1]+b[1], a[2]+b[2]];
function vmul(a,s) = [a[0]*s, a[1]*s, a[2]*s];
function vunit(a) = vmul(a, 1/norm(a));

lateral_entry = [tube_outer_d/2, 0, top_disc_t + lateral_entry_below_top];
reward_point = [0, 0, reward_plane_z];
lateral_vec = vsub(reward_point, lateral_entry);
lateral_unit = vunit(lateral_vec);
lateral_inner_start = vadd(lateral_entry, vmul(lateral_unit, outer_gate_len));

module cylinder_between(p1, p2, d) {
    v = vsub(p2, p1);
    l = norm(v);
    axis = cross([0,0,1], v);
    angle = acos(v[2] / l);
    translate(p1) {
        if (norm(axis) < 0.000001)
            cylinder(h=l, d=d);
        else
            rotate(a=angle, v=axis) cylinder(h=l, d=d);
    }
}

module hollow_tube_between(p1, p2, od, id) {
    difference() {
        cylinder_between(p1, p2, od);
        // extend the inner bore slightly to avoid coplanar faces
        u = vunit(vsub(p2,p1));
        cylinder_between(vadd(p1, vmul(u,-0.05)), vadd(p2, vmul(u,0.05)), id);
    }
}

module flower_body() {
    difference() {
        union() {
            cylinder(h=top_disc_t, d=top_disc_d);
            translate([0,0,top_disc_t])
                cylinder(h=visible_tube_len, d=tube_outer_d);
        }

        // Visible top entrance: 2.5-mm aperture only through top plate.
        translate([0,0,-0.1]) cylinder(h=top_disc_t+0.2, d=entry_d);

        // Top internal socket to fixed reward plane.
        translate([0,0,top_disc_t])
            cylinder(h=reward_plane_z-top_disc_t+0.05, d=internal_socket_d);

        // Visible lateral entrance: 2.5-mm gate through the outer shell region.
        cylinder_between(
            vadd(lateral_entry, vmul(lateral_unit,-0.1)),
            vadd(lateral_entry, vmul(lateral_unit,outer_gate_len+0.1)),
            entry_d
        );

        // Enlarged internal socket behind the externally fixed lateral entrance.
        cylinder_between(
            lateral_inner_start,
            vadd(reward_point, vmul(lateral_unit,0.05)),
            internal_socket_d
        );

        // Bottom-access reservoir cartridge socket. Cartridge top sits at reward plane.
        translate([0,0,reward_plane_z])
            cylinder(h=body_bottom_z-reward_plane_z+0.1, d=reservoir_socket_d);
    }
}

module sleeve_insert(length_mm=6) {
    assert(length_mm >= 2 && length_mm <= 10, "sleeve length must be 2..10 mm");
    difference() {
        cylinder(h=length_mm, d=sleeve_outer_d);
        translate([0,0,-0.05]) cylinder(h=length_mm+0.1, d=sleeve_inner_d);
    }
}

module shutter_plug() {
    cylinder(h=2.0, d=sleeve_outer_d);
}

module reservoir_cartridge() {
    // Local z=0 is the reward plane; cartridge extends downward into the body.
    difference() {
        union() {
            cylinder(h=reservoir_depth-0.1, d=reservoir_outer_d);
            translate([0,0,reservoir_depth-0.1])
                cylinder(h=reservoir_flange_t, d=reservoir_flange_d);
        }
        // Approximate 3-uL cup; exact delivered reward remains a pipetted trial variable.
        translate([0,0,-0.05])
            cylinder(h=reservoir_cup_depth+0.05, d=reservoir_cup_d);
    }
}

module assembly_preview(l_len=6, b_len=6) {
    color("lightblue") flower_body();

    // Legitimate sleeve, fully internal behind the visible top aperture.
    color("orange")
        translate([0,0,top_disc_t]) sleeve_insert(l_len);

    // Bypass sleeve along the diagonal socket.
    color("gold")
        hollow_tube_between(
            lateral_inner_start,
            vadd(lateral_inner_start, vmul(lateral_unit,b_len)),
            sleeve_outer_d,
            sleeve_inner_d
        );

    // Shared reward cartridge inserted from the bottom.
    color("white")
        translate([0,0,reward_plane_z]) reservoir_cartridge();
}

if (part == "body")
    flower_body();
else if (part == "sleeve")
    sleeve_insert(sleeve_length);
else if (part == "shutter")
    shutter_plug();
else if (part == "reservoir")
    reservoir_cartridge();
else
    assembly_preview(preview_legitimate_length, preview_bypass_length);
