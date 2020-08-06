from sys import argv
from PIL import Image
from math import sqrt

import os
import numpy as np

# Compares a pixel and a repsentation of that pixel using a certain block
def compare(r, g, b, R, G, B):
    if abs(r - R) + abs(g - G) + abs(b - B) > 100:
        return 4294967296

    else:
        red = abs(R ** 2 - r ** 2)
        green = abs(G ** 2 - g ** 2)
        blue = abs(B ** 2 - b ** 2)

        return(red + green + blue)


# Takes a input value and converts into a cordinate for the top-left corner of a map
def xyround(x):
    x -= 64
    x -= x % 128
    x += 64
    return(x)

colours = ((127, 178, 56),         (247, 233, 163),       (199, 199, 199),         (255, 0, 0),         (160, 160, 255),    (167, 167, 167),    (0, 124, 0),
          (255, 255, 255),         (164, 168, 184),       (151, 109, 77),          (112, 112, 112),     (143, 119, 72),     (255, 252, 245),    (216, 127, 51),
          (178, 76, 216),          (102, 153, 216),       (229, 229, 51),          (127, 204, 25),      (242, 127, 165),    (76, 76, 76),       (153, 153, 153),
          (76, 127, 153),          (127, 63, 178),        (51, 76, 178),           (102, 76, 51),       (102, 127, 51),     (153, 51, 51),      (25, 25, 25),
          (250, 238, 77),          (92, 219, 213),        (74, 128, 255),          (0, 217, 58),        (129, 86, 49),      (112, 2, 0),        (209, 177, 161),
          (159, 82, 36),           (149, 87, 108),        (112, 108, 138),         (186, 133, 36),      (103, 117, 53),     (160, 77, 78),      (57, 41, 35),
          (135, 107, 98),          (87, 92, 92),          (122, 73, 88),           (76, 62, 92),        (76, 50, 35),       (76, 82, 42),       (142, 60, 46),
          (37, 22, 16),            (189, 48, 49),         (148, 63, 97),           (92, 25, 29),        (22, 126, 134),     (58, 142, 140),     (86, 44, 62),
          (20, 180, 133))

blocks = ("slime_block",           "sandstone",           "mushroom_stem",         "redstone_block",    "packed_ice",       "iron_block",       "oak_leaves[persistent=true]",
          "white_concrete",        "infested_stone",      "polished_granite",      "stone",             "oak_planks",       "quartz_block",     "honey_block",
          "magenta_concrete",      "light_blue_concrete", "yellow_concrete",       "lime_concrete",     "pink_concrete",    "gray_concrete",    "light_gray_concrete",
          "cyan_concrete",         "purple_concrete",     "blue_concrete",         "brown_concrete",    "green_concrete",   "red_concrete",     "black_concrete",
          "gold_block",            "diamond_block",       "lapis_block",           "emerald_block",     "spruce_planks",    "netherrack",       "white_terracotta",
          "orange_terracotta",     "magenta_terracotta",  "light_blue_terracotta", "yellow_terracotta", "lime_terracotta",  "pink_terracotta",  "gray_terracotta",
          "light_gray_terracotta", "cyan_terracotta",     "purple_terracotta",     "blue_terracotta",   "brown_terracotta", "green_terracotta", "red_terracotta",
          "black_terracotta",      "crimson_nylium",      "crimson_planks",        "crimson_hyphae",    "warped_nylium",    "warped_planks",    "warped_hyphae",
          "warped_wart_block")

# Checks if the user added three arguments
if len(argv) != 5:
    print("Usage: python datapack.py [image.png] [outfile.mcfunction] [x] [z]")
    exit(1)

img = Image.open(argv[1]).convert("RGB")

image = img.resize((128, 128))
pixel = image.load()

X = xyround(int(argv[3]))
Z = xyround(int(argv[4]))

# Convert an image into a .ahk file that can be run
y = np.empty((128, 128), dtype='i1')
block = np.empty((128, 128), dtype='u1')

# Pick the colours to be used
for x in range(128):
    for z in range(128):
        minDifference = 4294967296
        pixel = image.getpixel((x, z))

        for i in range(len(blocks)):
            difference = compare(round(colours[i][0] * 0.86), round(colours[i][1] * 0.86), round(colours[i][2] * 0.86), pixel[0], pixel[1], pixel[2])
            if  difference < minDifference:
                minDifference = difference

                y[x][z] = 0
                block[x][z] = i

            difference = compare(colours[i][0], colours[i][1], colours[i][2], pixel[0], pixel[1], pixel[2])
            if difference < minDifference:
                minDifference = difference

                y[x][z] = 1
                block[x][z] = i

            difference = compare(round(colours[i][0] * 0.71), round(colours[i][1] * 0.71), round(colours[i][2] * 0.71), pixel[0], pixel[1], pixel[2])
            if difference < minDifference:
                minDifference = difference

                y[x][z] = -1
                block[x][z] = i

yPos = np.empty((128, 129), dtype='i2')

try:
    os.makedirs("datapacks/mapinator/data/mapart/functions")

except OSError:
    print("")

if not os.path.isfile("datapacks/mapinator/pack.mcmeta"):
    f = open(f"datapacks/mapinator/pack.mcmeta", "a+")

    f.write('{\r\n')
    f.write('"pack":\r\n')
    f.write('  {\r\n')
    f.write('  "pack_format": 5,\r\n')
    f.write('  "description": "Mapinator: A Minecraft Map Art Generator\r\n')
    f.write('  - Made by Albert Guo for CS50x"\r\n')
    f.write('  }\r\n')
    f.write('}\r\n')

    f.close


f = open(f"datapacks/mapinator/data/mapart/functions/{argv[2]}", "a+")

for x in range(128):
    yPos[x][64] = 190

    f.write(f"setblock {X + x} 190 {Z + 64} {blocks[block[x][64]]}\r\n")

for x in range(128):
    for z in range(65, 128):
        yPos[x][z] = yPos[x][z - 1] + y[x][z]

        f.write(f"setblock {X + x} {yPos[x][z]} {Z + z} {blocks[block[x][z]]}\r\n")

for x in range(128):
    for z in range(63, -1, -1):
        yPos[x][z] = yPos[x][z + 1] - y[x][z + 1]

        f.write(f"setblock {X + x} {yPos[x][z]} {Z + z} {blocks[block[x][z]]}\r\n")

for x in range(128):
    yPos[x][128] = yPos[x][0] - y[x][0]

    f.write(f"setblock {X + x} {yPos[x][128]} {Z - 1} diamond_block\r\n")

f.close()

exit(0)