import Dexie, { type Table } from 'dexie';
export interface User {
  uuid: string;
  name: string;
  ctime: number;
  mtime: number;
}

export interface Score {
  uuid: string;
  score: number;
  link?: string;
  ctime: number;
  mtime: number;
}

export class ScoreDB extends Dexie {
  user!: Table<User>;
  scoreboard!: Table<Score>;

  constructor() {
    super('scores');
    this.version(1).stores({
      user: 'uuid, name, ctime, mtime',
      scoreboard: 'uuid, score, link, ctime, mtime',
    });
  }
}

export const db = new ScoreDB();

export function getUser() {
  return db.user.toArray().then((d) => (d.length > 0 ? d[0] : null));
}

export function getScore(uuid: string) {
  return db.scoreboard
    .where('uuid')
    .equals(uuid)
    .toArray()
    .then((d) => (d.length > 0 ? d[0] : null));
}

export function updateScore(
  uuid: string,
  value: Partial<Omit<Score, 'ctime' | 'mtime' | 'uuid'>>
) {
  return db.scoreboard.where('uuid').equals(uuid).modify({
    link: value.link,
    score: value.score,
    mtime: Date.now(),
  });
}
