from pathlib import Path

class Annotation:
    # Coordinate system has (0, 0) at top-left corner of image.
    def __init__(self, filename, x1, y1, x2, y2, eye_y):
        self.filename = filename
        self.x1 = x1  # x-coord of top-left corner of head
        self.y1 = y1  # y-coord of top-left corner of head
        self.x2 = x2  # x-coord of bottom-right corner of head
        self.y2 = y2  # y-coord of bottom-right corner of head
        self.eye_y = eye_y  # y-coord of eye center (eye level)
        self.x = min(x1, x2)
        self.y = min(y1, y2)
        self.w = abs(x2 - x1)
        self.h = abs(y2 - y1)

    def __repr__(self):
        return f"Annotation(filename={self.filename}, " \
               f"x1={self.x1}, y1={self.y1}, " \
               f"x2={self.x2}, y2={self.y2}, " \
               f"eye_y={self.eye_y})"

def load(filename):
    path = Path(filename)
    anno_path = path.with_suffix(".txt")
    with open(anno_path, 'r') as f:
        values = [int(v) for v in f.read().strip().split()]
        return Annotation(path, *values)
