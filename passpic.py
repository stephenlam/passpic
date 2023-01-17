from pathlib import Path
import sys
import subprocess

import annotation
import passport_usa

def main():
    if len(sys.argv) < 2:
        print("""Usage:
    python3 passpic.py infile

Arguments:
    infile: path to image to be processed
""")
        sys.exit(1)

    outdir = Path("out")
    outdir.mkdir(parents=True, exist_ok=True)

    ann = annotation.load(sys.argv[1])

    stem = ann.filename.stem
    outfile = outdir / f"passport4x6_{stem}.png"
    cmdlog = outdir / f"passport4x6_{stem}.log"
    cmd = passport_usa.create_passport_4_6_cmd(ann, outfile)
    str_cmd = ' '.join([str(t) for t in cmd])

    print(f"Running command: \n{str_cmd}")
    subprocess.run(cmd)

    with open(cmdlog, "w", encoding="utf-8") as f:
        f.write(f"{ann}\n")
        f.write(f"{str_cmd}\n")


if __name__ == "__main__":
    main()
