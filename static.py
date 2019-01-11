"""Static texts."""

NO_CHANGES = "Breaking changes for {} not found, try another."

WRONG_VERSION = """
Found . in the version, use the minor version <b>only</b></br>
Example: 85
"""

STYLE = """
<head>
    <link rel="shortcut icon" type="image/png" href="/favicon.png"/>
    <style>
        body {
            padding-left: 5px;
        }
        div {
            padding-left: 16px;
            max-width: 450px;
        }
        a {
            padding-right: 16px;
            padding-top: 16px;
        }
    </style>
</head>
"""

HEADER = """
<h1>
    Breaking changes for version 0.{}.X
</h1>
"""

LINKS = """
<a href="{}" target="_blank">
    Pull Request
</a>
</br>
<a href="{}" target="_blank">
    Documentation
</a>
"""

DEFAULT = """
You need to add /%version% to the url</br>
</br>
examples:</br>
https://hachanges.halfdecent.io/85</br>
https://hachanges.halfdecent.io/85/json
"""