"""
Tests for the responsive design assignment.

Requires Selenium 4.6+ (uses Selenium Manager to auto-manage chromedriver)
and a recent installation of Google Chrome.
"""

import json
import pytest
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


PAGES = ['index.html', 'about_me.html', 'more_about_me.html', 'topic_of_interest.html']

# tolerance, in pixels, for "fits inside" assertions (browsers can off-by-1
# rounding on sub-pixel layouts).
PX_TOLERANCE = 2


def _build_url(site_url, page=""):
  base = site_url.rstrip("/")
  if not page:
    return base + "/"
  return base + "/" + page.lstrip("/")


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

  # ------------------------------------------------------------------
  # static structural requirements
  # ------------------------------------------------------------------

  def test_header_exists(self, driver):
    """A <header> element must exist on the home page."""
    assert driver.find_element(By.TAG_NAME, "header")

  def test_footer_exists(self, driver):
    """A <footer> element must exist on the home page."""
    assert driver.find_element(By.TAG_NAME, "footer"), 'Footer element not found'

  def test_columns_exist(self, driver, settings):
    """Elements with each required column class must exist on the home page."""
    for selector in settings['responsive_column_selectors']:
      elems = driver.find_elements(By.CSS_SELECTOR, selector)
      assert elems, '{} element not found'.format(selector)

  def test_container_exists(self, driver):
    """A .container element must exist (wrapping the page content)."""
    elems = driver.find_elements(By.CSS_SELECTOR, ".container")
    assert elems, "No element with class 'container' was found."

  def test_viewport_meta(self, driver, settings):
    """A <meta name='viewport'> must be present on every page."""
    for page in PAGES:
      driver.get(_build_url(settings["site_url"], page))
      metas = driver.find_elements(By.CSS_SELECTOR, "meta[name='viewport']")
      assert metas, "No <meta name='viewport'> on {}".format(page)

  def test_three_media_query_stylesheets(self, settings):
    """Each of mobile.css / tablet.css / desktop.css must be downloadable."""
    for css in ('mobile.css', 'tablet.css', 'desktop.css'):
      url = _build_url(settings["site_url"], "css/" + css)
      try:
        with urlopen(url, timeout=10) as resp:
          assert resp.status == 200
      except Exception as e:
        raise AssertionError("Could not load {} : {}".format(url, e))

  # ------------------------------------------------------------------
  # responsive layout - mobile (<= 480)
  # ------------------------------------------------------------------

  def test_mobile_width(self, driver, settings):
    """At 480px viewport, each main element must fit inside the container."""
    browser_width = 480
    driver.set_window_size(browser_width, 900)

    for page in PAGES:
      driver.get(_build_url(settings["site_url"], page))

      try:
        container = driver.find_element(By.CSS_SELECTOR, ".container")
        header = driver.find_element(By.TAG_NAME, "header")
        footer = driver.find_element(By.TAG_NAME, "footer")
        column1 = driver.find_element(By.CSS_SELECTOR, ".column1")
        column2 = driver.find_element(By.CSS_SELECTOR, ".column2")
        column3 = driver.find_element(By.CSS_SELECTOR, ".column3")
      except Exception as e:
        assert False, 'Error analyzing {}: {}'.format(page, e)

      cw = container.size["width"]
      assert cw <= browser_width + PX_TOLERANCE, (
        'Container width on mobile is wider than the browser viewport on {}.'.format(page)
      )
      assert header.size["width"] <= cw + PX_TOLERANCE, (
        'Header wider than container on mobile, page {}.'.format(page)
      )
      assert footer.size["width"] <= cw + PX_TOLERANCE, (
        'Footer wider than container on mobile, page {}.'.format(page)
      )
      for c, name in ((column1, "1"), (column2, "2"), (column3, "3")):
        assert c.size["width"] <= cw + PX_TOLERANCE, (
          'Column {} wider than container on mobile, page {}.'.format(name, page)
        )

      # All three columns must stack one on top of the other.
      tops = sorted([column1.location['y'],
                     column2.location['y'],
                     column3.location['y']])
      assert tops[0] != tops[1] or tops[1] != tops[2], (
        'Columns are not stacked on mobile on {} - at least two share '
        'the same y-coordinate.'.format(page)
      )

  # ------------------------------------------------------------------
  # responsive layout - tablet (481-960)
  # ------------------------------------------------------------------

  def test_tablet_width(self, driver, settings):
    """
    At tablet widths the first two columns must sit side-by-side and the
    third column must be on its own row below them.
    """
    browser_widths = [481, 960]
    for browser_width in browser_widths:
      driver.set_window_size(browser_width, 900)

      for page in PAGES:
        driver.get(_build_url(settings["site_url"], page))

        try:
          container = driver.find_element(By.CSS_SELECTOR, ".container")
          header = driver.find_element(By.TAG_NAME, "header")
          footer = driver.find_element(By.TAG_NAME, "footer")
          column1 = driver.find_element(By.CSS_SELECTOR, ".column1")
          column2 = driver.find_element(By.CSS_SELECTOR, ".column2")
          column3 = driver.find_element(By.CSS_SELECTOR, ".column3")
        except Exception as e:
          assert False, 'Error analyzing {}: {}'.format(page, e)

        cw = container.size["width"]
        assert cw <= browser_width + PX_TOLERANCE, (
          'Container wider than viewport at {}px on {}.'.format(browser_width, page)
        )
        assert header.size["width"] <= cw + PX_TOLERANCE
        assert footer.size["width"] <= cw + PX_TOLERANCE
        for c in (column1, column2, column3):
          assert c.size["width"] <= cw + PX_TOLERANCE

        # The first two columns must fit side-by-side.
        assert (
          column1.size['width'] + column2.size['width'] <= cw + PX_TOLERANCE
        ), 'column1 + column2 do not fit in one container row on {}.'.format(page)

        # column3 must be on a row BELOW column1.
        assert (
          column3.location['y'] >= column1.location['y'] + column1.size['height']
          - PX_TOLERANCE
        ), 'column3 is not below column1 at tablet width on {}.'.format(page)

  # ------------------------------------------------------------------
  # responsive layout - desktop (>= 961)
  # ------------------------------------------------------------------

  def test_desktop_width(self, driver, settings):
    """At desktop widths all three columns must share a single row."""
    browser_widths = [961, 1400]
    for browser_width in browser_widths:
      driver.set_window_size(browser_width, 900)

      for page in PAGES:
        driver.get(_build_url(settings["site_url"], page))

        try:
          container = driver.find_element(By.CSS_SELECTOR, ".container")
          header = driver.find_element(By.TAG_NAME, "header")
          footer = driver.find_element(By.TAG_NAME, "footer")
          column1 = driver.find_element(By.CSS_SELECTOR, ".column1")
          column2 = driver.find_element(By.CSS_SELECTOR, ".column2")
          column3 = driver.find_element(By.CSS_SELECTOR, ".column3")
        except Exception as e:
          assert False, 'Error analyzing {}: {}'.format(page, e)

        cw = container.size["width"]
        assert cw <= browser_width + PX_TOLERANCE, (
          'Container wider than viewport at {}px on {}.'.format(browser_width, page)
        )
        assert header.size["width"] <= cw + PX_TOLERANCE
        assert footer.size["width"] <= cw + PX_TOLERANCE
        for c in (column1, column2, column3):
          assert c.size["width"] <= cw + PX_TOLERANCE

        total_col_w = (
          column1.size['width'] + column2.size['width'] + column3.size['width']
        )
        assert total_col_w <= cw + PX_TOLERANCE, (
          'The three columns do not fit in one row on desktop on {}.'.format(page)
        )

        # All three columns must share the same top y-coordinate (single row).
        tops = [column1.location['y'],
                column2.location['y'],
                column3.location['y']]
        assert max(tops) - min(tops) <= PX_TOLERANCE, (
          'Columns are not on the same row on desktop on {} (y-tops: {}).'
          .format(page, tops)
        )

  def test_container_centered_on_desktop(self, driver, settings):
    """The .container should be horizontally centered at desktop widths."""
    driver.set_window_size(1400, 900)
    driver.get(_build_url(settings["site_url"]))
    container = driver.find_element(By.CSS_SELECTOR, ".container")
    body_width = driver.execute_script("return document.body.clientWidth")
    left = container.location['x']
    right = body_width - (container.location['x'] + container.size['width'])
    # Allow some asymmetry but it should be approximately centered.
    assert abs(left - right) <= 40, (
      'The .container is not approximately centered on desktop '
      '(left margin {}, right margin {}).'.format(left, right)
    )
