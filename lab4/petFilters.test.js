const { createEmptyPetFilters, filterPets } = require('./petFilters');

const pets = [
  { id: 1, name: 'Luna', type: 'Dog', age: 2, location: 'Ulaanbaatar' },
  { id: 2, name: 'Milo', type: 'Cat', age: 5, location: 'Darkhan' },
  { id: 3, name: 'Nala', type: 'Dog', age: 7, location: 'Ulaanbaatar' },
  { id: 4, name: 'Pip', type: 'Cat', age: 1, location: 'Erdenet' },
];

describe('filterPets', () => {
  test('filters by animal type without regard to letter case', () => {
    expect(filterPets(pets, { type: 'dog' }).map((pet) => pet.id)).toEqual([
      1, 3,
    ]);
  });

  test('filters by an inclusive age range', () => {
    expect(
      filterPets(pets, { minAge: '2', maxAge: '5' }).map((pet) => pet.id),
    ).toEqual([1, 2]);
  });

  test('filters by a case-insensitive partial location', () => {
    expect(filterPets(pets, { location: 'ULAA' }).map((pet) => pet.id)).toEqual([
      1, 3,
    ]);
  });

  test('combines animal type, age, and location filters', () => {
    expect(
      filterPets(pets, {
        type: 'dog',
        minAge: 2,
        maxAge: 3,
        location: 'ulaan',
      }).map((pet) => pet.id),
    ).toEqual([1]);
  });

  test('returns no pets when no listings match', () => {
    expect(filterPets(pets, { type: 'rabbit' })).toEqual([]);
  });

  test('returns every listing when filters are empty or missing', () => {
    expect(filterPets(pets, {})).toEqual(pets);
    expect(filterPets(pets)).toEqual(pets);
  });

  test('provides an empty filter object for resetting filters', () => {
    expect(createEmptyPetFilters()).toEqual({
      type: '',
      minAge: '',
      maxAge: '',
      location: '',
    });
    expect(filterPets(pets, createEmptyPetFilters())).toEqual(pets);
  });

  test('ignores invalid filter values and safely handles invalid listing input', () => {
    expect(
      filterPets(pets, {
        type: 42,
        minAge: 'not-an-age',
        maxAge: -1,
        location: null,
      }),
    ).toEqual(pets);
    expect(filterPets(null, {})).toEqual([]);
  });

  test('does not include listings with missing or invalid ages in an age range', () => {
    const incompleteListings = [
      { id: 1, age: 3 },
      { id: 2, age: 'not-an-age' },
      { id: 3 },
      null,
    ];

    expect(filterPets(incompleteListings, { minAge: 2 }).map((pet) => pet.id))
      .toEqual([1]);
  });
});
