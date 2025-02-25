class Color:
    def __init__(self, json_filename):
        self.json_filename = json_filename

    def __str__(self):
        return self.json_filename


green = Color('green.json')
gray = Color('gray.json')
red = Color('red.json')
