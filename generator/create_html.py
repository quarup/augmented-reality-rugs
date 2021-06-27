import argparse
from os import listdir
from os.path import join


_DEFAULT_RUG_ID = 'round'

_PREAMBLE = """
<head>
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

    <script>
    function updateAr() {
        document.getElementById("ar_element").src = document.getElementById("dropDown").value + ".glb";
        document.getElementById("ar_element").iosSrc = document.getElementById("dropDown").value + ".usdz";
    }
    </script>
    <style>
      /* This keeps child nodes hidden while the element loads */
      :not(:defined) > * {
        display: none;
      }

      model-viewer {
        background-color: #eee;
        overflow-x: hidden;
        --poster-color: #eee;
      }

      #ar-button {
        background-image: url(ic_view_in_ar_new_googblue_48dp.png);
        background-repeat: no-repeat;
        background-size: 50px 50px;
        background-position: 20px 50%;
        background-color: #fff;
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        bottom: 132px;
        padding: 0px 30px 0px 80px;
        font-family: Roboto Regular, Helvetica Neue, sans-serif;
        font-size: 50px;
        height: 80px;
        line-height: 36px;
        border-radius: 18px;
        border: 1px solid #DADCE0;
        color:#4285f4;
      }

      #ar-unsupported {
        color:#aa0000;
        font-size: 14px;
        display: none;
      }
    </style>
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
                src="{model_id}.glb"
                ios-src="{model_id}.usdz"
                camera-controls
                ar-modes="scene-viewer webxr quick-look"
                ar
                ar-scale="auto"
                style="width:100%; height:100%">
            <button slot="ar-button" id="ar-button">
                See rug in your room.
            </button>
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

    model_ids = [f.removesuffix('.glb') for f in listdir(args.input_models) if join(args.input_models, f).endswith('.glb')]
    if len(model_ids) < 1:
    	print("ERROR: could not find any GLB files in {}".format(args.input_models))
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
