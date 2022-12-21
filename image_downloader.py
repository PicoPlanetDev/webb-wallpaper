import requests
from bs4 import BeautifulSoup
import pathlib
import os

GALLERY_URL = 'https://esawebb.org/images/archive/search/?minimum_size=0&ranking=0&instrument=3&instrument=2&instrument=1&instrument=5&instrument=4&facility=1&id=&release_id=&published_since_day=&published_since_month=&published_since_year=&published_until_day=&published_until_month=&published_until_year=&title=&subject_name=&description=&credit=&fov=0'
FULLSIZE_URL = 'https://esawebb.org/media/archives/images/original/'

class ImageDownloader:
    def __init__(self) -> None:
        self.gallery = requests.get(GALLERY_URL)
        self.soup = BeautifulSoup(self.gallery.text, 'html.parser')

        self.gallery_imgs = self.get_gallery_imgs()
        self.banner_paths = self.get_banners()
        self.img_names = self.get_image_names()

    def get_gallery_imgs(self) -> list:
        imgs = self.soup.find_all('img')
        gallery_imgs = []
        for img in imgs:
            if img['src'].startswith('https://cdn.esawebb.org/archives/images/screen/'):
                gallery_imgs.append(img)
        return gallery_imgs


    def get_banners(self) -> list:
        banner_paths = []
        for gallery_img in self.gallery_imgs:
            img_url = gallery_img.get('src')
            img_path = pathlib.Path('static', 'banner', img_url.split('/')[-1])
            if img_path.exists():
                banner_paths.append(img_path)
            else:
                img = requests.get(img_url)
                with open(img_path, 'wb') as f:
                    f.write(img.content)
                # print(f'{img_path} downloaded')
                banner_paths.append(img_path)
        return banner_paths

    def get_image_names(self) -> list:
        img_names = []
        for gallery_img in self.gallery_imgs:
            parent_href = gallery_img.parent['href'] # parent is a link
            img_names.append(parent_href.split('/')[-2]) # looks like /images/name/
        return img_names

    def get_image(self, name) -> str:
        image_path = pathlib.Path('images', 'fullsize', name + '.tif')
        if image_path.exists():
            return image_path
        else:
            image_url = f'{FULLSIZE_URL}{name}.tif'
            image = requests.get(image_url)
            with open(image_path, 'wb') as f:
                f.write(image.content)
            print(f'{image_path} downloaded')
            return image_path

if __name__ == '__main__':
    image_downloader = ImageDownloader()