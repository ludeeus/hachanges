import { Change } from './change.entity';
import { Repository, EntityRepository } from 'typeorm';
import { Logger } from '@nestjs/common';

@EntityRepository(Change)
export class ChangeRepository extends Repository<Change> {
  private logger = new Logger('ChangeRepository');

  async getChanges(from: number, to: number): Promise<Change[]> {
    const query = this.createQueryBuilder('change');

    if (from === to) {
      query.where('change.homeassistant = :from', {
        from,
      });
    } else {
      query.where('change.homeassistant BETWEEN :from AND :to', {
        from,
        to,
      });
    }

    try {
      const changes = await query.getMany();
      return changes;
    } catch (error) {
      this.logger.error(
        `Failed to get cahnges for changes for  '0.${from}.0-0.${to}.0'.`,
        error.stack,
      );
    }
    return [];
  }
}
