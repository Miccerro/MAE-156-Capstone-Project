import math

def polar_to_cartesian(radius, angle_deg):
    angle_rad = math.radians(angle_deg)
    y = radius * math.cos(angle_rad)  # Cosine for Y coordinate (new Z)
    z = radius * math.sin(angle_rad)  # Sine for Z coordinate (new Y)
    return y, z

def convert_mm_to_steps(mm, conversion_factor):
    steps = mm / conversion_factor
    if abs(steps) < 0.01:  # If very small, consider it as 0
        return 0
    else:
        return round(steps, 2)  # Round to two decimal places

def main():
    ##LARGER WAGON WHEEL
    radius = 31  # Radius of the circle in mm
    num_spokes = 16  # Number of spokes

    ##SMALLER WAGON WHEEL
    #radius = 39/2  # Radius of the circle in mm
    #num_spokes = 8  # Number of spokes
    spoke_angle_deg = 360 / num_spokes  # Angle between spokes in degrees

    spoke1_angle_deg = 270  # Angle of spoke 1 in degrees
    spoke1_y, spoke1_z = polar_to_cartesian(radius, spoke1_angle_deg)

    print("Spoke 1 coordinates (Y, Z):", spoke1_y, ",", spoke1_z)

    y_conversion_factor = 32 / 10000  # Conversion factor for Y coordinate in mm/steps
    z_conversion_factor = 10 / 200    # Conversion factor for Z coordinate in mm/steps

    y_steps_dict = {}
    z_steps_dict = {}

    for i in range(2, num_spokes + 1):
        spoke_angle = (spoke1_angle_deg + (i - 1) * spoke_angle_deg) % 360
        y, z = polar_to_cartesian(radius, spoke_angle)
        diff_y = y - spoke1_y
        diff_z = z - spoke1_z

        y_steps = convert_mm_to_steps(diff_y, y_conversion_factor)
        z_steps = convert_mm_to_steps(diff_z, z_conversion_factor)

        y_steps_dict[f"Spoke 1 to spoke {i}"] = y_steps
        z_steps_dict[f"Spoke 1 to spoke {i}"] = z_steps

    print("Y steps:", y_steps_dict)
    print("Z steps:", z_steps_dict)

if __name__ == "__main__":
    main()
