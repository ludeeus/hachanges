"""Static texts."""
STYLE = """
<head>
    <title>Breaking changes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <style>
       @media only screen and (max-device-width : 1024px) {
            .row .col.s6 {
                width: 100%;
            }
        }
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
      <a href="#" class="brand-logo">&nbsp;&nbsp;&nbsp;Breaking changes for version 0.{version}.X</a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><a href="{previous}">Previous release</a></li>
        <li><a href="{next}">Next release</a></li>
      </ul>
    </div>
  </nav>
"""

CARD = """
  <div class="row">
    <div class="col s6">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text" id="{pull}">
          <a href="#{pull}"><span class="card-title"><i class="fa fa-link"></i> {title}</span></a>
          <p>{content}</p>
        </div>
        <div class="card-action">
          <a href="{docs}" target="_blank">Documentation</a>
          <a href="{prlink}" target="_blank">Pull request</a>
        </div>
      </div>
    </div>
  </div>
"""

NO_CHANGES = """
  <nav>
    <div class="nav-wrapper">
      <a href="#" class="brand-logo">&nbsp;&nbsp;&nbsp;Breaking changes</a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><a href="{previous}">Previous release</a></li>
        <li><a href="{next}">Next release</a></li>
      </ul>
    </div>
  </nav>
  <div class="row">
    <div class="col s12">
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
    <div class="col s12">
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
    <div class="col s12">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">Welcome!</span></a>
          <p>
            This site can give you an overview of breaking cahnges in Home Assistant releases.</br>
            To get breaking changes for a spesific release add the minor relase version at the end of the URL.
            </br></br>
            Generally a version are split in three "sections".</br>
            <i>major</i>.<b>minor</b>.<i>patch</i> it is the <b>minor</b> part you need to use here.</br></br>
            For version "0.85.0" this will be "85", examples:</br>
            <a href="https://hachanges.halfdecent.io/85" style="color: #ffab40;">https://hachanges.halfdecent.io/85</a></br>
            <a href="https://hachanges.halfdecent.io/85/json" style="color: #ffab40;">https://hachanges.halfdecent.io/85/json</a></br>
            </br>
            </br>
            <i>This site is not created, developed, affiliated, supported, maintained or endorsed by Home Assistant.</i>
          </p>
        </div>
      </div>
    </div>
  </div>
"""