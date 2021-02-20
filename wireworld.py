import argparse
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import simulation


parser = argparse.ArgumentParser()
parser.add_argument(
    "-w",
    "--window-size",
    metavar=("<width>", "<height>"),
    nargs=2,
    type=int,
    help="Specify the window width and height in pixels.",
    default=(1001, 801)  # +1 so that the rightmost and bottommost grid lines are visible
)
parser.add_argument(
    "-c",
    "--cell-width",
    metavar="<width>",
    type=int,
    help="Specify the cell width in pixels.",
    default=20
)
args = parser.parse_args()

simulation.Wireworld(args.window_size, args.cell_width).run()
