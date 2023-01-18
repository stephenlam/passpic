# From http://ch.china-embassy.gov.cn/ger/ls_fw_s_1/tz/201612/P020210712480189814253.jpg
# The paper photo should be 33 mm (width) x 48 mm (height).
CROP_W_MM = 33
CROP_H_MM = 48

# The head height should be 28 - 33 mm.
MIN_HEAD_HEIGHT_MM = 28
MAX_HEAD_HEIGHT_MM = 33

# The head width should be 15 - 22 mm.
MIN_HEAD_WIDTH_MM = 15
MAX_HEAD_WIDTH_MM = 22

# Eye level instructions are only provided for digital photos, but extrapolating
# to paper photos: the center of the eye should be >= 256 pixels from the bottom
# of the image. The minimum image height is 472 pixels.
MAX_EYE_LEVEL_TO_CROP_RATIO = 1 - 256 / 472

# Distance from top edge of photo to the top of the head should be 3 - 5 mm.
MIN_TOP_MARGIN_MM = 3
IDEAL_TOP_MARGIN_MM = 4
MAX_TOP_MARGIN_MM = 5

# Distance from bottom edge of photo to the bottom of the head should >= 7 mm.
MIN_BOTTOM_MARGIN_MM = 7

def create_visa_4_6_cmd(ann, outfile):
    l_bound = max(MIN_HEAD_HEIGHT_MM, MIN_HEAD_WIDTH_MM / ann.aspect_ratio)
    u_bound = min(MAX_HEAD_HEIGHT_MM, MAX_HEAD_WIDTH_MM / ann.aspect_ratio)
    print("bounds: {} {}".format(l_bound, u_bound))
    head_height_mm = (l_bound + u_bound) / 2
    head_width_mm = head_height_mm * ann.aspect_ratio
    print("Head height (mm): {}".format(head_height_mm))
    print("Head width (mm): {}".format(head_width_mm))

    crop_w_px = CROP_W_MM / head_width_mm * ann.w
    crop_h_px = CROP_H_MM / head_height_mm * ann.h

    shift_y = ann.y - crop_h_px * IDEAL_TOP_MARGIN_MM // CROP_H_MM
    shift_x = ann.x - (crop_w_px - ann.w) // 2

    pixels_per_cm = ann.h * 10 / head_height_mm
    extent_w_px = 5.08 * pixels_per_cm
    extent_h_px = 10.16 * pixels_per_cm

    validate_eye_level(ann, shift_y, crop_h_px)
    validate_bottom_margin(ann, shift_y, crop_h_px, head_height_mm)

    cmd = [
        "magick",
        ann.filename,

        "-crop", f"{crop_w_px}x{crop_h_px}+{shift_x}+{shift_y}",

        "-gravity", "center",
        "-background", "white",
        "-extent", f"{extent_w_px}x{extent_h_px}",

        "-duplicate", "2",
        "+append",

        "-quality", "100",
        "-units", "PixelsPerCentimeter",
        "-density", str(pixels_per_cm),

        outfile
    ]
    return cmd


def get_crop_dimensions(ann):
    return [calc_width, calc_height]


def validate_eye_level(ann, shift_y, crop_h_px):
    ratio = (ann.eye_y - shift_y) / crop_h_px
    print(f"Eye Level is at {ratio}.")
    if ratio > MAX_EYE_LEVEL_TO_CROP_RATIO:
        raise RuntimeError("Invalid eye level")


def validate_bottom_margin(ann, shift_y, crop_h_px, head_height_mm):
    bottom_margin_px = shift_y + crop_h_px - ann.y2
    pixels_per_mm = ann.h / head_height_mm
    bottom_margin_mm = bottom_margin_px / pixels_per_mm
    print(f"Bottom margin is {bottom_margin_mm} millimeters ({bottom_margin_px} pixels).")
    if bottom_margin_mm < MIN_BOTTOM_MARGIN_MM:
        raise RuntimeError("Invalid bottom margin")
