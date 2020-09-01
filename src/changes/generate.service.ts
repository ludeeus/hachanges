import {
  Injectable,
  Logger,
  InternalServerErrorException,
} from '@nestjs/common';
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

  private logger = new Logger('GenerateService');

  async generateChanges(id: number): Promise<void> {
    let url;
    if (id === 114) {
      url = 'https://www.home-assistant.io/blog/2020/08/12/release-114/';
    } else if (id === 113) {
      url = 'https://www.home-assistant.io/blog/2020/07/22/release-113/';
    } else {
      return;
    }
    const response = await fetch(url);
    const body = await response.text();
    await this._handleResponse(body, id);
  }

  private async _handleResponse(response: string, id: number) {
    this.logger.log(`Generating changes for 0.${id}.0`);
    const dom = await new JSDOM(response);

    const elements = dom.window.document.querySelectorAll('details');

    elements.forEach(async (element: HTMLDetailsElement) => {
      if (!element.textContent.includes('Click to see all changes!')) {
        await this._createChangeFromElement(element, id);
      }
    });
  }

  private async _createChangeFromElement(
    element: HTMLDetailsElement,
    id: number,
  ) {
    const change = new Change();
    let content = '';
    let integration = 'homeassistant';
    element.querySelectorAll('p').forEach(p => {
      if (p.innerHTML.includes('(<a href')) {
        const pullrequest = Number(p.innerHTML.match(/#(\d*)/)[1]);
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
      await change.save();
    } catch (error) {
      this.logger.error(
        `Failed to create new change. Data: ${JSON.stringify(change)}`,
        error.stack,
      );
      throw new InternalServerErrorException();
    }
  }
}
