import argparse
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from src import constants
from src import run


parser = argparse.ArgumentParser()
parser.add_argument(
    "-w",
    "--window-size",
    metavar=("<width>", "<height>"),
    nargs=2,
    type=int,
    help="Specify the window width and height in pixels.",
    default=constants.DEEFAULT_WINDOW_SIZE
)
args = parser.parse_args()
run.run(args.window_size)
