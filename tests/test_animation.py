from scripts import animation


class Obj:
    def __init__(self):
        self.location = (0.0, 0.0, 0.0)
        self.inserted = []

    def keyframe_insert(self, data_path, frame):
        self.inserted.append((data_path, frame))


def test_apply_location_keyframes():
    obj = Obj()
    frames = [1, 5]
    locs = [(0, 0, 0), (1, 2, 3)]
    result = animation.apply_location_keyframes(obj, frames, locs)
    assert result == list(zip(frames, locs))
    assert obj.inserted == [("location", 1), ("location", 5)]
    assert obj.location == (1, 2, 3)
