import { Controller, Get, Param } from '@nestjs/common';
import { ChangesService } from './changes.service';
import { Change } from './change.entity';

@Controller()
export class ChangesController {
  constructor(private changesService: ChangesService) {}

  @Get('/:id/json')
  getChanges(@Param('id') id: string): Promise<Change[]> {
    return this.changesService.getChanges(id);
  }
}
