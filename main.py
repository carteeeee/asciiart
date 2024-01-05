from PIL import Image, ImageFont, ImageDraw # import pil for silly image shenanigans
import numpy as np                          # import numpy for silly --meth-- math shenanigans
import string                               # import string for silly ascii shenanigans

PNW = [i for i in string.printable if i not in string.whitespace] # PNW: Printable Not Whitespace

def calclightness(chars, font, box):                                        # calculate lightness of each input char using PIL and numpy
    result = {}
    for char in chars:
        image = Image.new("L", (box[2], box[3]), "black")                   # greyscale image w/ black bg
        draw = ImageDraw.Draw(image)                                        # make imagedraw object
        draw.text((box[0], box[1]), char, font=font, fill="white")          # make text
        arr = np.array(image).flatten()                                     # convert image to np array (and flatten it)
        avg = np.average(arr)                                               # get avg of array
        result[char] = avg                                                  # add avg to result dict
    resvals = np.array(list(result.values()))                               # get vals of result
    resvals = (resvals-np.min(resvals)) / (np.max(resvals)-np.min(resvals)) # normalize vals
    result = dict(zip(result.keys(), resvals))                              # add back together
    return result                                                           # return

def getchar(target, chars):                                   # get char closest to target (between 0 and 1)
    return min(chars, key=lambda x: abs(chars.get(x)-target)) # literally just one line

def displayimage(image, box, chars, height):                              # displays an image using the charlightness
    image = image.convert("L")                                            # convert the image to greyscale
    iratio = height/image.size[1]                                         # compute image ratio
    bratio = box[2]/box[3]                                                # compute box ratio
    image = image.resize((int(image.size[0]*iratio), int(height*bratio))) # resize image
    arr = np.array(image)/255                                             # convert image to np array (and divide by 255)
    print("\033[1m", end="")                                              # make bold
    for row in arr:                                                       # for each row
        for col in row:                                                   # for each pixel in row
            print(getchar(col, chars), end="")                            # print pixel
        print("\n", end="")                                               # after full row has been printed, make a newline
    print("\033[0m", end="")                                              # stop balding!! (bolding)

if __name__ == "__main__":
    font = ImageFont.truetype(input("font path: "), 100)            # get font
    box = font.getbbox("█")                                         # get bounding box of font
    charlightness = calclightness(PNW, font, box)                   # calc char lightness
    image = Image.open(input("path to image: "))                    # open an image
    displayimage(image, box, charlightness, int(input("height: "))) # display the image
