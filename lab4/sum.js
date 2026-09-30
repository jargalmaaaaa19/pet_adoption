function sum(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Тоо оруулах шаардлагатай!');
  }
  return a + b;
}
module.exports = sum;