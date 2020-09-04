import { Injectable, Logger } from '@nestjs/common';
import { ChangeRepository } from './change.repository';
import { InjectRepository } from '@nestjs/typeorm';

import { JSDOM } from 'jsdom';
import * as fetch from 'node-fetch';
import { Change } from './change.entity';

@Injectable()
export class GenerateService {
  constructor(
    @InjectRepository(ChangeRepository)
    private changeRepository: ChangeRepository,
  ) {}

  private generated = [];

  private logger = new Logger('GenerateService');

  private async _getUrlFromSitemap(): Promise<any> {
    const url = 'https://www.home-assistant.io/sitemap.xml';
    const versions = {};

    const response = await fetch(url);
    const content = await response.text();
    const dom = await new JSDOM(content);

    const urls = dom.window.document.querySelectorAll('loc');
    urls.forEach(url => {
      const matches = url.textContent.match(/\/release-(\d*)\//);
      if (matches) {
        versions[matches[1]] = url.textContent;
      }
    });
    return versions;
  }

  private async _handleResponse(response: string, id: number) {
    const dom = await new JSDOM(response);

    const elements = dom.window.document.querySelectorAll('details');

    elements.forEach(async (element: HTMLDetailsElement) => {
      if (!element.textContent.includes('Click to see all changes!')) {
        await this._createChangeFromElement(element, id);
      }
    });
  }

  private async _handleLegacyResponse(response: string, id: number) {
    const dom = await new JSDOM(response);

    const elements = dom.window.document.querySelectorAll('li');

    elements.forEach(async (element: HTMLDetailsElement) => {
      if (
        element.innerHTML.includes('(breaking-change)') ||
        element.innerHTML.includes('(breaking change)')
      ) {
        await this._createLegacyChangeFromElement(element, id);
      }
    });
  }

  private async _createChangeFromElement(
    element: HTMLDetailsElement,
    id: number,
  ) {
    const change = new Change();
    let content = '';
    let pullrequest;
    let integration = 'homeassistant';
    element.querySelectorAll('p').forEach(p => {
      if (p.innerHTML.includes('(<a href')) {
        if (p.innerHTML.match(/#(\d*)/)) {
          pullrequest = Number(p.innerHTML.match(/#(\d*)/)[1]);
        }

        if (p.innerHTML.match(/\/integrations\/(\w*)/)) {
          integration = p.innerHTML.match(/\/integrations\/(\w*)/)[1];
        }
        change.pull = pullrequest;
        change.pull_request = pullrequest;
        change.integration = integration;
        change.component = integration;
      } else {
        content = content.concat(
          p.innerHTML
            .replace(/<code>/g, '`')
            .replace(/<\/code>/g, '`')
            .replace(/\n/g, ' '),
        );
      }
    });

    change.title = element.querySelector('b').textContent || 'homeassistant';
    change.homeassistant = id;
    change.description = content;
    change.doclink = `https://www.home-assistant.io/integrations/${change.integration}`;
    change.prlink = `https://github.com/home-assistant/core/pull/${change.pull}`;

    if (change.pull === undefined || change.integration === undefined) {
      return;
    }

    try {
      await this.changeRepository.save(change);
    } catch (error) {
      if (error.code === 'SQLITE_CONSTRAINT') {
        this.logger.log(`#${change.pull} allready exsist, skipping.`);
        return;
      }
      this.logger.error(
        `Failed to create new change. Input: ${JSON.stringify(
          element.innerHTML,
        )}, Output: ${JSON.stringify(change)}`,
        error.stack,
      );
    }
  }

  private async _createLegacyChangeFromElement(
    element: HTMLDetailsElement,
    id: number,
  ) {
    const change = new Change();
    let integration = 'homeassistant';
    let pull;
    if (element.innerHTML.match(/\/integrations\/(\w*)/)) {
      integration = element.innerHTML.match(/\/integrations\/(\w*)/)[1];
    }

    if (element.innerHTML.match(/#(\d*)/)) {
      pull = Number(element.innerHTML.match(/#(\d*)/)[1]);
    }

    change.title = integration;
    change.description = element.innerHTML
      .split(' (')[0]
      .replace(/<code>/g, '`')
      .replace(/<\/code>/g, '`')
      .replace(/\n/g, ' ');
    change.integration = integration;
    change.component = integration;
    change.pull = pull;
    change.pull_request = pull;
    change.homeassistant = id;
    change.doclink = `https://www.home-assistant.io/integrations/${change.integration}`;
    change.prlink = `https://github.com/home-assistant/core/pull/${change.pull}`;

    if (!change.pull) {
      return;
    }

    try {
      await change.save();
    } catch (error) {
      if (error.code === 'SQLITE_CONSTRAINT') {
        this.logger.log(`#${change.pull} allready exsist, skipping.`);
        return;
      }
      this.logger.error(
        `Failed to create new change. Input: ${JSON.stringify(
          element.innerHTML,
        )}, Output: ${JSON.stringify(change)}`,
        error.stack,
      );
    }
  }

  async generateChanges(id: number): Promise<void> {
    let body;
    const sitemap = await this._getUrlFromSitemap();
    if (!sitemap[id]) {
      this.logger.error(`No release found for '${id}'`);
      return;
    }

    if (id in this.generated) {
      return;
    }

    this.logger.log(`Generating changes for 0.${id}.0`);
    this.generated.push(id);

    try {
      const response = await fetch(sitemap[id]);
      body = await response.text();
    } catch (err) {
      this.generated = this.generated.filter(release => release !== id);
      return;
    }

    try {
      if (id >= 113) {
        await this._handleResponse(body, id);
      } else {
        await this._handleLegacyResponse(body, id);
      }
    } catch (err) {
      this.generated = this.generated.filter(release => release !== id);
      return;
    }
  }
}
