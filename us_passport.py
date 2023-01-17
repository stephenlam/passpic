DPI = 300
CROP_IN = 2
CROP_PX = DPI * CROP_IN
MIN_HEAD_HEIGHT_IN = 1
MAX_HEAD_HEIGHT_IN = 1 + 3/8
HEAD_HEIGHT_IN = (MIN_HEAD_HEIGHT_IN + MAX_HEAD_HEIGHT_IN) / 2
HEAD_TO_CROP_RATIO = HEAD_HEIGHT_IN / CROP_IN
MIN_EYE_LEVEL_IN = CROP_IN - (1 + 3/8) # from top edge
MAX_EYE_LEVEL_IN = CROP_IN - (1 + 1/8) # from top edge
EYE_LEVEL_IN = (MIN_EYE_LEVEL_IN + MAX_EYE_LEVEL_IN) / 2
EYE_LEVEL_TO_CROP_RATIO = EYE_LEVEL_IN / CROP_IN

def create_passport_4_6_cmd(ann, infile, outfile):
    crop = int(ann.h / HEAD_TO_CROP_RATIO)
    shift_y = ann.eye_y - int(EYE_LEVEL_TO_CROP_RATIO * crop)
    shift_x = ann.x - int((crop - ann.w) / 2)

    PAPER_W_PX = 6 * DPI
    PAPER_H_PX = 4 * DPI

    cmd = [
        "magick",
        infile,
        "-crop", f"{crop}x{crop}+{shift_x}+{shift_y}",
        "-resize", f"{CROP_PX}x{CROP_PX}",
        "-gravity", "center",
        "-background", "white",
        "-extent", f"{int(PAPER_W_PX / 2)}x{PAPER_H_PX}",
        "+duplicate",
        "+append",
        "-quality", "100",
        "-units", "PixelsPerInch",
        "-density", "300",
        outfile
    ]
    return cmd

