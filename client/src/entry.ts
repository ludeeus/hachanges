import { LitElement, customElement, TemplateResult, html } from 'lit-element';
import '@polymer/paper-card';

import './footer';

import { Style } from './style';

@customElement('breakingchanges-entry')
class BreakingChangesEntry extends LitElement {
  protected render(): TemplateResult | void {
    return html`<div class="content">
      <div class="header"><h1>Welcome!</h1></div>
      <paper-card>
        <div class="card-content">
          <p>
            This site can give you an overview of breaking changes in Home
            Assistant releases. To get breaking changes for a specific release
            add the minor relase version at the end of the URL.
          </p>
          <p>
            Generally a version is split into three "sections".
            major.<b>minor</b>.patch it is the <b>minor</b> part you need to use
            here.
          </p>
          <p>
            For version "0.114.0" this will be "114", examples:
            <li><a href="/114">https://hachanges.halfdecent.io/114</a></li>
            <li>
              <a href="/114/json">https://hachanges.halfdecent.io/114/json</a>
            </li>
          </p>
        </div>
      </paper-card>
    </div>`;
  }

  static get styles() {
    return Style;
  }
}
