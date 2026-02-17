def test_google_navigation(page):
    page.goto("http://127.0.0.1:5000")

    page.fill("#site", "google")
    page.click("#login-btn")

    page.wait_for_url("https://www.google.com/**")
    assert "google" in page.url.lower()
def test_youtube_navigation(page):
    page.goto("http://127.0.0.1:5000")
    page.fill("#site", "youtube")
    page.click("#login-btn")
    page.wait_for_url("https://www.youtube.com/**")
    assert "youtube" in page.url.lower()
def test_yahoo_navigation(page):
    page.goto("http://127.0.0.1:5000")
    page.fill("#site", "yahoo")
    page.click("#login-btn")
    page.wait_for_url("https://www.yahoo.com/**")
    assert "yahoo" in page.url.lower()  
def test_invalid_navigation(page):
    page.goto("http://127.0.0.1:5000")
    page.fill("#site", "invalidsite")
    page.click("#login-btn")
    page.wait_for_url("http://127.0.0.1:5000/") 
    assert page.url == "http://127.0.0.1:5000/"
    