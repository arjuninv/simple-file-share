import pytest
def test_add_file():
    file_name = "test_file_name"
    file_url = "test_file_url"
    file_author = "test_file_author"
    def add_file(file_name, file_url, file_author):
        data = { "file_name": file_name, "file_url": file_url, "file_author": file_author}
        assert data == { "file_name": "test_file_name", "file_url": "test_file_url", "file_author": "test_file_author"}, "test failed"


if __name__ == '__main__':
    test_add_file()