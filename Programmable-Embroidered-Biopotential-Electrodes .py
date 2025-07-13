# ==============================================================================
# Title     : Programmable Embroidered Biopotential Electrodes
# Authors   : Prof. SUN Ye, 
#             Faisal Rehman 
#
#             Department of Mechanical and Aerospace Engineering 
#             University of Virginia,Charlottesville VA USA. 
#############################################################
# Affiliation: SUN Lab, UVA
#############################################################
# Description:
#   This script generates programmable embroidery designs for biopotential 
#   electrodes using a triangle wave pattern in circular and rectangular shapes. 
#   The output includes both EXP and DST embroidery machine files and a visual 
#   plot of the electrode structure.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from pyembroidery import EmbPattern, write_exp, write_dst, read_dst, STITCH, END, COLOR_CHANGE
from datetime import datetime
#####################################################################################################################
# Parameters for the circles in millimeters
outer_radius = 30         # Outer circle radius
inner_radius = 30         # Inner circle radius (new)
new_circle_radius = 7     # Radius of the new circle at the free end of the rectangle
rectangle_length_mm = 20  # Length of the rectangle
rectangle_width_mm = 5    # Width of the rectangle
#####################################################################################################################
# Stithces controll Process and Parametters
circle_stitch_spacing_mm = 2.00     # Spacing between stitches for outer and inner circles
line_spacing_mm = 3.000              # Spacing between lines (used in circle patterns)
rectangle_stitch_spacing_mm = 1.45   # Spacing between stitches for the rectangle and other patterns
# Initialize the embroidery pattern
pattern = EmbPattern()
# Initialize the stitch counter
stitch_count = 0
# Machine JONOME Hoop size Setting units (mm)
hoop_width_mm = 80
hoop_height_mm = 90
#####################################################################################################################
# Function to add a line with stitches to the embroidery pattern and count stitches
def add_line_with_stitches(x0, y0, x1, y1, stitch_spacing, pattern):
    global stitch_count
    length = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    num_stitches = max(int(length / stitch_spacing), 1)  # Ensure at least one stitch
    for i in range(num_stitches + 1):
        t = i / num_stitches
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        pattern.add_stitch_absolute(STITCH, x * 10, y * 10)  # Scale to decipoints (10 times the millimeter value)
        stitch_count += 1
#####################################################################################################################
# Function to generate a timestamped filename
def generate_timestamped_filename(base_name, extension):
    timestamp = datetime.now().strftime("%H-%M-%d-%m-%Y")
    return f"{timestamp}_{base_name}.{extension}"
#####################################################################################################################
# Function to draw a triangle wave pattern inside a circle Inner Circle 
def draw_triangle_wave_circle(center_x, center_y, radius_mm, stitch_spacing_mm, pattern):
    x = np.arange(-radius_mm, radius_mm + line_spacing_mm, stitch_spacing_mm)
    y_values = []
    x_values = []

    for i in range(len(x)):
        value_inside_sqrt = radius_mm**2 - x[i]**2
        if value_inside_sqrt < 0:
            value_inside_sqrt = 0
        y = np.sqrt(value_inside_sqrt)
        y_values.extend([-y, y])
        x_values.extend([x[i], x[i]])

    for i in range(len(x_values) - 1):
        add_line_with_stitches(x_values[i] + center_x, y_values[i] + center_y, x_values[i + 1] + center_x, y_values[i + 1] + center_y, stitch_spacing_mm, pattern)

    return x_values, y_values
#####################################################################################################################
# Function to draw a rotated triangle wave pattern inside a outside circle
def draw_rotated_triangle_wave_circle(center_x, center_y, radius_mm, stitch_spacing_mm, pattern):
    x = np.arange(-radius_mm, radius_mm + line_spacing_mm, stitch_spacing_mm)
    y_values = []
    x_values = []

    for i in range(len(x)):
        value_inside_sqrt = radius_mm**2 - x[i]**2
        if value_inside_sqrt < 0:
            value_inside_sqrt = 0
        y = np.sqrt(value_inside_sqrt)
        y_values.extend([y, -y])
        x_values.extend([x[i], x[i]])

    # Rotate by 90 degrees (swap x and y)
    rotated_x_values = y_values
    rotated_y_values = x_values

    for i in range(len(rotated_x_values) - 1):
        add_line_with_stitches(rotated_x_values[i] + center_x, rotated_y_values[i] + center_y, rotated_x_values[i + 1] + center_x, rotated_y_values[i + 1] + center_y, stitch_spacing_mm, pattern)

    return rotated_x_values, rotated_y_values
