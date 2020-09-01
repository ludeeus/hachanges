import {
  LitElement,
  customElement,
  TemplateResult,
  html,
  property,
  css,
} from 'lit-element';
import '@polymer/iron-icon';
import '@polymer/iron-icons';
import '@material/mwc-button';
import '@polymer/paper-card';

import './footer';

import { Change, getChanges } from './data';
import { Style } from './style';

@customElement('breakingchanges-changes')
class BreakingChangesChanges extends LitElement {
  @property({ attribute: false }) private _changes: Change[] = [];

  @property() private _version!: string;
  @property({ type: Boolean }) private _init = true;

  public async connectedCallback() {
    super.connectedCallback();
    const version = window.location.pathname.replace('/', '');
    this._version = version;

    this._changes = await getChanges(version);
    this._init = false;
  }

  protected render(): TemplateResult | void {
    if (this._init) {
      return html``;
    }
    return html`<div class="content">
      <div class="header">
        <a href="/"><iron-icon icon="arrow-back" title="Back"></iron-icon></a>
        <h1>Breaking changes for ${this._version}</h1>
      </div>
      ${this._changes.length === 0
        ? html`<paper-card>
            <div class="card-content">
              <p>
                Breaking changes for ${this._version} not found, try another.
              </p>
            </div>
          </paper-card>`
        : this._changes
            .sort((a, b) => {
              return a.homeassistant > b.homeassistant ? 1 : -1;
            })
            .map(
              (change) =>
                html`<paper-card>
                  <div class="card-content">
                    <h2>
                      ${this._version.includes('-')
                        ? html`0.${change.homeassistant}`
                        : ''}
                      ${change.title}
                    </h2>
                    <p>${change.description}</p>
                  </div>
                  <div class="card-actions">
                    <a
                      href="${change.doclink}"
                      target="_blank"
                      referrerpolicy="no-referrer"
                    >
                      <mwc-button>Documentation</mwc-button>
                    </a>
                    <a
                      href="${change.prlink}"
                      target="_blank"
                      referrerpolicy="no-referrer"
                    >
                      <mwc-button>Pull Request</mwc-button>
                    </a>
                  </div>
                </paper-card>`,
            )}
    </div>`;
  }

  private _changePage(page: string): void {
    this.dispatchEvent(
      new CustomEvent('set-page', {
        detail: {
          page,
        },
        bubbles: true,
        composed: true,
      }),
    );
  }

  static get styles() {
    return [
      Style,
      css`
        h2 {
          margin-block-start: 0;
          margin-block-end: 0;
        }
        .header {
          display: flex;
          align-items: center;
        }
      `,
    ];
  }
}
