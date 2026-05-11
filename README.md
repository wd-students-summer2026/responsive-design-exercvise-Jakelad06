# Responsive Design

Welcome! In this assignment, you will incorporate CSS media queries into your existing web pages from the most recent version of your personal web site that you have built in previous assignments. This will allow your page layout to become **responsive**, meaning their layout, content, and/or styles change based on the size of the viewer's web browser in order to make the page well-designed and perfectly fit to whatever device the user is using at the moment.

## Requirements

Some rules about responsive behaviors for all existing HTML pages.

On top of these requirements, you are welcome to add any additional responsive design features that you believe will make this page as accessible and amenabale to users as posssible.

### Copy existing web site files

The work you do in this assignment will be published to the same directory where your current web site currently exists. To prevent you from accidentally deleting any of your existing web site files, copy all the files from your existing web site into the main project directory for this assignment. This means copying any existing HTML, CSS, images, and other files and directories so a copy exists within this project directory. Then we will be able to upload everything in this directory to the web server and replace all existing files without worry about losing anything.

### Create three new CSS files

You will need to create three new CSS files within the `css` directory:

- `mobile.css` - styles that will apply to browser widths of **480px or less**
- `tablet.css` - styles that will apply to browser widths between **481px and 960px, inclusive**
- `desktop.css` - styles that will apply to browser widths of **961px or greater**

### Add media queries to all existing HTML pages

In order to make all pages of your site responsive, place the following three link tags and meta tag inside the head section of each of your HTML documents. You will notice that these link tags include **media queries**, which indicate at which widths these each of the stylesheet files will be loaded by the browser.

```html
<!-- Media query for narrow browser width -->
<link
  rel="stylesheet"
  media="only screen and (max-width: 480px)"
  href="css/mobile.css"
/>

<!-- Media query for medium browser width -->
<link
  rel="stylesheet"
  media="only screen and (min-width: 481px) and (max-width: 960px)"
  href="css/tablet.css"
/>

<!-- Media query for full browser width -->
<link
  rel="stylesheet"
  media="only screen and (min-width: 961px)"
  href="css/desktop.css"
/>

<!-- Prevent smartphones from scaling the page by default -->
<meta name="viewport" content="initial-scale=1" />
```

As the comments indicate, these media queries assess a viewer's browser width and use that information to determine which of three style sheets to use for the page: `mobile.css`, `tablet.css`, or `desktop.css`.

## Create responsive layout

Now that your web pages have the flexibility to access different style sheets at different browser widths, the next step is to optimize the layout with CSS for each of the widths specified.

Your task is the following:

- use a **container div** around all content of all pages - this must be given the class, `container` and must be used to center the page.
- create a `header` and `footer` that is repeated on all pages - these must have a consistent style across all pages and should be the full width of the container.
- create a **fixed width three-column layout for desktop** widths - the columns must sit side-by-side and each column must be one-third of the container width.
- create a **fixed width two-column layout for tablet** widths - the first two columns will sit side-by-side and each be half the container width, and the third column must be full width below those first two.
- create a **one-column scaling layout for smartphone** widths - all the elements that were side-by-side in the desktop and tablet layouts must now be stacked one on top of the other. The widths of each must be the full container width.
- _the width of the site pages must never be wider than the browser's width_.

Make sure to...

- add the class `column1` to any responsive elements that make up the left-most column at desktop width
- add the class `column2` to the responsive elements that make up the middle column at desktop width
- add the class `column3` to the responsive elements that make up the right-most column at desktop width

## Submit your work

In order to submit this assignment, you must publish all modified files to the web and upload the code to GitHub.

### Upload the web page to a web server

Upload all files you have created to a web server. Your instructor will have given you instructions for how to do this.

Take note of the web address (URL) of your web page - this is the address that can be plugged into the address bar of any web browser for the web browser to load and display your web page.

### Update the settings.json file

Make sure your name, NYU Net ID, and the exact URL of your web site's home page are placed into the `settings.json` file in the appropriate places. Make sure the URL works when plugged into a web browser beforehand.

**Additional settings**
Additionally, you **must** include the CSS-style selectors for the three responsive column classes in the `settings.json` file. These have been entered for you in this file, and you do not need to adjust them unless you change the class names for some reason,

### Submit your work on GitHub

You are now ready to submit this assignment. You can do so directly from Visual Studio Code with the following steps, in the indicated order:

1. Switch to the Source Control view in Visual Studio Code - this view will show you a list of the files you have modified.
1. In the "`Message`" text field towards the top-left, enter a unique message to yourself about what you have changed and, while still with the text field selected, type `Command`-`Enter` on Mac OS X, or `Control`-`Enter` on Windows, to "commit" the changes you've made with this custom message. If you forget to hit `Command`-`Enter` after typing the message, you can instead click the "`...`" button above the message field and click the "`Commit all`" option in the menu that appears.
1. Now, click the "`...`" button above the message field and click the "`Push`" option in the menu that appears - this will upload your changes to your personal code repository on GitHub.

You have now submitted your completed assignment. Your changes are now posted to GitHub.com, where the instructor and graders can access it. Your `settings.json` file has information about who you are and where we can view your page on the web.

You can verify all this yourself manually by visiting your repository on GitHub.com and making sure the code displayed there is what you submitted.
