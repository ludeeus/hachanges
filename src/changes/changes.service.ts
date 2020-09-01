import { Injectable, Logger, ImATeapotException } from '@nestjs/common';
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

    if (range(versions[0], versions[1]).length > 10) {
      throw new ImATeapotException(
        'Ratelimit: You can only get 10 versions at a time',
      );
    }

    changes = await this.changeRepository.getChanges(versions[0], versions[1]);

    if (changes.length > 0) {
      this.logger.log(`Serving ${versions} from database`);
      return changes;
    }

    range(versions[0], versions[1]).forEach(async version => {
      const _changes = await this.changeRepository.getChanges(
        versions[0],
        versions[1],
      );

      if (_changes.length === 0) {
        await this.generateService.generateChanges(version);
      }
    });
    return changes;
  }
}
