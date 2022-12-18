import re


class InputHandler:
    def check_color(self, rgba: str):
        # Check to ensure color is of correct form
        regex = r"(\d+),\s*(\d+),\s*(\d+),\s*(((\d*)?\.\d*)|1|0)"
        keys = ["r", "g", "b", "a"]
        if not rgba:  # No input specified. Default to black
            return

        x = re.search(regex, rgba)

        if not x:
            raise Exception(
                f"Please format input as '(r,g,b,a) without negative values'"
            )
        else:
            x = list(x.groups())

        for i in range(3):
            try:
                x[i] = int(x[i])
            except ValueError:
                raise Exception(
                    f"{x[i]} could not be converted to an integer for {keys[i]} channel"
                )

            if x[i] > 255 or x[i] < 0:
                raise Exception(f"{x[i]} is not in a valid range for {keys[i]} channel")
        try:
            x[3] = float(x[3])
        except ValueError:
            raise Exception(
                f"{x[3]} could not be converted to an integer for {keys[3]} channel"
            )

        return x[0:4]

    def read_file(self, file_repo: str, filename: str):
        try:
            with open(file_repo + filename) as f:
                output = []
                for line in f:
                    li = line.strip().split(",")
                    res = [eval(i) for i in li]
                    output.append(res)
            num_vertices = output[0][0]
            shape_points = output[1 : num_vertices + 1]
            shape_faces = output[1 + num_vertices :]
            return shape_points, shape_faces
        except FileNotFoundError:
            raise Exception(
                f"File does not exist. Please make sure it is in object_files directory"
            )
        except IndexError:
            raise Exception(f"Input file is formatted incorrectly")
