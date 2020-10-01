import timeit


class Pieces:
    """
    Args:
            start (int): The start position in the document
            length (int): The number of characters after the start position
            source (string): The key to chose the text from 
    """
    def __init__(self, start, length, source):
        self.start = start
        self.length = length
        self.source = source


class SimpleEditor:

    def __init__(self, document):
        """
        Initializes 4 data structures used in the SimpleEditor class:
        1. self.dictionary - It is a set of english words which is used to check for misspellings
        2. self.piece_table - dictionary used for making efficient edits 
        3. self.undo_stack - stack to store text after operations like cut, copy, delete, and paste for undo operation
        4. self.redo_stack - stack to store text after undo operation
        
        Args:
                document (string): text stored in the editor
        """
        self.DICTIONARY_FILE = "spell.words.txt"
        self.dictionary = set()
        self.piece_table = {"original": document, "add": "", "cut": "", "pieces": [
            Pieces(0, len(document), "original")]}

        self.undo_stack = [document]
        self.redo_stack = [document]

        with open(self.DICTIONARY_FILE) as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)

        self.paste_text = ""

    def delete(self, offset, length):
        """
        Deletes `length` number of characters starting at position `offset`
        Equivalent to deleting text[offset:offset + length]

        Args:
                offset (int): The start position to delete from
                length (int): The number of characters to delete
        
        returns:
                    updated document after deleting text
        """

        original_text = self.piece_table["original"]
        if offset < 0 or offset >= len(original_text):
            raise NameError("Offset OutOfBounds Error!!")

        left_piece = Pieces(0, offset, "original")
        right_piece = Pieces(
            offset + length, len(original_text) - length + 1, "original")
        self.piece_table["pieces"][0] = left_piece
        if len(self.piece_table["pieces"]) == 1:
            self.piece_table["pieces"].append(right_piece)
        else:
            self.piece_table["pieces"][1] = right_piece

        updated_text = self.get_text()
        # add text after delete operation to undo stack to perform undo operations
        self.undo_stack.append(updated_text)
        return updated_text

    def undo(self):
        """
        pops the top text in the undo_stack and appends it to the redo_stack
        
        returns:
                    text after undo operation
        """

        if self.undo_stack:
            recent_text = self.undo_stack.pop()
            self.redo_stack.append(recent_text)
            if self.piece_table["cut"]:
                self.piece_table["cut"] = self.undo_stack[-1]
            return self.undo_stack[-1]

    def redo(self):
        """
        pops the top text in the redo_stack and appends it to the undo_stack and returns it
        
        returns:
                    text after redo operation
        """

        if self.redo_stack:
            recent_text = self.redo_stack.pop()
            self.undo_stack.append(recent_text)
            if self.piece_table["cut"]:
                self.piece_table["cut"] = self.undo_stack[-1]
            return recent_text

    def highlight_text(self, offset, length):
        """
        highlights `length` number of characters starting at position `offset`

        Args:
                offset (int): The start position to highlight from
                length (int): The number of characters to highlight
        
        returns:
                    highlighted text
        """
        return self.piece_table["original"][offset: offset + length]

    def cut(self, offset, length):
        """
        Cuts `length` number of characters starting at position `offset`

        Args:
                offset (int): The start position to cut text from
                length (int): The number of characters to cut
        
        returns:
                    text after cut operation
        """

        # if cut text exists that means we have used this operation in the past, so use the latest text from the cut field else use the original one
        if self.piece_table["cut"]:
            original_text = self.piece_table["cut"]
            source = "cut"
        else:
            original_text = self.piece_table["original"]
            source = "original"

        if offset < 0 or offset >= len(original_text):
            raise NameError("Offset OutOfBounds Error!!")

        left_piece = Pieces(0, offset, source)
        right_piece = Pieces(
            offset + length, len(original_text) - length + 1, source)
        self.piece_table["pieces"][0] = left_piece
        if len(self.piece_table["pieces"]) == 1:
            self.piece_table["pieces"].append(right_piece)
        else:
            self.piece_table["pieces"][1] = right_piece
        self.paste_text = original_text[offset:offset+length]
        self.piece_table["cut"] = original_text[: offset] + \
            original_text[offset + length:]

        updated_text = self.piece_table["cut"]
        # add text after cut operation to undo stack to perform undo operations
        self.undo_stack.append(updated_text)
        return updated_text

    def copy(self, offset, length):
        """
        Copies `length` number of characters starting at position `offset`

        Args:
                offset (int): The start position to copy text from
                length (int): The number of characters to copy
        
        returns:
                    copied text
        """
        original_text = self.piece_table["original"]
        if offset < 0 or offset >= len(original_text):
            raise NameError("Offset OutOfBounds Error!!")
        self.paste_text = original_text[offset: offset + length]
        return self.paste_text

    def paste(self, offset):
        """
        Pastes the text in self.paste_text variable at position `offset`

        Args:
                offset (int): The start position to cut text from
        
        returns:
                    text after paste operation
        """
        self.piece_table["add"] = self.paste_text
        original_text, source = '', ''
        # if paste is called after cut operation, then update the original text with text in the cut field
        if self.piece_table["cut"]:
            original_text = self.piece_table["cut"]
            source = "cut"
        else:
            original_text = self.piece_table["original"]
            source = "original"

        if offset < 0 or offset >= len(original_text):
            raise NameError("Offset OutOfBounds Error!!")

        left_piece = Pieces(0, offset, source)
        middle_piece = Pieces(0, len(self.paste_text), "add")
        right_piece = Pieces(offset, len(original_text) - offset, source)
        #TOD
        self.piece_table["pieces"][0] = left_piece
        if len(self.piece_table["pieces"]) == 1:
            self.piece_table["pieces"].append(middle_piece)
            self.piece_table["pieces"].append(right_piece)
        elif len(self.piece_table["pieces"]) == 2:
            self.piece_table["pieces"][1] = middle_piece
            self.piece_table["pieces"].append(right_piece)
        else:
            self.piece_table["pieces"][1] = middle_piece
            self.piece_table["pieces"][2] = right_piece

        updated_text = self.get_text()
        # add text after paste operation to undo stack to perform undo operations
        self.undo_stack.append(updated_text)
        # update the cut text
        if self.piece_table["cut"]:
            self.piece_table["cut"] = updated_text
        return updated_text

    def get_text(self):
        """
        returns:
                    combined text from all the pieces in the piece_table
        """
        text = ''
        for piece in self.piece_table["pieces"]:
            src = piece.source
            text += self.piece_table[src][piece.start:piece.start+piece.length]
        return text

    def misspellings(self):
        """
        returns:
                    number of misspelled words in the document
        """
        result = 0
        original_text = self.piece_table["original"]
        for word in original_text.split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result


