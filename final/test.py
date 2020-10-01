import pytest
TextEditor = __import__("editor")
original_text = "Neeva is Awesome"


def test_copy_paste():
    editor = TextEditor.SimpleEditor(original_text)
    copy_text = editor.copy(0, 5)
    editor.paste(5)
    final_text = editor.get_text()
    assert copy_text == "Neeva", "Copy not working"
    assert final_text == 'NeevaNeeva is Awesome', "test_copy_paste failed!!"


def test_cut_paste():
    editor = TextEditor.SimpleEditor(original_text)
    text_after_cut = editor.cut(0, 5)
    editor.paste(3)
    final_text = editor.piece_table["cut"]
    assert text_after_cut == " is Awesome", "Cut not working"
    assert final_text == ' isNeeva Awesome', "test_cut_paste failed!!"


def test_delete():
    editor = TextEditor.SimpleEditor(original_text)
    text_after_delete = editor.delete(0, 5)
    assert text_after_delete == " is Awesome", "test_delete failed!!"


def test_undo():
    editor = TextEditor.SimpleEditor(original_text)
    text_after_cut = editor.cut(0, 5)
    text_after_paste = editor.paste(8)
    text_on_editor = editor.undo()
    assert text_on_editor == text_after_cut, "test_undo failed!!"


def test_redo():
    editor = TextEditor.SimpleEditor(original_text)
    text_after_cut = editor.cut(0, 5)
    text_after_paste = editor.paste(8)
    undo_text = editor.undo()
    assert undo_text == text_after_cut, "test_redo failed!!"
    text_after_redo = editor.redo()
    assert text_after_paste == text_after_redo, "test_redo failed!!"


def test_highlight():
    editor = TextEditor.SimpleEditor(original_text)
    highlighted_text = editor.highlight_text(0, 5)
    assert highlighted_text == "Neeva", "test_highlight failed!!"


def test_get_text():
    editor = TextEditor.SimpleEditor(original_text)
    assert editor.get_text() == original_text, "test_get_text failed!!"


def test_mispelling():
    editor = TextEditor.SimpleEditor(original_text)
    assert editor.misspellings() == 2, "test_misspelling failed!!"


if __name__ == "__main__":
    print("Testing Copy Paste Feature")
    test_copy_paste()
    print("Test Successful")

    print("Testing Cut Paste Feature")
    test_cut_paste()
    print("Test Successful")

    print("Testing undo Feature")
    test_undo()
    print("Test Successful")

    print("Testing redo Feature")
    test_redo()
    print("Test Successful")

    print("Testing delete Feature")
    test_delete()
    print("Test Successful")

    print("Testing highlight Feature")
    test_highlight()
    print("Test Successful")

    print("Testing get text Feature")
    test_get_text()
    print("Test Successful")

    print("Testing misspelling Feature")
    test_mispelling()
    print("Test Successful")
