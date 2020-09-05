import { Injectable, Logger } from '@nestjs/common';
import { ChangeRepository } from './change.repository';
import { InjectRepository } from '@nestjs/typeorm';
import { Change } from './change.entity';
import { GenerateService } from './generate.service';

@Injectable()
export class ChangesService {
  constructor(
    @InjectRepository(ChangeRepository)
    private changeRepository: ChangeRepository,
    private generateService: GenerateService,
  ) {}

  private logger = new Logger('ChangesService');

  async getChanges(id: string): Promise<Change[]> {
    const versions = [];
    let changes: Change[] = [];

    const range = (start, end) =>
      Array.from(Array(end + 1).keys()).slice(start);

    if (id.includes('-')) {
      versions.push(Number(id.split('-')[0]));
      versions.push(Number(id.split('-')[1]));
    } else {
      versions.push(Number(id));
      versions.push(Number(id));
    }

    if (versions[0] > versions[1]) {
      // 0 should never be higher than 1
      this.logger.log(`${versions[0]} is newer than ${versions[1]}, skipping`);
      return changes;
    }

    changes = await this.changeRepository.getChanges(
      range(versions[0], versions[1]),
    );

    if (changes.length === 0) {
      const changeVersions = changes.map(change => change.homeassistant);
      range(versions[0], versions[1]).forEach(async version => {
        if (!changeVersions.includes(version)) {
          await this.generateService.generateChanges(version);
        }
      });
    }

    if (versions[0] == versions[1]) {
      this.logger.log(`Serving ${versions[0]}`);
    } else {
      this.logger.log(`Serving range ${versions[0]} - ${versions[1]}`);
    }
    return changes.map(change => {
      delete change['_id'];
      return change;
    });
  }
}
