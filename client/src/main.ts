import {
  LitElement,
  customElement,
  TemplateResult,
  html,
  css,
  property,
} from 'lit-element';

import './changes';
import './entry';
import { Style } from './style';

@customElement('breakingchanges-main')
class BreakingChangesMain extends LitElement {
  @property() public page = '/';

  public async connectedCallback() {
    super.connectedCallback();
    this.page = window.location.pathname;
  }

  protected render(): TemplateResult | void {
    return html`
      <div class="maincontent">
        ${this.page === '/'
          ? html`
              <breakingchanges-entry></breakingchanges-entry>
            `
          : html`
              <breakingchanges-changes></breakingchanges-changes>
            `}
      </div>
      <breakingchanges-footer></breakingchanges-footer>
    `;
  }

  static get styles() {
    return [
      Style,
      css`
        .maincontent {
          width: 100%;
          overflow-y: auto;
          height: calc(100vh - 40px);
          color: var(--primary-text-color);
          background-color: var(--theme-background-color);
        }
      `,
    ];
  }
}
