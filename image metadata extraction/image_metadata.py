from PIL import Image
from PIL.ExifTags import TAGS

# path to the image or video
imagename=input("Enter image path:")

# read the image data using PIL
image=Image.open(imagename)

# extract EXIF data
exifdata=image.getexif()

# in exifdata , all fields are id's not a human readable form
#  iterate over all EXIF data fields

# print(exifdata)
for tag_id in exifdata:
    # get tag name, instead of human unreadavle tag id
    tag=TAGS.get(tag_id,tag_id)
    data=exifdata.get(tag_id)
    # decode bytes
    if isinstance(data,bytes):
        data=data.decode()
        print(f"{tag:25}:{data}")
    