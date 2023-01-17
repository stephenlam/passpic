class Annotation:
    # Coordinate system has (0, 0) at top-left corner of image.
    def __init__(self, filename, x, y, w, h, eye_y):
        self.filename = filename
        self.x = x  # x-coord of top corner of head
        self.y = y  # y-coord of top corner of head
        self.w = w  # width of head in pixels
        self.h = h  # height of head in pixels
        self.eye_y = eye_y  # y-coord of eye center (eye level)

    def __repr__(self):
        return f"Annotation(filename={self.filename}, " \
               f"x={self.x}, y={self.y}, " \
               f"w={self.w}, h={self.h}, " \
               f"eye_y={self.eye_y}"
