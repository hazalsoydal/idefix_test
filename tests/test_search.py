def test_search_book(home_page):
    home_page.open()
    home_page.search("book")
    assert "book" in home_page.driver.current_url.lower()