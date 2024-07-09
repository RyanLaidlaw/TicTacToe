class Box:
    """
    Represents a single box in the Tic-Tac-Toe board.

    Attributes:
        content (str): The content of the box ('X', 'O', or None).
    """
    def __init__(self):
        self.content = None 

    def fill_with_x(self) -> bool:
        if self.content is not None:
            raise ValueError("Box is already filled.")
        self.content = 'X'
        return True

    def fill_with_o(self) -> bool:
        if self.content is not None:
            raise ValueError("Box is already filled.")
        self.content = 'O'
        return True

    def is_filled(self) -> bool:
        return self.content is not None

    def get_content(self) -> str:
        return self.content
