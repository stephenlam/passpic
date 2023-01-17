import sys
import subprocess
from pathlib import Path

import us_passport

class Annotation:
    # coord system has (0, 0) at top-left corner of image
    # and (W-1, H-1) at bottom-right corner, where W is the
    # image width in pixels and H is the image height in pixels.
    def __init__(self, filename, x, y, w, h, eye_y,
                 image_width=3024,
                 image_height=4032,
                 ):
        self.filename = filename
        self.x = x  # x-coord of top corner of head
        self.y = y  # y-coord of top corner of head
        self.w = w  # width of head in pixels
        self.h = h  # height of head in pixels
        self.eye_y = eye_y  # y-coord of eye center (eye level)
        self.img_w = image_width
        self.img_h = image_height

def get_annotation():
    if len(sys.argv) > 1:
        infile = Path(sys.argv[1])
        x1 = int(sys.argv[2])
        y1 = int(sys.argv[3])
        x2 = int(sys.argv[4])
        y2 = int(sys.argv[5])
        eye_y = int(sys.argv[6])
	# infile = Path(sys.argv[1])
	# head_h = int(sys.argv[2])
	# eye_y = int(sys.argv[3])
	# head_x1 = int(sys.argv[4])
	# head_x2 = int(sys.argv[5])
    # else:
    # 	print("Head height (pixels): ", end="")
    # 	head_h = int(input())
    # 	print("Top edge to eye level (pixels): ", end="")
    # 	eye_y = int(input())
    # 	print("Left edge to side of head (pixels): ", end="")
    # 	head_x1 = int(input())
    # 	print("Left edge to other side of head (pixels): ", end="")
    # 	head_x2 = int(input())
    # 	print("Image width (default 3024): ", end="")
    # 	img_w = input()
    # 	if len(img_w.strip()) > 0:
    # 		img_w = int(input())
    # 	else:
    # 		img_w = 3024
    # 	print("Image height (default 4032): ", end="")
    # 	img_h = input()
    # 	if len(img_h.strip()) > 0:
    # 		img_h = int(input())
    # 	else:
    # 		img_h = 4032

    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)

    ann = Annotation(infile, x, y, w, h, eye_y)
    return ann


def main():
    outdir = Path("out")
    outdir.mkdir(parents=True, exist_ok=True)

    ann = get_annotation()

    stem = ann.filename.stem
    outfile = outdir / f"passport4x6_{stem}.png"
    cmdlog = outdir / f"passport4x6_{stem}.log"
    cmd = us_passport.create_passport_4_6_cmd(
        ann, ann.filename, outfile
    )
    subprocess.run(cmd)
    print(cmd)
    with open(cmdlog, "w", encoding="utf-8") as f:
        # f.write(f"{infile} {head_h} {eye_y} {head_x1} {head_x2}\n")
        f.write(str(cmd))
        f.write("\n")

# # generate cropped file
# crop_cmd = [
#   "convert",
#   "-crop", f"{crop}x{crop}+{shift_x}+{shift_y}",
#   "-quality", "100",
#   infile,
#   tmpfile
# ]
# subprocess.run(crop_cmd)

# # create montage for printing
# montage_cmd = [
#   "montage",
#   "-quality", "100",
#   "-units", "PixelsPerInch",
#   "-density", "300",
#   "-geometry", "600x600+150+350",
#   tmpfile, tmpfile,
#   outfile
# ]
# subprocess.run(montage_cmd)

# delete the temp working file
# tmpfile.unlink()

# with open(cmdlog, "w", encoding="utf-8") as f:
# 	f.write(f"{infile} {head_h} {eye_y} {head_x1} {head_x2}\n")
# 	f.write(str(crop_cmd))
# 	f.write("\n")
# 	f.write(str(montage_cmd))
# 	f.write("\n")
	


# chinese passport
# 396px wide by 576px tall at 120 dots per centimeter

# min_head_h_prc = 28/48
# max_head_h_prc = 33/48
# crop_h = int(head_h / .5935)
# crop_w = int(head
# shift_y = eye_y - int(.375 * crop)
# shift_x = head_x1 - int((crop - head_w) / 2)


main()
