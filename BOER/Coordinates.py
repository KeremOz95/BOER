




# class Barkot:
#     def __init__(self, x1, y1, x2, y2, type, inside, match):
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2
#         self.type = type
#         self.inside = inside
#         self.match = match

# class Match:
#     def __init__(self, barkot1, barkot2):
#         self.barkot1 = barkot1
#         self.barkot2 = barkot2

# def set_coordinates(barkot, x1, y1, x2, y2):
#     barkot.x1 = x1
#     barkot.y1 = y1
#     barkot.x2 = x2
#     barkot.y2 = y2

# def set_inside(barkot, inside):
#     barkot.inside = inside

# def set_type(barkot, type):
#     barkot.type = type

# def matching(barkot1, barkot2):
#     if (barkot1.inside == barkot2.inside):
import re

file_path = "C:\\Users\\Kerem\\Desktop\\cr.txt"
barcode_data = []

coord_pattern = r"\((\d+),(\d+)\)"
type_code_pattern = r"(\w+)_p_(.+)$"

with open(file_path, "r") as file:
    for line in file:
        coords = re.findall(coord_pattern, line)
        type_code_match = re.search(type_code_pattern, line)

        if coords and type_code_match:
            x1, y1 = map(int, coords[0])
            x3, y3 = map(int, coords[2])
            midpoint = ((x1 + x3) // 2, (y1 + y3) // 2)

            barcode_data.append({
                "coordinates": [(int(x), int(y)) for x, y in coords],
                "type": type_code_match.group(1),
                "value": type_code_match.group(2),
                "midpoint": midpoint
            })

# Örnek çıktı
for item in barcode_data:
    print(f"Type: {item['type']}, Value: {item['value']}, Midpoint: {item['midpoint']}")
