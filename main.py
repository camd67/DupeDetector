import sys
from os import listdir, makedirs
from os.path import isfile, join
import hashlib
from PIL import Image
import datetime
from shutil import copyfile

def main():
    if len(sys.argv) == 3:
        firstFolder = getAllImageHashes(sys.argv[1])
        secondFolder = getAllImageHashes(sys.argv[2])
        printDifferences(firstFolder, secondFolder)
    else if len(sys.argv) == 2:
        folder = getAllImageHashes(sys.argv[1])
        printDifferences(folder, None)
    else:
        print("Improper arguments given")
        print("")
        print("Usage:")
        print("main.py <folder1> [folder2]")

def printDifferences(folder1, folder2):
    matchFound = False
    now = datetime.datetime.now()
    destFolder = "{}{}{}-{}-{}".format(now.year, now.month, now.day, now.second, now.microsecond)
    makedirs(destFolder)
    matchCount = 0
    # Only dissalow matching filenames if in the same directory
    if folder2 == None:
        for f1 in folder1:
            for f2 in folder1:
                if f1[1] == f2[1] and f1[0] != f2[0]:
                    matchCount += 1
                    copyfile(f1[0], destFolder + "\\{" + str(matchCount) + "} " + getOnlyFilename(f1[0]))
                    copyfile(f2[0], destFolder + "\\{" + str(matchCount) + "} " + getOnlyFilename(f2[0]))
                    matchFound = True
                    print("{ Match found: ")
                    print("\t" + f1[0])
                    print("\t" + f2[0])
                    print("}")
    else:
        for f1 in folder1:
            for f2 in folder2:
                if f1[1] == f2[1]:
                    matchCount += 1
                    matchFound = True
                    processMatchedImages(f1, f2, matchCount, destFolder)

    if not matchFound:
        print("No matches found!")

def processMatchedImages(img1, img2, matchCount, destFolder):
    copyfile(img1[0], destFolder + "\\{" + str(matchCount) + "} " + getOnlyFilename(img1[0]))
    copyfile(img2[0], destFolder + "\\{" + str(matchCount) + "} " + getOnlyFilename(img2[0]))
    print("{ Match #" + str(matchCount) + " found: ")
    print("  " + img1[0])
    print("  " + img2[0])
    print("}")

def getOnlyFilename(fullpath):
    return fullpath.split("\\")[-1]

def getAllImageHashes(folder):
    onlyfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and not f.endswith(".ini") and not f.endswith(".db")]
    hashedFiles = []
    fileLength = len(onlyfiles)
    for f in onlyfiles:
        hashedFiles.append((f, dhash(Image.open(f))))
    print("Hashed all files from folder: "+ folder)
    return hashedFiles

def dhash(image, hash_size = 8):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixels = list(image.getdata())

    # Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)

if __name__ == '__main__':
    main()
