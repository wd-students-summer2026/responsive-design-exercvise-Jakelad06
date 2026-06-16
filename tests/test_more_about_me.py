"""
Tests for the basic content of the more_about_me.html file in the CSS assignment.

Requires Selenium 4.6+ (uses Selenium Manager to auto-manage chromedriver)
and a recent installation of Google Chrome.
"""

import json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def _build_url(site_url, page=""):
  base = site_url.rstrip("/")
  if not page:
    return base + "/"
  return base + "/" + page.lstrip("/")


class Tests:

  @pytest.fixture(scope="class")
  def site_settings(self):
    with open('./settings.json', 'r') as f:
      yield json.load(f)

  @pytest.fixture(scope="class")
  def web_driver(self, site_settings):
    options = Options()
    options.add_argument("--window-size=1400,1000")
    driver = webdriver.Chrome(options=options)
    driver.get(_build_url(site_settings["site_url"], "more_about_me.html"))
    yield driver
    driver.quit()

  def test_h1_exists(self, web_driver):
    """An h1 element must exist."""
    elem = web_driver.find_element(By.TAG_NAME, "h1")
    assert elem and elem.text.strip() != ""

  def test_one_section(self, web_driver):
    """At least one <section> must exist."""
    elems = web_driver.find_elements(By.TAG_NAME, "section")
    assert len(elems) >= 1

  def test_paragraph_in_section(self, web_driver):
    """The section must include at least one <p> with text."""
    elems = web_driver.find_elements(By.CSS_SELECTOR, "section p")
    assert any((p.text or "").strip() for p in elems), (
      "No <p> with text content was found inside any <section>."
    )

  def test_two_images(self, web_driver):
    """At least two <img> elements must be present."""
    elems = web_driver.find_elements(By.TAG_NAME, "img")
    assert len(elems) >= 2

  def test_images_have_alt(self, web_driver):
    """Every <img> must have a non-empty alt attribute."""
    elems = web_driver.find_elements(By.TAG_NAME, "img")
    for img in elems:
      alt = img.get_attribute("alt")
      assert alt is not None and alt.strip() != "", (
        "An <img> element is missing an alt attribute: {}".format(
          img.get_attribute("src")
        )
      )

  def test_link_href_exists(self, web_driver):
    """Relative links back to index.html and about_me.html must exist."""
    target_urls = ['index.html', 'about_me.html']
    for url in target_urls:
      try:
        a = web_driver.find_element(By.CSS_SELECTOR, "a[href='{}']".format(url))
      except NoSuchElementException:
        a = None
      assert a, "Missing relative <a href='{}'> on this page.".format(url)

  def test_css_loaded(self, web_driver):
    """The site-wide stylesheet (css/main.css) must be linked from this page."""
    links = web_driver.find_elements(By.CSS_SELECTOR, "link[rel='stylesheet']")
    hrefs = [l.get_attribute("href") or "" for l in links]
    assert any("css/main.css" in h for h in hrefs), (
      "No <link rel='stylesheet' href='css/main.css'> was found."
    )
