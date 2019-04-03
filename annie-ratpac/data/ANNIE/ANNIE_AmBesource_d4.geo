////// AmBe source geometry
// The source (beryllium) is enclosed in a case (stainless steel)
// Design 4: AmBe source sits below BGO crystal with (stainless) steel plate sandwiched btwn them, all enclosed in (UVT) acrylic tube

{
name: "GEO",
index: "AmBe_acrylic_case",
enable: 1,
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "detector",
type: "tube",
r_max: 35.0,
r_min: 25.4, 
size_z: 40.0,
position: [0.0, 0.0, 0.0],
material: "acrylic_uvt_good",
color: [0.0, 1.0, 1.0, 0.1],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_BGO",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_acrylic_case",
type: "tube",
r_max: 25.0,
size_z: 25.0,
position: [0.0, 0.0, 8.0],
material: "BGO_scint",
color: [1.0, 1.0, 0.5, 0.3],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_shield",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_acrylic_case",
type: "tube",
r_max: 25.0,
size_z: 4.0,
position: [0.0, 0.0, -21.0],
material: "stainless_steel",
color: [1.0, 1.0, 1.0, 0.7],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_shield_ring",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_acrylic_case",
type: "tube",
r_max: 25.0,
r_min: 4.2,
size_z: 5.0,
position: [0.0, 0.0, -30.0],
material: "stainless_steel",
color: [1.0, 1.0, 1.0, 0.3],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_case",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_acrylic_case",
type: "tube",
r_max: 3.9,
size_z: 5.0,
position: [0.0, 0.0, -30.0],
material: "stainless_steel",
color: [1.0, 1.0, 1.0, 0.7],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_source",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_case",
type: "tube",
r_max: 2.3,
size_z: 2.0,
position: [0.0, 0.0, 0.0],
material: "beryllium",
color: [1.0, 0.0, 1.0, 0.7],
drawstyle: "solid",
}
