#!python
import sys
import re
import os
import time

# NOTE: Only works with ***OrcaSlicer***

source_file=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(source_file, "r") as f:
    lines = f.readlines() #count lines

# Process file to .gcode file for post-process script 
if (source_file.endswith('.gcode')):
    dest_file = re.sub('\.gcode$','',source_file)
    try:
        os.rename(source_file, dest_file+".scv.bak")
    except FileExistsError:
        os.remove(dest_file+".scv.bak")
        os.rename(source_file, dest_file+".scv.bak")
    dest_file = re.sub('\.gcode$','',source_file)
    dest_file = dest_file + '.gcode'
else:
    dest_file = source_file
    os.remove(source_file)

# Boolean variables
in_inner_wall = False
in_outer_wall = False
in_overhang_wall = False
in_sparse_infill = False
in_internal_solid_infill = False
in_ironing = False
in_bridge = False
in_internal_bridge = False
in_support = False
in_prime_tower = False

# Open the destination file and write
with open(dest_file, "w") as of:
    of.write('; Ensure SCV macros are properly setup in Klipper\n')
    of.write('_USE_NORMAL_SCV\n')
    of.write('_USE_INNER_WALL_SCV\n')
    of.write('_USE_OUTER_WALL_SCV\n')
    of.write('_USE_OVERHANG_WALL_SCV\n')
    of.write('_USE_SPARSE_INFILL_SCV\n')
    of.write('_USE_INTERNAL_SOLID_INFILL_SCV\n')
    of.write('_USE_IRONING_SCV\n')
    of.write('_USE_BRIDGE_SCV\n')
    of.write('_USE_INTERNAL_BRIDGE_SCV\n')
    of.write('_USE_SUPPORT_SCV\n')
    of.write('_USE_PRIME_TOWER_SCV\n')
    for line_Index in range(len(lines)):
        oline = lines[line_Index]
        # print(oline)
        # Parse gcode line
        if oline.startswith(';TYPE:Inner wall'):
            in_inner_wall = True
            of.write(oline)
            of.write('_USE_INNER_WALL_SCV\n')
        elif (oline.startswith(';TYPE:Outer wall') or oline.startswith(';TYPE:Top surface') or oline.startswith(';TYPE:Bottom surface')):
            in_outer_wall = True
            of.write(oline)
            of.write('_USE_OUTER_WALL_SCV\n')
        elif oline.startswith(';TYPE:Overhang wall'):
            in_overhang_wall = True
            of.write(oline)
            of.write('_USE_OVERHANG_WALL_SCV\n')
        elif oline.startswith(';TYPE:Sparse infill'):
            in_sparse_infill = True
            of.write(oline)
            of.write('_USE_SPARSE_INFILL_SCV\n')
        elif (oline.startswith(';TYPE:Internal solid infill') or oline.startswith(';TYPE:Gap infill')):
            in_internal_solid_infill = True
            of.write(oline)
            of.write('_USE_INTERNAL_SOLID_INFILL_SCV\n')
        elif oline.startswith(';TYPE:Ironing'):
            in_ironing = True
            of.write(oline)
            of.write('_USE_IRONING_SCV\n')
        elif oline.startswith(';TYPE:Bridge'):
            in_bridge = True
            of.write(oline)
            of.write('_USE_BRIDGE_SCV\n')
        elif oline.startswith(';TYPE:Internal Bridge'):
            in_internal_bridge = True
            of.write(oline)
            of.write('_USE_INTERNAL_BRIDGE_SCV\n')
        elif (oline.startswith(';TYPE:Support') or oline.startswith(';TYPE:Support transition')):
            in_support = True
            of.write(oline)
            of.write('_USE_SUPPORT_SCV\n')
        elif oline.startswith(';TYPE:Prime tower'):
            in_prime_tower = True
            of.write(oline)
            of.write('_USE_PRIME_TOWER_SCV\n')
        elif (oline.startswith('; INIT') or oline.startswith(';TYPE:Undefined') or oline.startswith(';TYPE:Skirt') or oline.startswith(';TYPE:Brim') or oline.startswith(';TYPE:Support interface') or oline.startswith(';TYPE:Custom') or oline.startswith(';TYPE:Multiple')):
            in_inner_wall = False
            in_outer_wall = False
            in_overhang_wall = False
            in_sparse_infill = False
            in_internal_solid_infill = False
            in_ironing = False
            in_bridge = False
            in_internal_bridge = False
            in_support = False
            in_prime_tower = False
            of.write(oline)
            of.write('_USE_NORMAL_SCV\n')
        else:
            of.write(oline)

of.close()
f.close()
