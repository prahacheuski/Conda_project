import numpy as np
import imageio
import sys
import os
import re


class ImageConverter(object):
    # General constants
    __TEXT_FILE_SEPARATOR: str = ','
    __TEXT_SHAPE_RE_PATTERN: re.compile = re.compile(r"^shape: \((?P<x>\d+), (?P<y>\d+), (?P<z>\d+)\)$")

    def __init__(self, mode: str, in_file_path: str, out_file_path: str) -> None:
        """
        Initialize class with parameters and call method '__check_args'.
        :param mode: operation mode ('from_picture' or 'from_text')
        :param in_file_path: path to input file (relative or absolute).
        :param out_file_path: path to output file (relative or absolute).
        """
        self.__mode: str = mode
        self.__in_file_path: str = in_file_path
        self.__out_file_path: str = out_file_path
        self.__check_args()

    def __check_args(self) -> None:
        """
        Check general conditions.
        :return: void.
        """
        if self.__mode not in ('from_picture', 'from_text'):
            raise ValueError("Allowed ('r', 'w') for argument 'mode', got: {}".format(self.__mode))

        if not (os.path.exists(self.__in_file_path) and os.path.isfile(self.__in_file_path)):
            raise ValueError("Any problems with given 'in_file_path'. It is not exist or is not a file: {}"
                             "".format(self.__in_file_path))

    def convert(self) -> None:
        """
        Convert picture to digits and vice versa.
        :return: void.
        """
        if self.__mode == 'from_picture':
            # Read image into matrix
            im: imageio.core.util.Array = imageio.imread(self.__in_file_path)

            with open(self.__out_file_path, 'wt') as out_f:
                # Write 'shape' declaration
                out_f.write(f"shape: {im.shape}\n")
                # Write digits
                im.tofile(out_f, sep=ImageConverter.__TEXT_FILE_SEPARATOR)

        else:  # from_text mode
            with open(self.__in_file_path, 'rt') as in_f:
                # Search line (e.g. shape: (466, 640, 3)) using regular expression
                search_res = ImageConverter.__TEXT_SHAPE_RE_PATTERN.search(in_f.readline())

                if not search_res:
                    raise ValueError("Didn't find 'shape' declaration in input file: {}".format(self.__in_file_path))

                res_dict = search_res.groupdict()

                # Read digits from file amd convert to matrix view
                im_mat = np.fromfile(in_f, dtype=np.uint8, sep=ImageConverter.__TEXT_FILE_SEPARATOR)
                im_mat = im_mat.reshape(int(res_dict['x']), int(res_dict['y']), int(res_dict['z']))

                # Writing image to the disk
                imageio.imwrite(self.__out_file_path, im_mat)


if __name__ == '__main__':
    # To view help run the application from command prompt without arguments (e.g. "python3.7 -m image_converter")
    if len(sys.argv) != 4:
        print(f"{'=' * 20} Image Converter {'=' * 20}\n"
              f"Accept following positional argument: image_converter.py [uri] [mode] [input file path] "
              f"[output file path]\nGot: {'Nothing' if not sys.argv[1:4] else sys.argv[1:]}\n{'-' * 30}\n"
              f"Run from command prompt examples:\npython3.7 -m image_converter from_picture ~/Downloads/"
              f"test_image.jpg ~/Downloads/image_matrix.txt\npython3.7 -m image_converter from_text "
              f"~/Downloads/image_matrix.txt ~/Downloads/new_image.jpg")

    else:
        _, __mode, __in_file_path, __out_file_path = sys.argv

        ic: ImageConverter = ImageConverter(__mode, __in_file_path, __out_file_path)

        print('Converting file...')
        ic.convert()
        print('The file has been converted successfully.')
