import {
  BaseEntity,
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ObjectIdColumn,
} from 'typeorm';

@Entity()
export class Change extends BaseEntity {
  @ObjectIdColumn()
  _id: string;

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
