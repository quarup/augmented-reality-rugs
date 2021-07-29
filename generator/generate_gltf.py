import numpy as np
import pygltflib
from pygltflib import GLTF2, BufferFormat
from pygltflib.utils import ImageFormat, Image, Texture
from pygltflib.validator import validate, summary
import argparse
import csv
import os
import shutil


def getRealRugId(id: str, input_images: str, skip_models_in_directory: str, model_suffix: str):
    """Gets rug ID, filling in missing zero prefix when necessary"""
    # Sometimes the CSV's ID is missing some prefixing zeros. We resolve the
    # problem here by looking for images with prefixed zeros.
    for id_prefix in ['', '0', '00', '000']:
        resolved_id = f'{id_prefix}{id}'
        # See if it exists in skip directory.
        if os.path.isfile(f"{skip_models_in_directory}/{resolved_id}.{model_suffix}"):
            return resolved_id

        # Look for png first (because it supports transparency), then fall back to jpg.
        for image_suffix in ['png', 'jpg']:
            filename = f"{input_images}/{resolved_id}.{image_suffix}"
            if os.path.isfile(filename):
                return resolved_id
    # Default to original ID passedi n.
    return id

class RugImage:
    """Rug Image."""
    def __init__(self, id: str, input_images: str):
        self.id = id
        self.original_filename = None
        # Look for png first (because it supports transparency), then fall back to jpg.
        for image_suffix in ['png', 'jpg']:
            filename = f"{input_images}/{id}.{image_suffix}"
            if os.path.isfile(filename):
                self.original_filename = filename
                break

    def getId(self):
        return self.id

    def getOriginalFilename(self):
        return self.original_filename

    def getLocalFilename(self):
        original_filename = self.getOriginalFilename()
        return os.path.basename(original_filename) if original_filename else None

    def getRelativeFilename(self):
        return os.path.relpath(self.getOriginalFilename())

    def getOutputFilename(self, store_image_in_blob):
        return self.getRelativeFilename() if store_image_in_blob else self.getLocalFilename()

class Rug:
    """Rug data."""
    def __init__(self, image: RugImage, length_m: float, width_m: float):
        self.image = image
        self.points = np.array(
            [
                [+width_m / 2, 0, +length_m / 2],
                [+width_m / 2, 0, -length_m / 2],
                [-width_m / 2, 0, -length_m / 2],
                [-width_m / 2, 0, +length_m / 2],
            ],
            dtype="float32",
        )
        self.points_blob = self.points.tobytes()
        self.texture_coords = np.array(
            [
                [1, 1],
                [1, 0],
                [0, 0],
                [0, 1],
            ],
            dtype="float32",
        )
        self.texture_coords_blob = self.texture_coords.flatten().tobytes()
        self.triangles = np.array(
            [
                [0, 1, 2],
                [2, 3, 0],
            ],
            dtype="uint8",
        )
        self.triangles_blob = self.triangles.flatten().tobytes()

    def getGLTF(self, store_image_in_blob=False):
        gltf = pygltflib.GLTF2(
            scene=0,
            scenes=[pygltflib.Scene(nodes=[0])],
            nodes=[pygltflib.Node(mesh=0)],
            meshes=[
                pygltflib.Mesh(
                    primitives=[
                        pygltflib.Primitive(
                            attributes=pygltflib.Attributes(
                                POSITION=0,
                                TEXCOORD_0=1),
                            indices=2,
                            material=0
                        )
                    ]
                )
            ],
            accessors=[
                # Points of the rug rectangle.
                pygltflib.Accessor(
                    bufferView=0,
                    componentType=pygltflib.FLOAT,
                    count=len(self.points),
                    type=pygltflib.VEC3,
                    max=self.points.max(axis=0).tolist(),
                    min=self.points.min(axis=0).tolist(),
                ),
                # Texture coordinates
                pygltflib.Accessor(
                    bufferView=1,
                    componentType=pygltflib.FLOAT,
                    count=len(self.texture_coords),
                    type=pygltflib.VEC2,
                    max=self.texture_coords.max(axis=0).tolist(),
                    min=self.texture_coords.min(axis=0).tolist(),
                ),
                # Triangle indices. We keep these at the end because unsigned bytes may not result in a length multiple of 4 bytes.
                pygltflib.Accessor(
                    bufferView=2,
                    componentType=pygltflib.UNSIGNED_BYTE,
                    count=self.triangles.size,
                    type=pygltflib.SCALAR,
                    max=[int(self.triangles.max())],
                    min=[int(self.triangles.min())],
                ),
            ],
            bufferViews=[
                # Points of the rug rectangle.
                pygltflib.BufferView(
                    buffer=0,
                    byteOffset=0,
                    byteLength=len(self.points_blob),
                    target=pygltflib.ARRAY_BUFFER,
                ),
                # Texture coordinates
                pygltflib.BufferView(
                    buffer=0,
                    byteOffset=len(self.points_blob),
                    byteLength=len(self.texture_coords_blob),
                    target=pygltflib.ARRAY_BUFFER,
                ),
                # Triangle indices. We keep these at the end because unsigned bytes may not result in a length multiple of 4 bytes.
                pygltflib.BufferView(
                    buffer=0,
                    byteOffset=len(self.points_blob) + len(self.texture_coords_blob),
                    byteLength=len(self.triangles_blob),
                    target=pygltflib.ELEMENT_ARRAY_BUFFER,
                ),
            ],
            buffers=[
                pygltflib.Buffer(
                    byteLength=len(self.points_blob) + len(self.texture_coords_blob) + len(self.triangles_blob)
                )
            ],
            images=[pygltflib.Image(uri=self.image.getOutputFilename(store_image_in_blob))],
            textures=[pygltflib.Texture(source=0)],
            materials=[pygltflib.Material(
                pbrMetallicRoughness=pygltflib.PbrMetallicRoughness(
                    metallicFactor=0,
                    roughnessFactor=0.9,
                    baseColorTexture=pygltflib.TextureInfo(index=0),
                  ),
                  alphaMode=pygltflib.MASK,
                  alphaCutoff=0.1,
                  doubleSided=True,
            )]
        )

        if store_image_in_blob:
            gltf.convert_images(ImageFormat.DATAURI)

        gltf.set_binary_blob(self.points_blob + self.texture_coords_blob + self.triangles_blob)
        gltf.convert_buffers(BufferFormat.DATAURI)  # convert buffer URIs to data.

        return gltf


