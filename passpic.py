from pathlib import Path
import sys
import subprocess

import annotation
import passport_usa

def get_annotation():
    infile = Path(sys.argv[1])
    x1 = int(sys.argv[2])
    y1 = int(sys.argv[3])
    x2 = int(sys.argv[4])
    y2 = int(sys.argv[5])
    eye_y = int(sys.argv[6])

    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)

    ann = annotation.Annotation(infile, x, y, w, h, eye_y)
    return ann


def main():
    if len(sys.argv) < 7:
        print("""Usage:
    python3 passpic.py infile x1 y1 x2 y2 eye_y

Arguments:
    infile: path to image to be processed
    x1: x-coordinate of top-left corner of head
    y1: y-coordinate of top-left corner of head
    x2: x-coordinate of bottom-right corner of head
    y2: y-coordinate of bottom-right corner of head
    eye_y: y-coordinate of eye center (eye level)
""")
        sys.exit(1)

    outdir = Path("out")
    outdir.mkdir(parents=True, exist_ok=True)

    ann = get_annotation()

    stem = ann.filename.stem
    outfile = outdir / f"passport4x6_{stem}_extent.png"
    cmdlog = outdir / f"passport4x6_{stem}_extent.log"
    cmd = passport_usa.create_passport_4_6_cmd(ann, outfile)
    str_cmd = ' '.join([str(t) for t in cmd])

    with open(cmdlog, "w", encoding="utf-8") as f:
        f.write(f"python3 {' '.join(sys.argv)}\n")
        f.write(f"{ann}\n")
        f.write(f"{str_cmd}\n")

    print(f"Running imagemagick command: \n{str_cmd}")
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
