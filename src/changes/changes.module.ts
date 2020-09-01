import { Module } from '@nestjs/common';
import { ChangesService } from './changes.service';
import { ChangesController } from './changes.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ChangeRepository } from './change.repository';
import { GenerateService } from './generate.service';

@Module({
  imports: [TypeOrmModule.forFeature([ChangeRepository])],
  providers: [ChangesService, GenerateService],
  controllers: [ChangesController],
})
export class ChangesModule {}
