import {
  LitElement,
  customElement,
  TemplateResult,
  html,
  css,
} from 'lit-element';

import { Style } from './style';

@customElement('breakingchanges-footer')
class BreakingChangesFooter extends LitElement {
  protected render(): TemplateResult | void {
    return html`<div class="footer">
      This site is not created, developed, affiliated, supported, maintained or
      endorsed by Home Assistant.
    </div>`;
  }

  static get styles() {
    return [
      Style,
      css`
        .footer {
          width: 100%;
          bottom: 0;
          height: 16px;
          position: absolute;
          text-align: center;
          padding: 12px 0;
          font-style: italic;
          font-size: 12px;
          background-color: var(--theme-background-color-card);
        }
      `,
    ];
  }
}
