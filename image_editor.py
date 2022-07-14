class ImageResizer:
    def __init__(self, image, target_height, target_width=None) -> None:
        self.image = image
        self.target_height = target_height
        self.target_width = target_width
    
    def resize(self):
        new_width = self.target_height * self.image.width / self.image.height # calculate new width
        image_resized = self.image.resize((int(new_width), int(self.target_height))) # resize image
        if self.target_width is None: return image_resized # if the image should stay wide for scrolling homescreens, return the image
        left_crop = (image_resized.width - self.target_width) / 2 # calculate left crop
        right_crop = (image_resized.width + self.target_width) / 2 # calculate right crop
        image_cropped = image_resized.crop((int(left_crop), 0, int(right_crop), image_resized.height)) # crop image
        return image_cropped # return cropped image

# if __name__ == '__main__':
#     image_resizer = ImageResizer(Image.open('images/fullsize/weic2205a.tif'), 2340, 1080)
#     image_resizer.resize().show()