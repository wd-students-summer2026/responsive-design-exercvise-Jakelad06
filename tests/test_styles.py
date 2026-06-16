"""
Tests for CSS styles across the pages of the personal site.

Requires Selenium 4.6+ (uses Selenium Manager to auto-manage chromedriver)
and a recent installation of Google Chrome.
"""

import json
import pytest
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def _build_url(site_url, page=""):
  base = site_url.rstrip("/")
  if not page:
    return base + "/"
  return base + "/" + page.lstrip("/")


# Browser-default serif fonts (Times / "Times New Roman") used to detect
# whether the student supplied any non-default font-family for an element.
_DEFAULT_FONT_FRAGMENTS = ("times new roman", "times")


def _has_non_default_font(font_family):
  ff = (font_family or "").lower()
  # the value usually looks like:  "Open Sans", Arial, sans-serif
  return all(frag not in ff for frag in _DEFAULT_FONT_FRAGMENTS) or "," in ff


class Tests:

  @pytest.fixture(scope="class")
  def settings(self):
    with open('./settings.json', 'r') as f:
      yield json.load(f)

  @pytest.fixture(scope="class")
  def driver(self, settings):
    options = Options()
    options.add_argument("--window-size=1400,1000")
    driver = webdriver.Chrome(options=options)
    driver.get(_build_url(settings["site_url"]))
    yield driver
    driver.quit()

  def test_main_css_loads(self, settings):
    """css/main.css must be downloadable from the site root."""
    url = _build_url(settings["site_url"], "css/main.css")
    try:
      with urlopen(url, timeout=10) as resp:
        body = resp.read().decode("utf-8", errors="ignore")
        assert resp.status == 200
        assert body.strip() != "", "css/main.css is empty."
    except Exception as e:
      raise AssertionError("Could not load {} : {}".format(url, e))

  def test_global_p_styles(self, driver, settings):
    """Paragraphs across all content pages must have a non-default font."""
    pages = ['about_me.html', 'more_about_me.html']
    for page in pages:
      driver.get(_build_url(settings["site_url"], page))
      elems = driver.find_elements(By.TAG_NAME, "p")
      assert elems, "No <p> elements found on {}".format(page)
      for elem in elems:
        ff = elem.value_of_css_property('font-family')
        assert _has_non_default_font(ff), (
          "A <p> on {} has the default font-family ({}). Set a custom "
          "font-family in css/main.css.".format(page, ff)
        )

  def test_global_h_styles(self, driver, settings):
    """h1, h2, h3 across all content pages must have a non-default font."""
    pages = ['about_me.html', 'more_about_me.html']
    for page in pages:
      driver.get(_build_url(settings["site_url"], page))
      elems = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
      assert elems, "No h1/h2/h3 found on {}".format(page)
      for elem in elems:
        ff = elem.value_of_css_property('font-family')
        assert _has_non_default_font(ff), (
          "A heading on {} has the default font-family ({}).".format(page, ff)
        )

  def test_global_a_styles(self, driver, settings):
    """
    Hovering over a link must change either the text colour or the
    background colour. We test one link per page to avoid issues with
    off-screen elements.
    """
    pages = ['index.html', 'about_me.html', 'more_about_me.html']
    for page in pages:
      driver.get(_build_url(settings["site_url"], page))
      anchors = [
        a for a in driver.find_elements(By.TAG_NAME, "a")
        if a.is_displayed()
      ]
      assert anchors, "No visible <a> elements on {}".format(page)
      target = anchors[0]

      driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", target
      )

      default_text_color = target.value_of_css_property('color')
      default_bg_color = target.value_of_css_property('background-color')

      ActionChains(driver).move_to_element(target).pause(0.2).perform()

      hover_text_color = target.value_of_css_property('color')
      hover_bg_color = target.value_of_css_property('background-color')

      ActionChains(driver).move_by_offset(0, 0).pause(0).perform()

      assert (
        default_text_color != hover_text_color
        or default_bg_color != hover_bg_color
      ), (
        "Hovering over a link on {} did not change its colour or "
        "background-colour. Define a distinct :hover style for <a> "
        "elements in css/main.css.".format(page)
      )

  def test_section_padding_styles(self, driver, settings):
    """Sections on the about_me and more_about_me pages must have padding."""
    pages = ['about_me.html', 'more_about_me.html']
    for page in pages:
      driver.get(_build_url(settings["site_url"], page))
      elems = driver.find_elements(By.CSS_SELECTOR, "section")
      assert elems, "No <section> elements on {}".format(page)
      for elem in elems:
        for side in ('padding-top', 'padding-right',
                     'padding-bottom', 'padding-left'):
          val = elem.value_of_css_property(side)
          px = float((val or "0px").rstrip("px") or 0)
          assert px > 0, (
            "A <section> on {} has no {} ({}). All four sides must have "
            "padding.".format(page, side, val)
          )

  def test_section_margin_styles(self, driver, settings):
    """Sections must have a bottom margin to separate them visually."""
    pages = ['about_me.html', 'more_about_me.html']
    for page in pages:
      driver.get(_build_url(settings["site_url"], page))
      elems = driver.find_elements(By.CSS_SELECTOR, "section")
      assert elems, "No <section> elements on {}".format(page)
      for elem in elems:
        mb = elem.value_of_css_property('margin-bottom')
        px = float((mb or "0px").rstrip("px") or 0)
        assert px > 0, (
          "A <section> on {} has no bottom margin ({}).".format(page, mb)
        )

  def test_section_border_styles(self, driver, settings):
    """Sections must have some kind of visible border."""
    pages = ['about_me.html', 'more_about_me.html']
    for page in pages:
      driver.get(_build_url(settings["site_url"], page))
      elems = driver.find_elements(By.CSS_SELECTOR, "section")
      assert elems, "No <section> elements on {}".format(page)
      for elem in elems:
        widths = [
          elem.value_of_css_property('border-top-width'),
          elem.value_of_css_property('border-right-width'),
          elem.value_of_css_property('border-bottom-width'),
          elem.value_of_css_property('border-left-width'),
        ]
        nums = [float((w or "0px").rstrip("px") or 0) for w in widths]
        assert any(n > 0 for n in nums), (
          "A <section> on {} has no visible border. Set a border in "
          "css/main.css.".format(page)
        )

  def test_section_ids(self, driver, settings):
    """The two required sections on about_me.html must have the right ids."""
    driver.get(_build_url(settings["site_url"], "about_me.html"))
    elem1 = driver.find_element(By.CSS_SELECTOR, "section#my_background")
    elem2 = driver.find_element(By.CSS_SELECTOR, "section#my_interests")
    assert elem1 and elem2

  def test_section_backgrounds(self, driver, settings):
    """
    Each of the two required sections on about_me.html must have either
    a background-color or background-image, not just the page default.
    """
    driver.get(_build_url(settings["site_url"], "about_me.html"))
    for sid in ("my_background", "my_interests"):
      sec = driver.find_element(By.CSS_SELECTOR, "section#" + sid)
      bg_image = sec.value_of_css_property('background-image') or "none"
      bg_color = sec.value_of_css_property('background-color') or ""
      has_image = bg_image.lower() != "none"
      # browser default is "rgba(0, 0, 0, 0)" (fully transparent)
      has_color = (
        bg_color
        and "rgba(0, 0, 0, 0)" not in bg_color.replace(" ", " ")
      )
      assert has_image or has_color, (
        "section#{} on about_me.html has neither a background-image nor "
        "a background-color set in CSS.".format(sid)
      )

  def test_h2_in_section_has_custom_style(self, driver, settings):
    """
    The README requires a style that applies only to h2 elements nested
    inside <section> on about_me.html. We check that those h2s do not
    have the same font-family as a bare h2 (i.e. that the selector
    "section h2" has done something).
    """
    driver.get(_build_url(settings["site_url"], "about_me.html"))
    h2s = driver.find_elements(By.CSS_SELECTOR, "section h2")
    assert h2s, "No <h2> elements inside <section> on about_me.html."
    for h in h2s:
      ff = h.value_of_css_property('font-family')
      assert _has_non_default_font(ff), (
        "An h2 inside <section> on about_me.html still uses the default "
        "font-family ({}). Add a `section h2` rule in css/main.css.".format(ff)
      )
