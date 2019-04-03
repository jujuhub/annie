////// AmBe source geometry
// The source (beryllium) is enclosed in a case (stainless steel) enclosed in a shield (for 60 keV X-rays)
// Design 1: BGO crystal surrounds entire AmBe source

{
name: "GEO",
index: "AmBe_BGO",
enable: 1,
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "detector",
type: "tube",
r_max: 35.0,
size_z: 40.0,
position: [0.0, 0.0, 0.0],
material: "BGO_scint",
color: [0.0, 1.0, 1.0, 0.1],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_shield",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_BGO",
type: "tube",
r_max: 6.0,
size_z: 7.0,
position: [0.0, 0.0, 0.0],
material: "stainless_steel",
color: [1.0, 1.0, 1.0, 0.7],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_case",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_shield",
type: "tube",
r_max: 3.9,
size_z: 5.0,
position: [0.0, 0.0, 0.0],
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
color: [1.0, 0.0, 0.0, 0.7],
drawstyle: "solid",
}
