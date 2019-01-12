"""Static texts."""
STYLE = """
<head>
    <title>Breaking changes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <style>
        body {
            padding-left: 5px !important;
            font-family: roboto !important;
        }
        .fa {
            font-size:18px !important;
        }
        code {
            font-family: roboto !important;
            font-size: 14px !important;
        }
        nav {
            background-color: #546e7a !important;
            margin-bottom: 32px;
        }
        .card-title {
            color: white;
        }
    </style>
</head>
"""
HEADER = """
  <nav>
    <div class="nav-wrapper">
      <a href="#" class="brand-logo">&nbsp;&nbsp;&nbsp;Breaking changes for version 0.{}.X</a>
    </div>
  </nav>
"""

CARD = """
  <div class="row">
    <div class="col s12 m6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text" id="{pull}">
          <a href="#{pull}"><span class="card-title"><i class="fa fa-link"></i> {title}</span></a>
          <p>{content}</p>
        </div>
        <div class="card-action">
          <a href="{docs}">Documentation</a>
          <a href="{pull}">Pull request</a>
        </div>
      </div>
    </div>
  </div>
"""

NO_CHANGES = """
  <nav>
    <div class="nav-wrapper">
      <a href="#" class="brand-logo">&nbsp;&nbsp;&nbsp;Breaking changes</a>
    </div>
  </nav>
  <div class="row">
    <div class="col s12 m6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <p>Breaking changes for {version} not found, try another.</p>
        </div>
      </div>
    </div>
  </div>
"""

WRONG_VERSION = """
  <nav>
    <div class="nav-wrapper">
      <a href="#" class="brand-logo">&nbsp;&nbsp;&nbsp;Breaking changes</a>
    </div>
  </nav>
    <div class="row">
    <div class="col s12 m6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <p>Found "." in the version, use the minor version <b>only</b></br>
          Example: 85</p>
        </div>
      </div>
    </div>
  </div>
"""

DEFAULT = """
  <nav>
    <div class="nav-wrapper">
      <a href="#" class="brand-logo">&nbsp;&nbsp;&nbsp;Breaking changes</a>
    </div>
  </nav>
  <div class="row">
    <div class="col s12 m6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">You need to add /%version% to the url</span></a>
          <p>Examples:
            https://hachanges.halfdecent.io/85</br>
            https://hachanges.halfdecent.io/85/json
          </p>
        </div>
        <div class="card-action">
          <a href="https://hachanges.halfdecent.io/85">/85</a>
          <a href="https://hachanges.halfdecent.io/85/json}">/85/json</a>
        </div>
      </div>
    </div>
  </div>
"""