import argparse
from os import listdir
from os.path import join


_DEFAULT_RUG_ID = 'round'

_PREAMBLE = """
<head>
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

    <script>
    function updateAr() {
        document.getElementById("ar_element").src = document.getElementById("dropDown").value + ".gltf";
        document.getElementById("ar_element").iosSrc = document.getElementById("dropDown").value + ".usdz";
    }
    </script>
</head>
<body>
    <div style="width:100%; height:100%">
        <div align="center" style="font-size: larger;">
            Rug:
            <select id="dropDown" onChange="updateAr()" style="font-size: larger;">"""

_SELECT_LINE = """
                <option value="{model_id}" {selected_str}>{model_id}</option><br />"""

_POSTAMBLE = """
            </select>
        </div>


        <model-viewer
            id="ar_element"
            src="{model_id}.gltf"
            ios-src="{model_id}.usdz"
            camera-controls
            ar-modes="scene-viewer webxr quick-look"
            ar
            ar-scale="auto"
            style="width:100%; height:100%">
        </model-viewer>
    </div>
</body>
"""

def main():
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--input_models', metavar='path', required=True,
                        help='Path to models directory')
    parser.add_argument('--output_html', metavar='path', required=True,
                        help='Path to the output HTML file')
    args = parser.parse_args()

    model_ids = [f.removesuffix('.gltf') for f in listdir(args.input_models) if join(args.input_models, f).endswith('.gltf')]
    if len(model_ids) < 1:
    	print("ERROR: could not find any GLTF files in {}".format(args.input_models))
    	return

    select_lines = [_SELECT_LINE.format(model_id=f, selected_str=('selected' if f == _DEFAULT_RUG_ID else '')) for f in model_ids]

    with open(args.output_html, "w") as file1:
        # Writing data to a file
        file1.write(_PREAMBLE)
        file1.writelines(select_lines)
        file1.write(_POSTAMBLE.format(model_id=_DEFAULT_RUG_ID))

    print("Wrote {} models to {}".format(len(model_ids), args.output_html))

if __name__ == "__main__":
    main()