class Generator:
    def __init__(self, args):
        self.args = args

    def generate(self):
        suffix = 'glb' if self.args.save_as_glb else 'gltf'
        with open(self.args.input_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            num_written = 0
            for row in reader:
                rug_id = getRealRugId(row['ID'], self.args.input_images,
                                      self.args.skip_models_in_directory, suffix)
                image = RugImage(rug_id, self.args.input_images)
                model_filename = f"{rug_id}.{suffix}"
                if self.args.skip_models_in_directory:
                    skip_filename = os.path.join(self.args.skip_models_in_directory, model_filename)
                    if os.path.isfile(skip_filename):
                        print(f'Skipping {model_filename} because it already exists in {skip_filename}')
                        continue
                output_model_file = os.path.join(self.args.output_models, model_filename)
                rug = Rug(image, float(row['L cm']) / 100, float(row['W cm']) / 100)
                if rug.image.getOriginalFilename() is not None:
                    gltf = rug.getGLTF(store_image_in_blob=self.args.save_as_glb)
                    num_written += 1
                    if not self.args.save_as_glb:
                        print(f"[{num_written}] Writing {output_model_file}")
                        gltf.save(output_model_file)
                        image_file = os.path.join(self.args.output_models, rug.image.getLocalFilename())
                        print(f"[{num_written}] Copying {image_file}")
                        shutil.copyfile(
                            rug.image.getOriginalFilename(),
                            image_file)
                    else:
                        gltf.convert_buffers(BufferFormat.BINARYBLOB)
                        print(f"[{num_written}] Writing {output_model_file}")
                        gltf.save_binary(output_model_file)
                else:
                    print(f"WARNING: Skipping rug without image file. Rug ID={rug_id}")
            print("\nSuccess!\n")

def main():
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--input_csv', metavar='path', required=True,
                        help='Path to input CSV file')
    parser.add_argument('--input_images', metavar='path', required=True,
                        help='Path to input images directory')
    parser.add_argument('--output_models', metavar='path', required=True,
                        help='Path to output models directory')
    parser.add_argument('--skip_models_in_directory', metavar='path', default='',
                        help='If provided, skips building models that already exist in this directory.')
    parser.add_argument('--save_as_glb', metavar='path', default='true',
                        help='Whether to save as a binary blob')
    Generator(parser.parse_args()).generate()



if __name__ == "__main__":
    main()
