# Auto Eclipse Collage Creator

## Installation

1. Download the latest release from the [release tab](https://github.com/Gobidev/auto-eclipse-collage/releases).
2. Unpack the zip file.
3. Open the directory.
4. Start the application.

## How To Use

To use the creator, begin with copying your image files (jpg) in the same directory where the .exe is located. Also make sure all your images are numbered, _i.e. image_001.jpg_.

If there is another or no connection between the image name and the number, you can leave it as it is.
Continue by launching the .exe file of the program. It shoud look like this:


![alt text](https://raw.githubusercontent.com/Gobidev/auto-eclipse-collage/master/screenshots/gui.PNG)

Inputs are following:

**Index** is the naming scheme of the images. In this example it is *image_*. If you have another connection between the name and the number of the images, you can change that here.

**First Image Number** is the number, with that the photo-series starts. In this example it is *1*

**Last Image Number** is the number, with that the photo-series ends.

**Grid Width** changes the grid width of the output image.

**Grid Height** changes the grid height of the output image.

**Downscaling** -> When activated, downscales the images before combining them. Activate if you have little RAM or you are creating a huge collage


After filling everything in, press start. The output file will be created in the same directory together with an info.txt file including the used images.
