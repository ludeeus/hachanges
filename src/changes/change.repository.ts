import { Change } from './change.entity';
import { Repository, EntityRepository } from 'typeorm';

@EntityRepository(Change)
export class ChangeRepository extends Repository<Change> {
  async getChanges(ids: number[]): Promise<Change[]> {
    return this.find({
      where: {
        homeassistant: {
          $in: ids,
        },
      },
    });
  }
}
