import { faker } from '@faker-js/faker';

export function fakeUsername() {
  const now = Date.now();
  const suf = now.toString(32);
  return `${faker.person.lastName()}_${suf}`;
}
