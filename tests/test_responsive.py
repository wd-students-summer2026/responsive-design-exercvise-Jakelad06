"""
Tests for responsive design assignment.

Selenium webdriver for Chrome (a.k.a. the file named chromedriver) must be installed in either:
- in the same directory as chrome.exe on Windows (e.g. C:\Program Files\Google\Chrome\Application)
- in a directory that is included in the PATH on Mac OS X (e.g. /usr/local/bin)
"""

import pytest
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

class Tests:

  @pytest.fixture(scope="class")
  def settings(self):
    settings = json.load(open('./settings.json', 'r'))
    yield settings

  @pytest.fixture(scope="class")
  def driver(self):
    """
    Pop open a web browser and make it available to the tests.
    """
    settings = json.load(open('./settings.json', 'r'))
    print(settings["site_url"])

    # set up the fixture
    driver = webdriver.Chrome()
    driver.get(settings["site_url"]) # load the site from the settings file
    # provide the fixture value
    yield driver  
    # now tear it down
    driver.close()

  @pytest.fixture(scope='function')
  def zoom(self, driver):
    # zoom in by changing chrome's settings
    driver.get('chrome://settings/') # load chrome's settings page
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(1.5);')  # change zoom
    # make the zoomed in driver available
    yield driver
    # return back to normal when done
    driver.get('chrome://settings/') # load chrome's settings page
    driver.execute_script('chrome.settingsPrivate.setDefaultZoom(1);') # change zoom    

  # responsive design requirements
  def test_header_exists(self, driver, settings):
    """
    Check that header tag exists.
    """
    elem = driver.find_element_by_tag_name("header")
    assert elem

  def test_footer_exists(self, driver, settings):
    """
    Check that footer tag exists.
    """
    elem = driver.find_element_by_tag_name("footer")
    assert elem, 'Footer element not found'

  def test_columns_exist(self, driver, settings):
    """
    Check that elements exist with required column classes.
    """
    for selector in settings['responsive_column_selectors']:
      elem = driver.find_elements_by_css_selector(selector)
      assert elem, f'{selector} element not found'

  def test_mobile_width(self, settings, driver, zoom):
    """
    Check the width of elements with mobile css loaded.
    """
    # set the width to mobile-ish
    browser_width = 480
    driver.set_window_size(browser_width, 800)
    # ActionChains(driver).pause(1).perform() 

    # activate the body
    # elem = driver.find_element_by_tag_name('body')
    # ActionChains(driver).move_to_element(elem).perform()  # activate the body

    # the pages to test    
    pages = ['index.html', 'about_me.html', 'more_about_me.html', 'topic_of_interest.html']

    # test each page
    for page in pages:
      url = "{}/{}".format(settings["site_url"], page)
      driver.get(url) # return to page of interest

      try:
        container = driver.find_element_by_css_selector(".container")
        header = driver.find_element_by_tag_name("header")
        footer = driver.find_element_by_tag_name("footer")
        column1 = driver.find_element_by_css_selector(".column1")
        column2 = driver.find_element_by_css_selector(".column2")
        column3 = driver.find_element_by_css_selector(".column3")
      except Exception as e:
        assert False, f'Error analyzing {page}: {e}'

      # determine margin and padding on container
      # pl = int(container.value_of_css_property('padding-left')[:-2])
      # pr = int(container.value_of_css_property('padding-right')[:-2])
      # ml = int(container.value_of_css_property('margin-left')[:-2])
      # mr = int(container.value_of_css_property('margin-right')[:-2])
      # available_width = container.size['width'] - pl - pr - ml - mr

      # check widths are appropriate
      assert container.size["width"] <= browser_width, f'Container width on mobile is wider than the browser viewport on {page}.'
      assert header.size["width"] <= container.size["width"], f'Header width on mobile is wider than the container on {page}.'
      assert footer.size["width"] <= container.size["width"], f'Footer width on mobile is wider than the container on {page}.'
      assert column1.size["width"] <= container.size["width"], f'Column 1 width on mobile is wider than the container on {page}.'
      assert column2.size["width"] <= container.size["width"], f'Column 2 width on mobile is wider than the container on {page}.'
      assert column3.size["width"] <= container.size["width"], f'Column 3 width on mobile is wider than the container on {page}.'

      # check floats are appropriate
      # assert container.value_of_css_property('float') == 'none'
      # assert column1.value_of_css_property('float') == 'none'
      # assert column2.value_of_css_property('float') == 'none'
      # assert column3.value_of_css_property('float') == 'none'

  def test_tablet_width(self, settings, driver):
    """
    Check the width of elements with tablet css loaded.
    """
    # set the width to tablet-ish
    browser_widths = [481, 960]  # min and max tablet widths
    last_container_width = -1 # keep track of the width we detect
    # try out both min and max widths
    for browser_width in browser_widths:
      # set the browser width
      driver.set_window_size(browser_width, 800)

      # the pages to test    
      pages = ['index.html', 'about_me.html', 'more_about_me.html', 'topic_of_interest.html']

      # test each page
      for page in pages:
        url = "{}/{}".format(settings["site_url"], page)
        driver.get(url) # return to page of interest

        try:
          container = driver.find_element_by_css_selector(".container")
          header = driver.find_element_by_tag_name("header")
          footer = driver.find_element_by_tag_name("footer")
          column1 = driver.find_element_by_css_selector(".column1")
          column2 = driver.find_element_by_css_selector(".column2")
          column3 = driver.find_element_by_css_selector(".column3")
        except Exception as e:
          assert False, f'Error analyzing {page}: {e}'

        # determine margin and padding on container
        # pl = int(container.value_of_css_property('padding-left')[:-2])
        # pr = int(container.value_of_css_property('padding-right')[:-2])
        # ml = int(container.value_of_css_property('margin-left')[:-2])
        # mr = int(container.value_of_css_property('margin-right')[:-2])
        # available_width = container.size['width'] - pl - pr - ml - mr

        # check widths are appropriate
        assert container.size["width"] <= browser_width, f'Container width on tablet is wider than the browser viewport on {page}.'
        assert header.size["width"] <= container.size["width"], f'Header width on tablet is wider than the container on {page}.'
        assert footer.size["width"] <= container.size["width"], f'Footer width on tablet is wider than the container on {page}.'
        assert column1.size["width"] <= container.size["width"], f'Column 1 width on tablet is wider than the container on {page}.'
        assert column2.size["width"] <= container.size["width"], f'Column 2 width on tablet is wider than the container on {page}.'
        assert column3.size["width"] <= container.size["width"], f'Column 3 width on tablet is wider than the container on {page}.'

        # check that the columns fit in one row
        assert column1.size['width'] + column2.size['width'] <= container.size["width"]

        # remember the size of the container
        if last_container_width >= 0:
          assert container.size['width'] == last_container_width, 'Container width on tablet is not consistent.'
        else:
          last_container_width = container.size['width']

        # check floats are appropriate
        # assert container.value_of_css_property('float') == 'none'
        # assert column1.value_of_css_property('float') == 'left'
        # assert column2.value_of_css_property('float') == 'left'
        # assert column3.value_of_css_property('float') == 'left'

  def test_desktop_width(self, settings, driver):
    """
    Check the width of elements with desktop css loaded.
    """
    # set the width to desktop-ish
    # try out a few different sizes
    browser_widths = [961, 1400]
    last_container_width = -1 # keep track of the width we detect
    # try out both min and max widths
    for browser_width in browser_widths:
      # set the browser width
      driver.set_window_size(browser_width, 800)

      # the pages to test    
      pages = ['index.html', 'about_me.html', 'more_about_me.html', 'topic_of_interest.html']

      # test each page
      for page in pages:
        url = "{}/{}".format(settings["site_url"], page)
        driver.get(url) # return to page of interest

        try:
          container = driver.find_element_by_css_selector(".container")
          header = driver.find_element_by_tag_name("header")
          footer = driver.find_element_by_tag_name("footer")
          column1 = driver.find_element_by_css_selector(".column1")
          column2 = driver.find_element_by_css_selector(".column2")
          column3 = driver.find_element_by_css_selector(".column3")
        except Exception as e:
          assert False, f'Error analyzing {page}: {e}'

        # determine margin and padding on container
        # pl = int(container.value_of_css_property('padding-left')[:-2])
        # pr = int(container.value_of_css_property('padding-right')[:-2])
        # ml = int(container.value_of_css_property('margin-left')[:-2])
        # mr = int(container.value_of_css_property('margin-right')[:-2])
        # available_width = container.size['width'] - pl - pr - ml - mr

        # check widths are appropriate
        assert container.size["width"] <= browser_width, f'Container width on desktop is wider than the browser viewport on {page}.'
        assert header.size["width"] <= container.size["width"], f'Header width on desktop is wider than the container on {page}.'
        assert footer.size["width"] <= container.size["width"], f'Footer width on desktop is wider than the container on {page}.'
        assert column1.size["width"] <= container.size["width"], f'Column 1 width on desktop is wider than the container on {page}.'
        assert column2.size["width"] <= container.size["width"], f'Column 2 width on desktop is wider than the container on {page}.'
        assert column3.size["width"] <= container.size["width"], f'Column 3 width on desktop is wider than the container on {page}.'
        
        # check that the columns fit in one row
        assert column1.size['width'] + column2.size['width'] + column3.size['width'] <= container.size["width"], 'Columns do not fit in one row on desktop.'

        # remember the size of the container
        if last_container_width >= 0:
          assert container.size['width'] == last_container_width, f'Container width on desktop is not consistent on {page}.'
        else:
          last_container_width = container.size['width']

        # check floats are appropriate
        # assert container.value_of_css_property('float') == 'none'
        # assert column1.value_of_css_property('float') == 'left'
        # assert column2.value_of_css_property('float') == 'left'
        # assert column3.value_of_css_property('float') == 'left'
