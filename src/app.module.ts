import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { typeOrmConfig } from './config/typeorm.config';
import { ChangesModule } from './changes/changes.module';
import { join } from 'path';
import { ServeStaticModule } from '@nestjs/serve-static';

const rootPath =
  process.env.NODE_ENV === 'production'
    ? join(__dirname, '..', '..', 'client', 'build')
    : join(__dirname, '..', 'client', 'build');

@Module({
  imports: [
    ServeStaticModule.forRoot({
      rootPath,
      exclude: ['/*/json'],
    }),
    TypeOrmModule.forRoot(typeOrmConfig),
    ChangesModule,
  ],
})
export class AppModule {}
