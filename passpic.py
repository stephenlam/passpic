from pathlib import Path
import sys
import subprocess

import annotation
import passport_usa
import visa_china

def main():
    if len(sys.argv) < 2:
        print("""Usage:
    python3 passpic.py infile

Arguments:
    infile: path to image to be processed

For each image, passpic requires a corresponding annotation file
with these five parameters:
    x1: x-coordinate of top-left corner of head
    y1: y-coordinate of top-left corner of head
    x2: x-coordinate of bottom-right corner of head
    y2: y-coordinate of bottom-right corner of head
    eye_y: y-coordinate of eye center (eye level)

The parameters should be integers separated by single spaces on a single line.

Example:
1024 1260 1424 1860 1585

The annotation file should be located in the same directory as the image file,
with a suffix .txt. For instance, the annotation file for john.jpg should be
john.txt.""")
        sys.exit(1)

    outdir = Path("out")
    outdir.mkdir(parents=True, exist_ok=True)

    ann = annotation.load(sys.argv[1])

    print("Creating US passport photo.")
    stem = ann.filename.stem
    outfile = outdir / f"passport4x6_{stem}.png"
    cmdlog = outdir / f"passport4x6_{stem}.log"
    cmd = passport_usa.create_passport_4_6_cmd(ann, outfile)
    str_cmd = ' '.join([str(t) for t in cmd])

    print(f"Running command: \n{str_cmd}")
    subprocess.run(cmd)

    print()
    print("Creating Chinese visa photo.")
    with open(cmdlog, "w", encoding="utf-8") as f:
        f.write(f"{ann}\n")
        f.write(f"{str_cmd}\n")

    outfile = outdir / f"visa4x6_{stem}.png"
    cmdlog = outdir / f"visa4x6_{stem}.log"
    cmd = visa_china.create_visa_4_6_cmd(ann, outfile)
    str_cmd = ' '.join([str(t) for t in cmd])

    print(f"Running command: \n{str_cmd}")
    subprocess.run(cmd)

    with open(cmdlog, "w", encoding="utf-8") as f:
        f.write(f"{ann}\n")
        f.write(f"{str_cmd}\n")


if __name__ == "__main__":
    main()
