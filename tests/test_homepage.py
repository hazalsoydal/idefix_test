def test_homepage_opens(home_page):
    home_page.open()
    home_page.close_popups()
    assert home_page.wait_search_box().is_displayed()

    #homepagedriver accesses the browser driver

    #Find an element whose id is search-input diyo find_element ile.
    #isdisplayed de zaten diyo ki hani is this element visible on the page???