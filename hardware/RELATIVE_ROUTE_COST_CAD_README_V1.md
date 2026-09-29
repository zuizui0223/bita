# Relative-route-cost CAD scaffold v1

## Purpose

This directory contains a parametric OpenSCAD scaffold for the preregistered BITA artificial-flower experiment. It is an engineering starting point, not a frozen biological manipulation.

## Files

- relative_route_cost_flower_v1.scad — parametric body, sleeve, shutter and reward-cartridge geometry.
- RELATIVE_ROUTE_COST_CAD_BOM_V1.csv — minimum prototype parts list.

## Geometry

The CAD keeps the literature-derived visible reference geometry:

~~~text
top disc = 50 mm diameter
visible tube = 20 mm
top entrance = 2.5 mm
lateral entrance = 2.5 mm
lateral entrance centre = 5 mm below the top
~~~

The internal CAD body is intentionally wider than the historical pipette-tip flower because it must accommodate two independently variable internal sleeves plus one shared bottom-loaded reward cartridge.

Engineering-only defaults:

~~~text
tube outer diameter = 30 mm
internal socket diameter = 3.6 mm
sleeve OD / ID = 3.4 / 2.5 mm
candidate sleeve lengths = 2..10 mm
reward plane = 14 mm below top
reservoir cup = about 3 uL
~~~

These internal values can change before the Stage -1 hardware freeze. Any change creates a new geometry version and requires bench QC again.

## Why sleeve length rather than reward distance?

The shared reward plane is fixed. Low/high manipulations change only the length of a narrow guided tunnel immediately behind an externally identical entrance. Stage 0 measures whether that guided length actually changes handling cost in the permitted bumblebee system.

This avoids moving the reward or changing entrance visibility across conditions.

## Rendering

Set the OpenSCAD variable part to one of:

~~~text
body
sleeve
shutter
reservoir
assembly
~~~

For sleeve, set sleeve_length to an integer from 2 through 10 mm.

Do not export final STL files as frozen experiment parts until:

1. the CAD measurements are copied into the module manifest;
2. the physical prints are measured;
3. Stage -1 bench QC passes.

## Prototype sequence

1. Print at least four identical bodies.
2. Print two labelled sleeve sets: L002–L010 and B002–B010.
3. Print spare shutters and reservoir cartridges.
4. Measure every body and insert with the module manifest.
5. Run 20-load wetting/leakage QC on every assembly planned for Stage 0A.
6. Only then expose calibration bees.

## Important claim boundary

The CAD does not establish that 10 mm is harder than 2 mm biologically. Only the Stage-0 handling-time calibration defines biological route cost.
