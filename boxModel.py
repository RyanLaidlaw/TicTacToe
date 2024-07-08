class Box:
    def __init__(self):
        self.content = None 

    def fill_with_x(self):
        if self.content is not None:
            raise ValueError("Box is already filled.")
        self.content = 'X'
        return True

    def fill_with_o(self):
        if self.content is not None:
            raise ValueError("Box is already filled.")
        self.content = 'O'
        return True

    def is_filled(self):
        return self.content is not None

    def get_content(self):
        return self.content