class EditorBenchmarker:
    new_editor_case = """
from __main__ import SimpleEditor
s = SimpleEditor("{}")"""

    editor_delete_undo = """
for n in range(2,{}):
    if n % 2 == 0:
        s.delete(10,100)
    else:
        s.undo()"""

    editor_delete_text = """
for n in range({}):
    s.delete(10,100)"""

    editor_highlight_text = """
for n in range({}):
    s.highlight_text(10,100)"""

    editor_cut_paste = """
for n in range(2,{}):
    if n%2 == 0:
        s.cut(10,100)
    else:
        s.paste(65)"""

    editor_copy_paste = """
for n in range(2,{}):
    if n%2 == 0:
        s.copy(10,100)
    else:
        s.paste(65)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_cut_redo = """
for n in range(2,{}):
    if n%2 == 0:
        s.cut(10,100)
    else:
        s.paste(65)
        s.undo()
        s.redo()"""

    editor_cut_undo = """
for n in range(2,{}):
    if n%2 == 0:
        s.cut(10,100)
    else:
        s.undo()"""

    editor_mispellings = """
for n in range({}):
    s.misspellings()"""

    def __init__(self, cases, N):
        self.cases = cases
        self.N = N
        self.editor_cut_paste = self.editor_cut_paste.format(N)
        self.editor_cut_undo = self.editor_cut_undo.format(N)
        self.editor_cut_redo = self.editor_cut_redo.format(N)
        self.editor_delete_text = self.editor_delete_text.format(N)
        self.editor_highlight_text = self.editor_highlight_text.format(N)
        self.editor_delete_undo = self.editor_delete_undo.format(N)
        self.editor_copy_paste = self.editor_copy_paste.format(N)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)

    def benchmark(self):
        for case in self.cases:
            print("Evaluating case: {}".format(case))
            new_editor = self.new_editor_case.format(case)
            delete_text_time = timeit.timeit(stmt=self.editor_delete_text, setup=new_editor, number=1)
            print("{} delete text operations took {} s".format(self.N, delete_text_time))
            delete_undo_time = timeit.timeit(stmt=self.editor_delete_undo, setup=new_editor, number=1)
            print("{} delete and undo text operations took {} s".format(self.N, delete_undo_time))
            highlight_time = timeit.timeit(stmt=self.editor_highlight_text, setup=new_editor, number=1)
            print("{} highlight operations took {} s".format(self.N, highlight_time))
            cut_undo_time = timeit.timeit(stmt=self.editor_cut_undo, setup=new_editor, number=1)
            print("{} cut undo operations took {} s".format(self.N, cut_undo_time))
            cut_redo_time = timeit.timeit(stmt=self.editor_cut_redo, setup=new_editor, number=1)
            print("{} cut redo operations took {} s".format(self.N, cut_redo_time))
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste, setup=new_editor, number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste, setup=new_editor, number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text, setup=new_editor, number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings, setup=new_editor, number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))


if __name__ == "__main__":
    text = ''
    f = open("demofile.txt", "r")
    for x in f:
        text += x
    b = EditorBenchmarker([text], 1000)
    b.benchmark()