function normalizeText(value) {
  return typeof value === 'string' ? value.trim().toLowerCase() : '';
}

function normalizeAge(value) {
  if (typeof value !== 'number' && typeof value !== 'string') {
    return null;
  }

  if (typeof value === 'string' && value.trim() === '') {
    return null;
  }

  const age = Number(value);
  return Number.isFinite(age) && age >= 0 ? age : null;
}

function matchesAgeRange(ageValue, minAge, maxAge) {
  if (minAge === null && maxAge === null) {
    return true;
  }

  const age = normalizeAge(ageValue);
  return (
    age !== null &&
    (minAge === null || age >= minAge) &&
    (maxAge === null || age <= maxAge)
  );
}

function createEmptyPetFilters() {
  return {
    type: '',
    minAge: '',
    maxAge: '',
    location: '',
  };
}

function filterPets(pets, filters = {}) {
  if (!Array.isArray(pets)) {
    return [];
  }

  const safeFilters =
    filters !== null && typeof filters === 'object' ? filters : {};
  const type = normalizeText(safeFilters.type);
  const location = normalizeText(safeFilters.location);
  const minAge = normalizeAge(safeFilters.minAge);
  const maxAge = normalizeAge(safeFilters.maxAge);

  return pets.filter((pet) => {
    if (pet === null || typeof pet !== 'object') {
      return false;
    }

    if (type && normalizeText(pet.type) !== type) {
      return false;
    }

    if (location && !normalizeText(pet.location).includes(location)) {
      return false;
    }

    if (!matchesAgeRange(pet.age, minAge, maxAge)) {
      return false;
    }

    return true;
  });
}

const petFilters = { createEmptyPetFilters, filterPets };

if (typeof module === 'object' && module.exports) {
  module.exports = petFilters;
} else {
  globalThis.PetFilters = petFilters;
}
