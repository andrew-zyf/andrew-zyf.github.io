import { readFileSync, statSync } from 'node:fs';
import assert from 'node:assert/strict';

const root = new URL('../public/', import.meta.url);
const data = JSON.parse(readFileSync(new URL('people.json', root), 'utf8'));
assert.ok(data.count > 0, 'Unexpected collection size.');
assert.equal(data.layoutCapacity, Math.max(10, Math.ceil((data.count + 40) / 80) * 2) * 40 - 40);
assert.equal(data.count, data.profileFollowerCount, 'Retain the complete captured list.');
assert.equal(data.omittedSlots, data.layoutCapacity - data.count);
assert.equal(data.people.length, data.count);
assert.equal(new Set(data.people.map(p => p.handle.toLowerCase())).size, data.count);
assert.equal(data.atlasColumns, 40);
assert.equal(data.atlasRows, Math.ceil(data.count / data.atlasColumns));
assert.ok(Number.isFinite(Date.parse(data.capturedAt)));
for (const person of data.people) {
  assert.match(person.handle, /^[A-Za-z0-9_]{1,15}$/);
  assert.equal(person.profileUrl, `https://x.com/${person.handle}`);
  assert.equal(typeof person.displayName, 'string');
  assert.ok(person.displayName.length > 0);
  assert.equal(typeof person.bio, 'string');
  assert.ok(['available', 'empty', 'unavailable'].includes(person.bioStatus));
  assert.equal(person.bioStatus === 'available', person.bio.length > 0);
}
assert.ok(statSync(new URL('portraits.webp', root)).size > 0);
assert.equal(data.source, 'https://x.com/andrew_zyf/followers');
console.log(`Verified ${data.count} unique profile records; ${data.omittedSlots} unused layout slots remain empty.`);
