"""
Created on Tue Jan 28 13:15:28 2025
# Python Script, API Version = V231
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


# Function to set the view mode
def set_view_mode(mode):
    result = ViewHelper.SetViewMode(mode, None)
    return result

# Function to set the sketch plane
def set_sketch_plane(plane):
    result = ViewHelper.SetSketchPlane(plane, None)
    return result

# Function to create a rectangle sketch
def create_rectangle_sketch(point1, point2, point3):
    surface = SketchRectangle.Create(point1, point2, point3)
    return surface

# Function to extrude a face
def extrude_face(face, height):
    options = ExtrudeFaceOptions()
    options.ExtrudeType = ExtrudeType.Add
    body = ExtrudeFaces.Execute(face, height, options)
    return body

# Function to translate a body along a given direction
def translate_body(body, direction, distance):
    options = MoveOptions()
    result = Move.Translate(body, direction, distance, options)
    return result

# Function to handle body creation and translation
def create_and_translate_body(locations, body_index):
    name = "body" + str(body_index + 1)
    x = locations[body_index][0]
    y = locations[body_index][1]
    
    # Create a copy of the body
    new_body = Copy.Execute(BodySelection.Create(GetRootPart().Bodies[0]))

    # Set named selection
    primary_selection = BodySelection.Create(GetRootPart().Bodies[body_index+1])
    secondary_selection = Selection.Empty()
    result = NamedSelection.Create(primary_selection, secondary_selection)
    result = NamedSelection.Rename("Group1", name)

    # Translate along Y-axis
    selection = BodySelection.Create(GetRootPart().Bodies[body_index+1])
    result = translate_body(selection, Direction.DirY, MM(y))

    # Translate along X-axis
    selection = BodySelection.Create(GetRootPart().Bodies[body_index+1])
    result = translate_body(selection, Direction.DirX, MM(x))

# Main Script Execution

# Solidify Sketch
set_view_mode(InteractionMode.Solid)

# Set Sketch Plane
set_sketch_plane(Plane.PlaneXY)

# Sketch Rectangle
point1 = Point2D.Create(MM(-0.1), MM(-0.1))
point2 = Point2D.Create(MM(-0.1), MM(0.1))
point3 = Point2D.Create(MM(0.1), MM(0.1))
create_rectangle_sketch(point1, point2, point3)

# Solidify Sketch again
set_view_mode(InteractionMode.Solid)

# Extrude 1 Face
face = FaceSelection.Create(GetRootPart().Bodies[0].Faces[0])
extrude_face(face, MM(0.2))

# Locations for body translations
file_path = r"C:\Users\qrt1kor\Downloads\TopPoints_PCB (1).txt"  # Replace with your file path
locations = read_and_extract_columns(file_path)
rows = len(locations)

# Loop through body locations and translate
for i in range(rows):
    create_and_translate_body(locations, i)

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[0])
result = Delete.Execute(selection)

for i in range(rows):
    foce_name = "Spring_face" + str(i+1)
    # Create Named Selection Group
    primarySelection = FaceSelection.Create(GetRootPart().Bodies[i+1].Faces[5])
    secondarySelection = Selection.Empty()
    result = NamedSelection.Create(primary_selection, secondary_selection)
    result = NamedSelection.Rename("Group1", foce_name)