# Augmented Reality Rugs

This project focuses on converting 2D images of rugs (e.g. jpegs) into 3D models that can be viewed in Augmented Reality from mobile devices (Android, iPhone):

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
    python -m pip install pygltflib      # Install library for writing GLTF model files.
    python -m pip install numpy          # Install numpy mathematics library.
    ```

### Input

*   Each rug should have a 2d image provided as a jpg (although other formats could be easily supported). The files should be named `ID.jpg` where `ID` must match an entry in the CSV file below.
*   a CSV file contains one row per rug, with columns:
    *    `ID` matching the name of the jpg file.
    *    `L cm` matching the length (height) of the rug in centimeters.
    *    `W cm` matching the width of the rug in centimeters.
