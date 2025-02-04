# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:15:28 2025

@author: QRT1KOR
"""

def read_and_extract_columns(file_path):
    with open(file_path, 'r') as file:
        # Read and process each line
        data = []
        for line in file:
            # Split the line into columns
            columns = line.split()
            # Ensure there are at least 5 columns
            if len(columns) >= 5:
                # Extract the 3rd, 4th, and 5th columns and convert them to floats
                x, y, z = float(columns[2]), float(columns[3]), float(columns[4])
                data.append([x, y, z])    
    return data

# Function to add a spring based on coordinates
def add_spring(x, i, reference_body_name="1", height=2, stiffness_values=None):
    """
    Adds a spring connection with the given coordinates x.

    Args:
        x (list): Coordinates [x, y, z] for the Mobile_Coor.
        i (int): Index for naming mobile body.
        reference_body_name (str): Name of the reference body (default: "1").
        height (float): Fixed Y-coordinate value (default: 2).
        stiffness_values (list of tuples): Spring stiffness table (default: predefined values).
    """
    mobile_body_name = "Spring_face" + str(i + 1)
    
    # Default stiffness values if none are provided
    if stiffness_values is None:
        stiffness_values = [
            (0.0, -100000.),
            (50.0, -10000.),
            (60.0, -1000.),
            (100.0, 0.),
            (140.0, 1000.)
        ]

    # Get connections from the project
    connections = ExtAPI.DataModel.Project.Model.Connections

    # Define the spring stiffness table
    spring_table = "System.Array.CreateInstance(float,5,2)\n"
    for j in range(len(stiffness_values)):
        k1, k2 = stiffness_values[j]
        spring_table += "spring_table[%d,0]=%f \nspring_table[%d,1]=%f \n" % (j, k1, j, k2)
    
    snippet = "Spring_table={}\nstiffness = CS_PointsTable(spring_table) \nspring.SetTable(stiffness)".format(spring_table)

    # Create a new spring
    spring = connections.AddSpring()
    spring.RenameBasedOnDefinition()
    spring.AddCommandSnippet().Input = snippet

    # Set the spring type and scoping
    spring.Scope = SpringScopingType.BodyToBody
    spring.LongitudinalStiffness = Quantity("10 [N Mm-1]")

    # Get reference and mobile bodies by name
    reference_body = DataModel.GetObjectsByName(reference_body_name)[0]
    mobile_body = DataModel.GetObjectsByName(mobile_body_name)[0]

    spring.ReferenceScopeLocation = reference_body
    spring.MobileScopeLocation = mobile_body

    # Set coordinates
    mobile_coor = x
    spring.ReferenceXCoordinate = Quantity(mobile_coor[0], "mm")
    spring.ReferenceYCoordinate = Quantity(mobile_coor[1] , "mm")
    spring.ReferenceZCoordinate = Quantity(height, "mm")

    spring.MobileXCoordinate = Quantity(mobile_coor[0], "mm")
    spring.MobileYCoordinate = Quantity(mobile_coor[1], "mm")
    spring.MobileZCoordinate = Quantity(0.2 , "mm")

# Example usage
file_path = r"C:\Users\qrt1kor\Downloads\TopPoints_PCB.txt"  # Replace with your file path
extracted_data = read_and_extract_columns(file_path)

# Loop through the list and add springs
i = 0
for x in extracted_data:
    add_spring(x, i, "1", 6.65 ,)
    i += 1