#######################################################################################################################
# Function to draw a continuous triangle wave pattern within a rectangle with added density
def draw_square_wave_with_cross_and_diagonal_lines_rectangle(x0, y0, length_mm, width_mm, stitch_spacing_mm, pattern):
    x_start = x0
    x_end = x0 + length_mm
    y_top = y0 + width_mm / 2
    y_bottom = y0 - width_mm / 2

    rect_x_values = []
    rect_y_values = []

    # Start from the bottom and move up
    y = y_bottom
    line_spacing_mm = 1.0  # Spacing between horizontal lines

    toggle = True  # To alternate the direction of the lines

    while y <= y_top:
        if toggle:
            # Draw line from left to right
            add_line_with_stitches(x_start, y, x_end, y, stitch_spacing_mm, pattern)
            rect_x_values.extend([x_start, x_end])
            rect_y_values.extend([y, y])
        else:
            # Draw line from right to left
            add_line_with_stitches(x_end, y, x_start, y, stitch_spacing_mm, pattern)
            rect_x_values.extend([x_end, x_start])
            rect_y_values.extend([y, y])

        y += line_spacing_mm        # Move up to the next line
        toggle = not toggle         # Toggle direction

    return rect_x_values, rect_y_values
######################################################################################################################
# Function to draw an intersecting triangle wave pattern within a rectangle
def draw_intersecting_triangle_wave_rectangle(x0, y0, length_mm, width_mm, stitch_spacing_mm, pattern):
    x = x0
    y_top = y0 + width_mm / 2
    y_bottom = y0 - width_mm / 2

    rect_x_values = []
    rect_y_values = []

    while x < x0 + length_mm:
        # Draw diagonal from bottom to top
        add_line_with_stitches(x, y_bottom, x + stitch_spacing_mm, y_top, stitch_spacing_mm, pattern)
        rect_x_values.extend([x, x + stitch_spacing_mm])
        rect_y_values.extend([y_bottom, y_top])
        x += stitch_spacing_mm               # Move horizontally to continue the wave

        # Draw diagonal from top to bottom
        add_line_with_stitches(x, y_top, x + stitch_spacing_mm, y_bottom, stitch_spacing_mm, pattern)
        rect_x_values.extend([x, x + stitch_spacing_mm])
        rect_y_values.extend([y_top, y_bottom])

        x += stitch_spacing_mm   # Move horizontally to continue the wave

    return rect_x_values, rect_y_values
#####################################################################################################################
# Draw the continuous triangle wave pattern inside the outer circle
outer_x_values, outer_y_values = draw_triangle_wave_circle(0, 0, outer_radius / 2, circle_stitch_spacing_mm, pattern)

# Connect the end of the outer circle's pattern to the start of the rectangle's pattern
last_x = outer_x_values[-1]- 3.5
last_y = outer_y_values[-1]
##################################################################################################################
# Draw the first continuous triangle wave pattern inside the rectangle
rect_x_values, rect_y_values = draw_square_wave_with_cross_and_diagonal_lines_rectangle(last_x, last_y, rectangle_length_mm, rectangle_width_mm, rectangle_stitch_spacing_mm, pattern)

# Draw the intersecting triangle wave pattern inside the rectangle
rect_intersect_x_values, rect_intersect_y_values = draw_intersecting_triangle_wave_rectangle(last_x, last_y, rectangle_length_mm, rectangle_width_mm, rectangle_stitch_spacing_mm, pattern)

# Continue the pattern from the end of the rectangle to the start of the inner circle
last_x = last_x + rectangle_length_mm
last_y = (rect_y_values[-1] + rect_y_values[0]) / 2  # Center Y-coordinate of the rectangle

# Draw the cross pattern inside the inner circle, rotated 45 degrees
inner_x_values, inner_y_values = draw_rotated_triangle_wave_circle(0, 0, inner_radius / 2, circle_stitch_spacing_mm, pattern)

# Draw the new circle at the end of the second rectangle
new_circle_x = last_x + 3
new_circle_y = last_y - 0.60
new_circle_x_values, new_circle_y_values = draw_triangle_wave_circle(new_circle_x, new_circle_y, new_circle_radius, rectangle_stitch_spacing_mm, pattern)

