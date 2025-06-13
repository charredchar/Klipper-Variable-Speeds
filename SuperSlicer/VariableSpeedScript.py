#!python
import sys
import re
import os
import time

# NOTE: Only works with ***SuperSlicer***

source_file=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(source_file, "r") as f:
    lines = f.readlines() #count lines

# Process file to .gcode file for post-process script 
if (source_file.endswith('.gcode')):
    dest_file = re.sub(r'\.gcode$','',source_file)
    try:
        os.rename(source_file, dest_file+".acc.bak")
    except FileExistsError:
        os.remove(dest_file+".acc.bak")
        os.rename(source_file, dest_file+".acc.bak")
    dest_file = re.sub(r'\.gcode$','',source_file)
    dest_file = dest_file + '.gcode'
else:
    dest_file = source_file
    os.remove(source_file)

# Boolean variables
in_internal_perimeter = False
in_external_perimeter = False
in_overhang_perimeter = False
in_internal_infill = False
in_solid_infill = False
in_ironing = False
in_bridge_infill = False
in_internal_bridge_infill = False
in_gap_fill = False
in_support_material = False
in_support_material_interface = False
in_wipe_tower = False
in_travel = False

# Open the destination file and write
with open(dest_file, "w") as of:
    of.write('; Ensure macros are properly setup in klipper\n')
    of.write('; If they are not this print will error before it starts to prevent an issue mid-print\n')
    of.write('_USE_INTERNAL_PERIMETER_VSS\n')
    of.write('_USE_EXTERNAL_PERIMETER_VSS\n')
    of.write('_USE_OVERHANG_PERIMETER_VSS\n')
    of.write('_USE_INTERNAL_INFILL_VSS\n')
    of.write('_USE_SOLID_INFILL_VSS\n')
    of.write('_USE_IRONING_VSS\n')
    of.write('_USE_BRIDGE_INFILL_VSS\n')
    of.write('_USE_INTERNAL_BRIDGE_INFILL_VSS\n')
    of.write('_USE_GAP_FILL_VSS\n')
    of.write('_USE_SUPPORT_MATERIAL_VSS\n')
    of.write('_USE_SUPPORT_MATERIAL_INTERFACE_VSS\n')
    of.write('_USE_WIPE_TOWER_VSS\n')
    of.write('_USE_TRAVEL_VSS\n')
    of.write('_USE_NORMAL_VSS\n')
    for line_Index in range(len(lines)):
        oline = lines[line_Index]
        # print(oline)
        # Parse gcode line
        if oline.startswith(';TYPE:Internal perimeter'):
            in_internal_perimeter = True
            of.write(oline)
            of.write('_USE_INTERNAL_PERIMETER_VSS\n')
        elif oline.startswith(';TYPE:External perimeter') or oline.startswith(';TYPE:Top solid infill'):
            in_external_perimeter = True
            of.write(oline)
            of.write('_USE_EXTERNAL_PERIMETER_VSS\n')
        elif oline.startswith(';TYPE:Overhang perimeter'):
            in_overhang_perimeter = True
            of.write(oline)
            of.write('_USE_OVERHANG_PERIMETER_VSS\n')
        elif oline.startswith(';TYPE:Internal infill'):
            in_internal_infill = True
            of.write(oline)
            of.write('_USE_INTERNAL_INFILL_VSS\n')
        elif oline.startswith(';TYPE:Solid infill'):
            in_solid_infill = True
            of.write(oline)
            of.write('_USE_SOLID_INFILL_VSS\n')
        elif oline.startswith(';TYPE:Ironing'):
            in_ironing = True
            of.write(oline)
            of.write('_USE_IRONING_VSS\n')
        elif oline.startswith(';TYPE:Bridge infill'):
            in_bridge_infill = True
            of.write(oline)
            of.write('_USE_BRIDGE_INFILL_VSS\n')
        elif oline.startswith(';TYPE:Internal bridge infill'):
            in_internal_bridge_infill = True
            of.write(oline)
            of.write('_USE_INTERNAL_BRIDGE_INFILL_VSS\n')
        elif oline.startswith(';TYPE:Thin wall') or oline.startswith(';TYPE:Gap fill'):
            in_gap_fill = True
            of.write(oline)
            of.write('_USE_GAP_FILL_VSS\n')
        elif oline.startswith(';TYPE:Support material'):
            in_support_material = True
            of.write(oline)
            of.write('_USE_SUPPORT_MATERIAL_VSS\n')
        elif oline.startswith(';TYPE:Support material interface'):
            in_support_material_interface = True
            of.write(oline)
            of.write('_USE_SUPPORT_MATERIAL_INTERFACE_VSS\n')
        elif oline.startswith(';TYPE:Wipe tower'):
            in_wipe_tower = True
            of.write(oline)
            of.write('_USE_WIPE_TOWER_VSS\n')
        elif oline.startswith(';TYPE:Travel'):
            in_travel = True
            of.write(oline)
            of.write('_USE_TRAVEL_VSS\n')
        elif oline.startswith('; INIT') or oline.startswith(';TYPE:Unknown') or oline.startswith(';TYPE:Skirt') or oline.startswith(';TYPE:Mill') or oline.startswith(';TYPE:Custom') or oline.startswith(';TYPE:Mixed'):
            in_internal_perimeter = False
            in_external_perimeter = False
            in_overhang_perimeter = False
            in_internal_infill = False
            in_solid_infill = False
            in_ironing = False
            in_bridge_infill = False
            in_internal_bridge_infill = False
            in_gap_fill = False
            in_support_material = False
            in_support_material_interface = False
            in_wipe_tower = False
            in_travel = False
            of.write(oline)
            of.write('_USE_NORMAL_VSS\n')
        else:
            of.write(oline)

of.close()
f.close()