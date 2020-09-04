import { TypeOrmModuleOptions } from '@nestjs/typeorm';
import * as config from 'config';
import { Change } from 'src/changes/change.entity';

const dbConfig = config.get('db');

export const typeOrmConfig: TypeOrmModuleOptions = {
  type: dbConfig.type,
  url: dbConfig.url,
  useUnifiedTopology: true,
  entities: [Change],
};