# Draw the rotated triangle wave pattern (cross pattern) inside the new circle
new_circle_cross_x_values, new_circle_cross_y_values = draw_rotated_triangle_wave_circle(new_circle_x, new_circle_y, new_circle_radius, rectangle_stitch_spacing_mm, pattern)
#####################################################################################################################
# Center the design within the hoop area
all_x_values = outer_x_values + list(rect_x_values) + list(rect_intersect_x_values) + inner_x_values + list(new_circle_x_values) + list(new_circle_cross_x_values)
all_y_values = outer_y_values + list(rect_y_values) + list(rect_intersect_y_values) + inner_y_values + list(new_circle_y_values) + list(new_circle_cross_y_values)
design_width = max(all_x_values) - min(all_x_values)
design_height = max(all_y_values) - min(all_y_values)
x_offset = (hoop_width_mm - design_width) / 2 - min(all_x_values)
y_offset = (hoop_height_mm - design_height) / 2 - min(all_y_values)
#####################################################################################################################
# Apply the offset to all coordinates to center the design
outer_x_values = np.array(outer_x_values) + x_offset
outer_y_values = np.array(outer_y_values) + y_offset
rect_x_values = np.array(rect_x_values) + x_offset
rect_y_values = np.array(rect_y_values) + y_offset
rect_intersect_x_values = np.array(rect_intersect_x_values) + x_offset
rect_intersect_y_values = np.array(rect_intersect_y_values) + y_offset
new_circle_x_values = np.array(new_circle_x_values) + x_offset
new_circle_y_values = np.array(new_circle_y_values) + y_offset
new_circle_cross_x_values = np.array(new_circle_cross_x_values) + x_offset
new_circle_cross_y_values = np.array(new_circle_cross_y_values) + y_offset
inner_x_rot = (np.array(inner_x_values) * np.cos(np.pi/4) - np.array(inner_y_values) * np.sin(np.pi/4)) + x_offset
inner_y_rot = (np.array(inner_x_values) * np.sin(np.pi/4) + np.array(inner_y_values) * np.cos(np.pi/4)) + y_offset
#####################################################################################################################
# Finalize the embroidery pattern with proper start and end commands
pattern.add_command(STITCH, 0, 0)  # Starting point
pattern.add_command(COLOR_CHANGE, 0, 0)  # Color change to signal start
pattern.add_command(END, 0, 0)  # Add end command
#####################################################################################################################
# Generate timestamped filenames for the output files
exp_filename = generate_timestamped_filename("Electrode", "exp")
dst_filename = generate_timestamped_filename("Electrode", "dst")
#####################################################################################################################
# Save the pattern as EXP and DST files
write_exp(pattern, exp_filename)
write_dst(pattern, dst_filename)
#####################################################################################################################
# Plot the design including the rectangle and triangle wave patterns
fig, ax = plt.subplots()
ax.set_aspect('equal')

# Set axis limits based on min/max coordinates
ax.set_xlim(min(outer_x_values.min(), rect_x_values.min(), rect_intersect_x_values.min(), inner_x_rot.min(), new_circle_x_values.min(), new_circle_cross_x_values.min()) - 10, 
            max(outer_x_values.max(), rect_x_values.max(), rect_intersect_x_values.max(), inner_x_rot.max(), new_circle_x_values.max(), new_circle_cross_x_values.max()) + 10)
ax.set_ylim(min(outer_y_values.min(), rect_y_values.min(), rect_intersect_y_values.min(), inner_y_rot.min(), new_circle_y_values.min(), new_circle_cross_y_values.min()) - 10, 
            max(outer_y_values.max(), rect_y_values.max(), rect_intersect_y_values.max(), inner_y_rot.max(), new_circle_y_values.max(), new_circle_cross_y_values.max()) + 10)

# Plot the Designed Electrode
ax.plot(outer_x_values, outer_y_values, 'b--')
# Plot the first triangle wave pattern in the rectangle
ax.plot(rect_x_values-2.5, rect_y_values, 'b--')
# Plot the intersecting triangle wave pattern in the rectangle
ax.plot(rect_intersect_x_values-2.5, rect_intersect_y_values, 'm--')
# Plot the cross pattern for the inner circle
ax.plot(inner_x_rot, inner_y_rot, 'm--')
# Plot the new circle at the free end of the rectangle
ax.plot(new_circle_x_values + 36, new_circle_y_values +1, 'b--')
# Plot the cross pattern inside the new circle
ax.plot(new_circle_cross_x_values+36, new_circle_cross_y_values+ 1, 'm--')
# Add title and labels
ax.set_title('Dry Electrode')
ax.set_xlabel('X-axis (mm)')
ax.set_ylabel('Y-axis (mm)')
plt.show()
# Print the total number of stitches
print("Total number of stitches:", stitch_count)
#####################################################################################################################
# Verify dimensions of the embroidery file
pattern_from_file = read_dst(dst_filename)
stitches = pattern_from_file.stitches
x_coords = [stitch[1] / 10 for stitch in stitches]  # Convert back to mm from decipoints
y_coords = [stitch[2] / 10 for stitch in stitches]  # Convert back to mm from decipoints
design_width_in_dst = max(x_coords) - min(x_coords)
design_height_in_dst = max(y_coords) - min(y_coords)
print("Design width in DST file: {} mm".format(design_width_in_dst))
print("Design height in DST file: {} mm".format(design_height_in_dst))
# Compare with actual design dimensions
expected_width = 2 * outer_radius / 2 + rectangle_length_mm + new_circle_radius * 2
expected_height = max(2 * outer_radius / 2, rectangle_width_mm, new_circle_radius * 2)
#####################################################################################################################