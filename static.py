"""Static texts."""

NO_CHANGES = "Breaking changes for {} not found, try another."

WRONG_VERSION = """
Found . in the version, use the minor version <b>only</b></br>
Example: 85
"""

STYLE = """
<head>
    <link rel="shortcut icon" type="image/png" href="/favicon.png"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <style>
        body {
            padding-left: 5px !important;
            font-family: roboto !important;
        }
        .description {
            padding-left: 16px !important;
            max-width: 450px !important;
            font-style: italic !important;
            font-size: 14px !important;
        }
        .description a {
            font-style: normal !important;
            font-size: 12px !important;
        }
        .header a {
            text-decoration: none !important;
            color: black !important;
            font-weight: bold !important;
            font-size: 17px !important;
        }
        .fa {
            font-size:12px !important;
        }
    </style>
</head>
"""

HEADER = """
<h1>
    Breaking changes for version 0.{}.X
</h1>
"""

CHANGE_HEADER = """
<div class='header' id='{id}'>
    <a href="#{id}"><i class="fa fa-link"></i> {comp}</a>
    </br>
</div>
"""

CHANGE_DESCRIPTION = "<div class='description'>{}</br>"

CHANGE_LINKS = """
<a href="{}" target="_blank">Pull Request</a>
</br>
<a href="{}" target="_blank">Documentation</a>
"""

DEFAULT = """
You need to add /%version% to the url</br>
</br>
examples:</br>
https://hachanges.halfdecent.io/85</br>
https://hachanges.halfdecent.io/85/json
"""