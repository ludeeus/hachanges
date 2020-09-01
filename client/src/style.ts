import { css } from 'lit-element';

export const Style = css`
  :host {
    --theme-color: #03a9f4;
    --theme-color-error: #cf1919;
    --theme-accent-color: #ff9800;
    --mdc-theme-primary: var(--theme-accent-color);
    --theme-background-color-card: #1c1c1c;
    --theme-background-color: #111111;
    --text-primary-color: #ffffff;
    --primary-text-color: var(--text-primary-color);
    --secondary-text-color: #727272;
    --paper-card-header-color: var(--text-primary-color);
    --paper-item-body-secondary-color: var(--text-primary-color);
  }
  .header {
    padding: 12px;
  }
  .subheader {
    padding: 0 8px;
  }
  .back {
    position: absolute;
    top: 0;
    left: 4px;
  }
  .error {
    color: var(--theme-color-error);
  }
  iron-icon {
    --iron-icon-width: 42px;
    --iron-icon-height: 42px;
    margin-right: 12px;
  }
  iron-icon,
  .back,
  .description,
  .next,
  .footer {
    color: var(--paper-item-body-secondary-color, var(--secondary-text-color));
  }
  paper-item iron-icon {
    color: var(--theme-color);
    opacity: 0.7;
  }
  .dpendencies,
  .header,
  .subheader {
    opacity: 0.75;
  }
  paper-item,
  .back {
    cursor: pointer;
  }
  a {
    color: var(--theme-color);
    text-decoration: none;
  }
  .content {
    margin: auto;
    width: 75%;
    max-width: 600px;
    height: calc(100vh - 40px);
    font-family: Roboto, 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: var(--primary-text-color);
  }
  paper-card {
    width: 100%;
    margin: auto;
    margin-bottom: 16px;
    border-radius: 10px;
    opacity: 0.9;
    background-color: var(--theme-background-color-card);
  }
  mwc-button {
    --mdc-theme-primary: var(--theme-accent-color);
  }
  pre {
    padding: 0 8px 8px;
    white-space: pre-line;
  }
  @media only screen and (max-width: 600px) {
    .content {
      width: 100%;
      max-width: 90%;
    }
  }
`;
