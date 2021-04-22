# Augmented Reality Rugs

This project converts 2D images of rugs (e.g. jpegs) into 3D models that can be viewed in Augmented Reality from mobile devices (Android, iOS):

![augmented_reality_rug](https://user-images.githubusercontent.com/46463924/115776391-59257580-a3b4-11eb-904e-6108c44c9858.png)

## Live demo

See the [live demo here](https://quarup.github.io/rugs/).

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

## Generate GL Transmission Format (GLTF) models

### Input

*   Each rug should have a 2d image provided as a jpg (although other formats could be easily supported). The files should be named `ID.jpg` where `ID` must match an entry in the CSV file below.
*   a CSV file contains one row per rug, with columns:
    *    `ID` matching the name of the jpg file.
    *    `L cm` matching the length (height) of the rug in centimeters.
    *    `W cm` matching the width of the rug in centimeters.

## Generate Universal Scene Description (USD) models

## Generate HTML

## Serve HTML

