const { generateDemoPets } = require('./demoPetListings');
const { filterPets } = require('./petFilters');

describe('generateDemoPets', () => {
  test('creates more than 100 complete, uniquely identified demo listings', () => {
    const pets = generateDemoPets();

    expect(pets).toHaveLength(120);
    expect(new Set(pets.map((pet) => pet.id)).size).toBe(120);
    expect(
      pets.every(
        (pet) =>
          pet.name &&
          pet.type &&
          pet.breed &&
          Number.isFinite(pet.age) &&
          pet.location &&
          pet.locationDetail &&
          pet.origin &&
          pet.description,
      ),
    ).toBe(true);
  });

  test('includes adoption and sale listings with valid prices for sale posts', () => {
    const pets = generateDemoPets();
    const salePets = pets.filter((pet) => pet.listingType === 'sale');
    const adoptionPets = pets.filter((pet) => pet.listingType === 'adoption');

    expect(salePets.length).toBeGreaterThan(0);
    expect(adoptionPets.length).toBeGreaterThan(0);
    expect(salePets.every((pet) => Number.isFinite(pet.price) && pet.price > 0))
      .toBe(true);
    expect(adoptionPets.every((pet) => pet.price === undefined)).toBe(true);
  });

  test('can generate a requested number of listings', () => {
    expect(generateDemoPets(5)).toHaveLength(5);
    expect(generateDemoPets(0)).toEqual([]);
    expect(generateDemoPets(-1)).toEqual([]);
  });

  test('includes district or soum details across many Mongolian locations', () => {
    const pets = generateDemoPets();
    const locations = new Set(pets.map((pet) => pet.location));

    expect(locations.size).toBeGreaterThan(20);
    expect([...locations].every((location) => location.includes(', '))).toBe(
      true,
    );
    expect([...locations]).toContain('Улаанбаатар, Баянзүрх дүүрэг');
    expect([...locations]).toContain('Дархан-Уул аймаг, Дархан сум');
    expect(pets.some((pet) => pet.locationDetail.includes('хороо'))).toBe(true);
    expect(pets.some((pet) => pet.locationDetail.includes('баг'))).toBe(true);
  });

  test('finds a listing using its detailed district name', () => {
    const pets = generateDemoPets();

    expect(
      filterPets(pets, { location: 'БАЯНЗҮРХ' }).map((pet) => pet.id),
    ).toEqual([1, 2, 3, 97, 98, 99]);
  });

  test('finds a listing using its detailed neighborhood name', () => {
    const pets = generateDemoPets();

    expect(
      filterPets(pets, { location: 'олимп хотхон' }).map((pet) => pet.id),
    ).toEqual([1, 2, 3]);
  });
});
