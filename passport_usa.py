# From https://do.usembassy.gov/u-s-citizen-services/passports/photo-requirements-u-s-passports-visa/

# The photograph should measure 2″ square (roughly 50 mm square) with the
# head centered in the frame.
CROP_IN = 2

# The head (measured from the top of the hair to the bottom of the chin)
# should measure between 1 to 1 3/8″ (25 to 35 mm).
MIN_HEAD_HEIGHT_IN = 1
MAX_HEAD_HEIGHT_IN = 1 + 3/8
HEAD_HEIGHT_IN = (MIN_HEAD_HEIGHT_IN + MAX_HEAD_HEIGHT_IN) / 2
HEAD_TO_CROP_RATIO = HEAD_HEIGHT_IN / CROP_IN

# ...with the eye level between 1 1/8 to 1 3/8″ (28 and 35 mm) from the bottom
# of the photo.
MIN_EYE_LEVEL_IN = CROP_IN - (1 + 3/8) # from top edge
MAX_EYE_LEVEL_IN = CROP_IN - (1 + 1/8) # from top edge
EYE_LEVEL_IN = (MIN_EYE_LEVEL_IN + MAX_EYE_LEVEL_IN) / 2
EYE_LEVEL_TO_CROP_RATIO = EYE_LEVEL_IN / CROP_IN

def create_passport_4_6_cmd(ann, outfile):
    crop = int(ann.h / HEAD_TO_CROP_RATIO)

    # ensure crop pixel width is divisible by 2
    if crop % 2 != 0:
        crop -= 1

    shift_y = ann.eye_y - int(EYE_LEVEL_TO_CROP_RATIO * crop)
    shift_x = ann.x - (crop - ann.w) // 2

    density = crop // 2
    extent_w_px = 3 * density
    extent_h_px = 4 * density

    cmd = [
        "magick",
        ann.filename,

        "-crop", f"{crop}x{crop}+{shift_x}+{shift_y}",

        "-gravity", "center",
        "-background", "white",
        "-extent", f"{extent_w_px}x{extent_h_px}",

        "+duplicate",
        "+append",

        "-quality", "100",
        "-units", "PixelsPerInch",
        "-density", str(density),

        outfile
    ]
    return cmd

