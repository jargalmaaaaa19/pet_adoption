const { createEmptyPetFilters, filterPets } = require('./petFilters');

const pets = [
  {
    id: 1,
    name: 'Luna',
    type: 'Dog',
    breed: 'Golden Retriever',
    age: 2,
    location: 'Ulaanbaatar',
    origin: 'Local shelter',
    listingType: 'adoption',
  },
  {
    id: 2,
    name: 'Milo',
    type: 'Cat',
    breed: 'British Shorthair',
    age: 5,
    location: 'Darkhan',
    origin: 'Foster family',
    listingType: 'sale',
    price: 500000,
  },
  {
    id: 3,
    name: 'Nala',
    type: 'Dog',
    breed: 'Mongolian mixed breed',
    age: 7,
    location: 'Ulaanbaatar',
    origin: 'Rescue center',
    listingType: 'adoption',
  },
  {
    id: 4,
    name: 'Pip',
    type: 'Cat',
    breed: 'British Shorthair',
    age: 1,
    location: 'Erdenet',
    origin: 'Home-raised',
    listingType: 'sale',
    price: 650000,
  },
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

  test('filters by a case-insensitive partial breed', () => {
    expect(filterPets(pets, { breed: 'SHORTHAIR' }).map((pet) => pet.id)).toEqual([
      2, 4,
    ]);
  });

  test('filters adoption and sale listings by listing type', () => {
    expect(
      filterPets(pets, { listingType: 'sale' }).map((pet) => pet.id),
    ).toEqual([2, 4]);
  });

  test('combines breed and listing type filters', () => {
    expect(
      filterPets(pets, {
        breed: 'british',
        listingType: 'sale',
        minAge: 5,
      }).map((pet) => pet.id),
    ).toEqual([2]);
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
      breed: '',
      listingType: '',
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
        breed: 42,
        listingType: null,
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
