////// AmBe source geometry
// The source (beryllium) is enclosed in a case (stainless steel) enclosed in a shield (for 60 keV X-rays)
// Design 3: AmBe source sits on top of a BGO crystal

{
name: "GEO",
index: "AmBe_BGO_bottom",
enable: 1,
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "detector",
type: "tube",
r_max: 35.0,
size_z: 12.5,
position: [0.0, 0.0, -23.0],
material: "BGO_scint",
color: [0.0, 1.0, 1.0, 0.1],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_shield",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "detector",
type: "tube",
r_max: 19.0,
size_z: 10.5,
position: [0.0, 0.0, 0.0],
material: "lead",
color: [0.0, 1.0, 1.0, 0.5],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_case",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_shield",
type: "tube",
r_max: 13.0,
size_z: 4.5,
position: [0.0, 0.0, 0.0],
material: "stainless_steel",
color: [0.0, 1.0, 1.0, 0.7],
drawstyle: "solid",
}

{
name: "GEO",
index: "AmBe_source",
valid_begin: [0, 0],
valid_end: [0, 0],
mother: "AmBe_case",
type: "tube",
r_max: 10.0,
size_z: 1.5,
position: [0.0, 0.0, 0.0],
material: "beryllium",
color: [0.0, 1.0, 1.0, 0.9],
drawstyle: "solid",
}
