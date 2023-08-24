from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    divides = image_size[0] % tile_size[0] == 0 and image_size[1]%tile_size[1] == 0
    div = (image_size[0]*image_size[1]) // (tile_size[0]*tile_size[1])
    # print(f"\ndiv+{div} imsize: {image_size}, tilesize: {tile_size}")
    orderingCorrect = len(set(ordering)) == div and all([x in list(range(div)) for x in ordering])

    return divides and orderingCorrect



def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    original_image = Image.open(image_path)
    image_size = original_image.size
    new_image = Image.new(mode="RGB", size=image_size)

    if not valid_input(image_size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")
    xdiv = image_size[0] // tile_size[0]
    # print(f"xdiv {xdiv}")
    ydiv = image_size[1] // tile_size[1]
    # print(f"ydiv {ydiv}")
    y= 0
    x=0
    for y in range(ydiv):
        for x in range(xdiv):
            # INDEX OF CURRENT IMAGE POINTER
            index = xdiv*y + x

            # THE POSITION IN CURRENT IMAGE (NEW IMAGE WHERE PIECES ARE PASTED)
            origpos = (x*tile_size[0], y*tile_size[1])

            # INDEX FROM WHERE TO GET FROM SCRAMBLED IMAGE
            getindex = ordering[index]

            # THE POSITION TO GET FROM THE SCRAMBLED IMAGE
            getpos = (getindex%xdiv * tile_size[0], getindex//xdiv * tile_size[1])

            tile = original_image.crop(
                (
                    getpos[0], # left
                    getpos[1], # top
                    getpos[0]+tile_size[0], # right
                    getpos[1]+tile_size[1] # bottom
                )
            )
            new_image.paste(tile, origpos)

    new_image.save(out_path)
    original_image.close()
    new_image.close()




rearrange_tiles("images/great_wave_scrambled.png", (16, 16), [int(x) for x in open("images/great_wave_order.txt").readlines()], "images/my.png")
# rearrange_tiles("images/pydis_logo_scrambled.png", (256, 256), [0,1,2,3,4,5,6,7], "images/my.png")



