Tutorial
========

Start by defining a `require.js i18n bundle`_.
In a require.js application called `site` you might have the following i18n directory
structure::

  site/nls/colors.js
  site/nls/root/colors.js

Let's say you want to add a translation for Dutch (`nl`). Enable the language
code `nl` in `site/nls/colors.js`::

  define({
      "root": true,

      "nl": true
  });

The root file `site/nls/root/colors.js` contains the key/value pairs to translate::

  // Copyright (c) My Project

  define(
  {
      "closeLabel": "Close",
      "openLabel": "Open"
  }
  );

Run the `compile_js` command to extract the translation strings and generate a
catalog for the `nl` locale::

  manage.py compile_js --no-empty -l nl


.. _require.js i18n bundle: http://requirejs.org/docs/api.html#i18n