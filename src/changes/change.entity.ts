import { BaseEntity, Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Change extends BaseEntity {
  @PrimaryGeneratedColumn()
  pull_request: number;

  @Column()
  title: string;

  @Column()
  integration: string;

  @Column()
  pull: number;

  @Column()
  component: string;

  @Column()
  doclink: string;

  @Column()
  prlink: string;

  @Column()
  homeassistant: number;

  @Column()
  description: string;
}
