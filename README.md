# Portal Plugin for FlaskBB

This plugin provides a simple portal for FlaskBB.

In addition to the settings that can be changed via the management panel,
one setting has to be added (if desired) to your ``flaskbb.cfg``:
```python
PLUGIN_PORTAL_URL_PREFIX="/yourportalurlprefix"
```
This setting allows you to change the URL of the portal from the default
value of ``/portal`` to something else. Be sure to **not** change it something that
could conflict with one of the ``URL_PREFIX``es of FlaskBB.


# Installation

This plugin can be installed from PyPI via:
```bash
$ pip install flaskbb-plugin-portal
```


# License

``flaskbb-plugin-portal`` is licensed under the
[BSD License](https://github.com/sh4nks/flaskbb-plugins/blob/master/LICENSE).


# Links

* [Project Website](https://flaskbb.org)
* [Documentation](https://flaskbb.readthedocs.io)
* [Source Code](https://github.com/sh4nks/flaskbb)
