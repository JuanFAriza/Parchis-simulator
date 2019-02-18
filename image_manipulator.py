from PIL import Image

def open_image(path):
    newImage = Image.open(path)
    return newImage

def save_image(image, path):
    image.save(path, 'png')

def create_image(width, height):
    image = Image.new("RGB", (width, height), "white")
    return image

def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height:
        return None

    pixel = image.getpixel((i,j))
    return pixel

def convert_grayscale(image):
    width, height = image.size

    new = create_image(width, height)
    pixels = new.load()

    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)

            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            gray_weighted = (red*0.299) + (green*0.587) + (blue*0.114)
            gray_mean = (red*0.33333) + (green*0.33333) + (blue*0.33334)

            gray = int(gray_mean)
            pixels[i, j] = (gray, gray, gray)

    return new

def diag_changes(image):
    width, height = image.size

    for i in range(1,min(width, height)):
        pixel_0 = get_pixel(image, i-1, i-1)
        pixel_1 = get_pixel(image, i, i)
        dif = (pixel_0[0] - pixel_1[0], pixel_0[1] - pixel_1[1], pixel_0[2] - pixel_1[2])
        
        if dif != (0,0,0):
            print(i,",",i)

def hor_changes(image):
    width, height = image.size

    for i in range(1,width):
        pixel_0 = get_pixel(image, i-1, 10)
        pixel_1 = get_pixel(image, i, 10)
        dif = (pixel_0[0] - pixel_1[0], pixel_0[1] - pixel_1[1], pixel_0[2] - pixel_1[2])
        
        if dif != (0,0,0):
            print(i,",",10)

def ver_changes(image):
    width, height = image.size

    for i in range(1,height):
        pixel_0 = get_pixel(image, 585, i-1)
        pixel_1 = get_pixel(image, 585, i)
        dif = (pixel_0[0] - pixel_1[0], pixel_0[1] - pixel_1[1], pixel_0[2] - pixel_1[2])
        
        if dif != (0,0,0):
            print(585,",",i)

def widen_corners(image, widen):
    width, height = image.size

    new = image.copy()
    pixels = new.load()
    color = (153, 76, 0)
    
    for i in range(widen):
        for j in range(widen):
            pixels[i, j] = color
            pixels[width - 1 - i, j] = color
            pixels[width - 1 - i, height - 1 - j] = color
            pixels[i, height - 1 - j] = color
    
    return new

def widen_borders(image, widen):
    width, height = image.size

    new = image.copy()
    pixels = new.load()
    color = (153, 76, 0)
    
    for i in range(widen,width - widen):
        for j in range(widen):
            pixels[i,j] = color
            pixels[i,(height - 1) - j] = color

    for j in range(widen,height - widen):
        for i in range(widen):
            pixels[i,j] = color
            pixels[(width - 1) - i,j] = color
    
    return new

def add_borders(image, wide):
    width, height = image.size
    width += 2*wide
    height += 2*wide
    
    old = image.copy()
    new = create_image(width, height)
    
    pixels_new = new.load()
    pixels_old = old.load()

    color = (153, 76, 0)
    
    for i in range(width):
        for j in range(wide):
            pixels_new[i,j] = color
            pixels_new[i,(height - 1) - j] = color

    for j in range(wide,height - wide):
        for i in range(wide):
            pixels_new[i,j] = color
            pixels_new[(width - 1) - i,j] = color

    for i in range(wide,width - wide):
        for j in range(wide, height - wide):
            pixels_new[i,j] = pixels_old[i - wide,j - wide]
    
    return new

def widen_blacks(image):
    width, height = image.size
    
    old = image.copy()
    new = image.copy()
    
    pixels_new = new.load()
    pixels_old = old.load()

    color = (0, 0, 0)
    for i in range(1,width - 1):
        for j in range(1,height - 1):
            pixel = pixels_old[i,j]
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            
            if red < 90 and green < 60 and blue < 90:
                pixels_new[i,j] = color
                pixels_new[i + 1,j] = color
                pixels_new[i,j + 1] = color
                pixels_new[i - 1, j] = color
                pixels_new[i,j - 1] = color

                pixels_new[i + 1,j + 1] = color
                pixels_new[i + 1,j - 1] = color
                pixels_new[i - 1,j - 1] = color
                pixels_new[i - 1,j + 1] = color
                
    return new
#image = open_image("board.png")

#gray_image = convert_grayscale(image)

#save_image(gray_image, "gray_mean.png")

path = "board_borders.png"
copy = open_image(path)

path_edit = "edit.png"
edit = widen_blacks(copy)

save_image(edit, path_edit)

