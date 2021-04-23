# Augmented Reality Rugs

This project converts 2D images of rugs (e.g. jpegs) into 3D models that can be viewed in Augmented Reality from mobile devices (Android, iOS):

![augmented_reality_rug](https://user-images.githubusercontent.com/46463924/115776391-59257580-a3b4-11eb-904e-6108c44c9858.png)

## Live demo

See the [live demo here](https://quarup.github.io/rugs/).

![live_demo](https://user-images.githubusercontent.com/46463924/115842995-ac341280-a41e-11eb-9418-6eed882ae4c0.png)

Click on the bottom-right icon to see the rug in augmented reality. This requires a mobile device (Android or iOS). If you're on your desktop, you won't see this icon, but you should still see the 3D model.

## Installation

### Python libraries

*   Download & install the [latest Python release](https://www.python.org/downloads/)
    *    On MacOS, here's how to set it as the [default Python version](https://dev.to/malwarebo/how-to-set-python3-as-a-default-python-version-on-mac-4jjf)
*   Install or update libraries:
    ```
    python -m pip install --upgrade pip  # Upgrade PIP installer.
    python -m pip install pygltflib      # Install library for writing GLTF (GL Transmission Format) model files.
    python -m pip install numpy          # Install numpy mathematics library.
    python -m pip install Pillow         # Install Pillow for reading and writing images.
    ```
### Install Universal Scene Description (USD)

USD is the Pixar format for 3D animated models, which is required for using Augmented Reality on iOS (iPhone, iPad) devices.

On *MacOS*, the easiest solution is to install the [pre-built *0.62* version of USDPython](https://developer.apple.com/download/more/?=USDPython). As of April 2021, later versions [have a bug](https://stackoverflow.com/questions/60116329/how-can-i-solve-usdzconvert-pxr-import-error), so make sure to download `version 0.62`.

If you don't have a Mac, you'll either have to look for pre-built binaries for your OS, or you'll need to [build USD from scratch](https://github.com/PixarAnimationStudios/USD). I struggled to build USD on my MacOS, though. Let me know if you have better luck. When building from scratch, you'll get some extra tools (e.g. USD Viewer, Python library support).

### Clone this repository

Follow [these instructions](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) to clone this repository `https://github.com/quarup/augmented-reality-rugs`

## Prepare images

`prepare_images.py` converts 2D images of rugs (jpg, although other formats could be easily supported) to be used in the 3D models. The conversion does a couple of important things:

1.   Replaces the background color with transparent. This is necessary as rugs aren't exactly rectangular and occupy 100% of the image, and we do not want to display the background color when we show the rug in augmented reality. This is particularly important for rugs that have non-rectangular shapes.
2.   Shrinks the image so it is no bigger than 4.2 megapixels. This allows mobile phones (especially older ones) to display the 3D model in augmented reality. Failure to limit the image size sometimes causes problems (e.g. the phone may not display the rug at all).
     >  I chose 4.2 megapixels somewhat arbitrarily (a large square image would be resized to 2048 * 2048, which seemed like a reasonably high resolution to me). However, there may be a more scientific way to choose the maximum size, especially if someone can find the specs of what phones can handle.

Run the following command to prepare the images in the examples directory. It will read from the JPG files, convert, and write out the output as PNG files in the same directory:

```
python generator/prepare_images.py \
--images "examples/images/*.jpg"
```

> The converted images are stored in `png` format primarily because `jpg` does not natively support an alpha (transparency) channel. Unfortunately, `png` compression seems to be significantly worse for big images, so the resulting files are bigger, and therefore take longer to transfer to the user's devices. It may be worth trying to figure out a way to serve smaller files.
> 
> On the other hand, the mobile device likely needs to decompress the image to its full size to be displayed on the screen. Therefore we will always want to keep a maximum number of pixels per image regardless of how well we can compress it.

## Generate GL Transmission Format (GLTF) models

Mobile devices use the GLTF models for previewing and (in the case of Android) in Augmented Reality mode.

Run the following comment to generate GLTF models in the examples directory:

```
python geneator/generate_gltf.py \
--input_csv=examples/examples.csv \
--input_images=examples/images \
--output_models=examples/models
```

Explanation of each parameter:

*   `--input_csv` should point to a CSV file containing one row per rug, with columns:
    *    `ID` matching the name of the rug's image file.
    *    `L cm` matching the length (height) of the rug in centimeters.
    *    `W cm` matching the width of the rug in centimeters.
*   `--input_images` is the directory used in the previous step
*   `--outputmodels` will contain, per rug
    *    the `.png` file copied from `--input_images`
    *    the `.gltf` model containing the rug's shape and texture, referring back to the `.png` file

## Generate Universal Scene Description (USD) models

Next, we generate the USD models, which are necessary for the augmented reality on iOS:

```
for file in examples/models/*.gl*
do
  usdzconvert "$file"
done
```

This outputs a `.usdz` file per `.gltf` file on the same directory.

## Generate HTML

Next, we use the [\<model-viewer\> HTML tag](https://modelviewer.dev/) to display the 3D models in HTML.

For convenience, run this command to automatically generate HTML for the models in the examples directory:

```
python /Users/laure/Documents/quarup/GitHub/quarup.github.io/rugs/generator/create_html.py \
--input_models=examples/models \
--output_html=examples/models/index.html
```

>   The generated HTML is pretty bare bones. You later probably want to change certain features -- for example, you can [replace the AR button](https://modelviewer.dev/docs/#augmentedreality-slots) or [toggle the Augmented Reality mode from Javascript](https://modelviewer.dev/docs/#entrydocs-augmentedreality-methods-activateAR). Also be sure to check out the [AR examples page](https://modelviewer.dev/examples/augmentedreality/).

## Serve HTML

### Locally

To see your website, you can spin up a local web server using Python:

```
cd examples/models
python -m http.server
```

Then open your browser to http://localhost:8000/index.html. The caveat is that desktop browsers can load the 3D model, but don't support augmented reality. So this local server allows you to check that the models are loading fine, but to load augmented reality, you will either

1.   need to load the website from a mobile device, which would likely require you to set up the desktop to users browsing from the network, and then browse from the phone using your desktop's local IP instead of `localhost`, or
2.   serve the HTML on a proper internet server (see options below)

Please update this document, or let me know the steps to get #1 to work (i.e. load the web page on a mobile device by using a local server). This would be a nice speed up in development.

### On your own web server on the internet

If you already have an internet server set up, then you can just upload the `examples/models` directory and load it up on your server. Then you can test your HTML from any device connected to the internet.

### On a GitHub Page

[GitHub Pages](https://pages.github.com/) is a free service for web serving. This is what I'm using for the [live demo](https://quarup.github.io/rugs/). Once you set it up, upload the `examples/models` directory browse to it from any internet connected device.

The disadvantage of GitHub Pages is that they can take a while to pick up your changes (sometimes 10+ minutes). So it can be a bit annoying when you're making a lot of changes quickly and want to see the results right away.

## Inspiration and history

I've developed this as a feature in https://www.teppichportal.ch/. Hopefully you'll see it live there soon.

## Contributions and contact

Feel free to use this code as you wish. If possible, please update this code as you make improvements, and/or contact me for whatever reason.

Thanks!
