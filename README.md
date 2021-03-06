# Augmented Reality Rugs

This project converts 2D images of rugs (e.g. jpegs) into 3D models that can be viewed in Augmented Reality from mobile devices (Android, iOS):

![augmented_reality_rug](https://user-images.githubusercontent.com/46463924/115776391-59257580-a3b4-11eb-904e-6108c44c9858.png)

## Live demo

### On Teppichportal

I've developed this as a feature for https://www.teppichportal.ch/. Open one of the product pages and click on the "View in your room" button on a mobile device (Android or iOS):

![Teppichportal product page](https://user-images.githubusercontent.com/46463924/145562475-1887b94c-569e-417c-9dc6-148782866dad.png)


Following the instructions, you'll see the rug:

![Teppichportal AR rug](https://user-images.githubusercontent.com/46463924/145561707-edd8314b-960f-4842-bbe2-508616f79c89.png)

### On GitHub

You can also see a [developer version of the demo](https://quarup.github.io/rugs/).

![developer version of the demo](https://user-images.githubusercontent.com/46463924/123559601-53298780-d79d-11eb-946e-c1e1cf3e3d24.png)

The Augmented Reality "See rug in your room" feature requires a mobile device (Android or iOS). If you're on your desktop, you should still be able to see the 3D model.


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
### Install a converter from GLTF to Universal Scene Description (USD)

USD is the Pixar format for 3D animated models, which is required for using Augmented Reality on iOS (iPhone, iPad) devices.

We have two options below on how to convert from GL Transmission Format (GLTF) models to USD.

#### Option 1 (preferred, Mac-only): Install Reality Converter

In the page for Apple's [Augmented Reality Tools](https://developer.apple.com/augmented-reality/tools/), click on the download button for **Reality Converter**:

<a link="https://developer.apple.com/augmented-reality/tools/"><img src="https://user-images.githubusercontent.com/46463924/161235320-096aa926-3c97-42e6-8108-c19250083611.png"></a>

Then proceed to install Reality Converter.

### Option 2: USD command line tool.

Alternatively you can run the USD tool libraries, which take a bit more work, and are (at least in theory) more compatible with different systems, including non-Mac computers.

On *MacOS*, you can install the [pre-built *0.62* version of USDPython](https://developer.apple.com/download/more/?=USDPython). As of April 2021, later versions [have a bug](https://stackoverflow.com/questions/60116329/how-can-i-solve-usdzconvert-pxr-import-error), so make sure to download `version 0.62`.

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
python generator/prepare_images.py --images "examples/images/*.jpg"
```

> The converted images are stored in `png` format primarily because `jpg` does not natively support an alpha (transparency) channel. Unfortunately, `png` compression seems to be significantly worse for big images, so the resulting files are bigger, and therefore take longer to transfer to the user's devices. It may be worth trying to figure out a way to serve smaller files.
> 
> On the other hand, the mobile device likely needs to decompress the image to its full size to be displayed on the screen. Therefore we will always want to keep a maximum number of pixels per image regardless of how well we can compress it.

## Generate GL Transmission Format (GLTF) models

Mobile devices use the GLTF models for previewing and (in the case of Android) in Augmented Reality mode.

Run the following comment to generate GLTF models in the examples directory:

```
python generator/generate_gltf.py --input_csv=examples/examples.csv --input_images=examples/images --output_models=examples/models
```

Explanation of each parameter:

*   `--input_csv` should point to a CSV file containing one row per rug, with columns:
    *    `ID` matching the name of the rug's image file.
    *    `L cm` matching the length (height) of the rug in centimeters.
    *    `W cm` matching the width of the rug in centimeters.
    *.   All other columns are ignored by the program.
*   `--input_images` is the directory used in the previous step
*   `--output_models` will contain, per rug
    *    the `.png` file copied from `--input_images`
    *    the `.gltf` model containing the rug's shape and texture, referring back to the `.png` file

## Generate Universal Scene Description (USD) models

Next, we generate the USD models, which are necessary for the augmented reality on iOS.

We need to convert each `.gltf` file into a corresponding `.usdz` in same directory. The next step depends on which tool you installed earlier.

### Option 1 (preferred, Mac-only): Convert to USDZ using the Reality Converter

If you installed Reality Converter (see instructions above), then launch it now and:

1. Open all the `.gltf` files you generated
2. Preview the 3D models to see what they look like
3. Export to `.usdz` files in the same directory

### Option 2: Convert to USDZ using the USD command line tool.

To run the USD command line tools, you'll need to either:

1.   Run the `USD.command` script under your USD (or USDPython) directory (see USD installation step above), or
2.   Set the corresponding python environment variables manually.

Then run the converter tool to convert your GLTF files to USD:

```
for file in examples/models/*.gl*
do
  usdzconvert "$file"
done
```

### Notes about converting to USDZ

>   The `.usdz` model is a binary file containing a copy of the `png` image. This unfortunately means that iOS users need to download the image twice: once when they first view the 3D (GLTF) model and then again when they download the USDZ file for agumented reality.
>
>   Theoretically, we should be able to overcome this by using a `.usda` text representation (which allows us to reference the `.png` file instead of copying it) instead of the binary `.usdz`. Unfortunately I wasn't able to get it to work, even after running `usdzconverter model.gltf model.usda` and tweaking the output. Please update the code or contact me if you figure this out.

## Generate HTML

Next, we use the [\<model-viewer\> HTML tag](https://modelviewer.dev/) to display the 3D models in HTML.

For convenience, run this command to automatically generate HTML for the models in the examples directory:

```
python generator/create_html.py --input_models=examples/models --output_html=examples/models/index.html
```

>   The generated HTML is pretty bare bones. You later probably want to change certain features -- for example, you can [replace the AR button](https://modelviewer.dev/docs/#augmentedreality-slots) or [toggle the Augmented Reality mode from Javascript](https://modelviewer.dev/docs/#entrydocs-augmentedreality-methods-activateAR). Also be sure to check out the [AR examples page](https://modelviewer.dev/examples/augmentedreality/).

Note that the HTML loads the \<model-viewer\> code from a seperate server:

```
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
```

When launching this on your website, you may want to copy `model-viewer.min.js` to minimize dependency on other servers.

## Serve HTML

### Within your local network

To see your website, you can spin up a local web server using Python:

```
cd examples/models
python -m http.server
```

Then open your browser to http://localhost:8000. The caveat is that desktop browsers can load the 3D model, but don't support augmented reality.

To test the augmented reality feature, you need to load the page on your phone or tablet. To do this, get the IP address of your desktop (MacOS, Windows, or Linux) by running:

```
ifconfig
```

In the output you will see an IP address of your machine within the local network, likely starting with `192.168.`. For example, on MacOS there is a line that may look like:

```
	inet 192.168.0.45 netmask 0xffffff00 broadcast 192.168.0.255
```

Then on your phone or tablet, you should be able to load the website with augmented reality. Following the same example, it would be http://192.168.0.45:8000, but you need to modify the IP to match yours.


### On your own web server on the internet

If you already have an internet server set up, then you can just upload the `examples/models` directory and load it up on your server. Then you can test your HTML from any device connected to the internet.

### On a GitHub Page

[GitHub Pages](https://pages.github.com/) is a free service for web serving. This is what I'm using for the [live demo](https://quarup.github.io/rugs/). Once you set it up, upload the `examples/models` directory browse to it from any internet connected device.

The disadvantage of GitHub Pages is that they can take a while to pick up your changes (sometimes 10+ minutes). So it can be a bit annoying when you're making a lot of changes quickly and want to see the results right away.

## Contributions and contact

Feel free to use this code as you wish. If possible, please update this code as you make improvements, and/or contact me for whatever reason.

Thanks!
