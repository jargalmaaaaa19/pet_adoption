const petNames = [
  'Бороо',
  'Сондор',
  'Хөөрхөн',
  'Цасхан',
  'Мишээл',
  'Азтай',
  'Найр',
  'Эрдэнэ',
  'Тэмүүжин',
  'Цэцэг',
  'Торго',
  'Номин',
  'Сүүдэр',
  'Очир',
  'Зулаа',
  'Дөлгөөн',
  'Халиун',
  'Марал',
  'Амин',
  'Бамбар',
  'Сарнай',
  'Бяцхан',
  'Од',
  'Тайга',
  'Мөнхөө',
  'Туслах',
  'Хасар',
  'Тэнгэр',
  'Эгшиг',
  'Хөөрхөнөө',
];

const petTypes = [
  'Dog',
  'Cat',
  'Dog',
  'Rabbit',
  'Cat',
  'Dog',
  'Dog',
  'Cat',
  'Dog',
  'Rabbit',
];

const breedsByType = {
  Dog: ['Монголын эрлийз', 'Самоед', 'Лабрадор', 'Хаски', 'Померан'],
  Cat: [
    'Монголын богино үст',
    'Британийн богино үст',
    'Шотланд нугалаа чихт',
    'Сиам',
    'Перс',
  ],
  Rabbit: [
    'Нидерланд одой',
    'Рекс',
    'Ангор',
    'Арслан толгойт',
    'Монголын туулай',
  ],
};

const locations = [
  'Улаанбаатар',
  'Дархан',
  'Эрдэнэт',
  'Ховд',
  'Өмнөговь',
  'Сэлэнгэ',
  'Архангай',
  'Дорнод',
];

const origins = [
  'Асрамжийн төвөөс',
  'Сайн дурын асрагчаас',
  'Гэрийн үржүүлгээс',
  'Найзынхаа асрамжаас',
  'Гудамжнаас олж аварсан',
  'Эзэн нь нүүх болсон тул',
  'Орон нутгийн хамгаалах бүлгээс',
  'Малын эмнэлгийн түр асрамжаас',
];

const descriptions = {
  Dog: [
    'Найрсаг, тоглох дуртай. Шинэ гэр бүлээ хүлээж байна.',
    'Ухаалаг, алхах дуртай, халамжтай эзэн хайж байна.',
    'Эрч хүчтэй, гэр бүлтэй хурдан дасдаг нохой.',
    'Тайван зантай, өдөр тутмын алхалтад дуртай.',
  ],
  Cat: [
    'Тайван зантай, гэрт дассан өхөөрдөм муур.',
    'Хүмүүстэй хурдан дасдаг, дөлгөөн муур.',
    'Сониуч, цэвэрч, дулаан гэр бүл хайж байна.',
    'Иллэг, тоглоомд дуртай эелдэг муур.',
  ],
  Rabbit: [
    'Зөөлөн үстэй, арчилгаа сайтай туулай.',
    'Тайван, цэвэрч бөгөөд гэрийн орчинд дассан.',
    'Сониуч зантай, шинэ орчинд хурдан дасна.',
    'Өдөр тутмын анхаарал халамжид дуртай туулай.',
  ],
};

function generateDemoPets(count = 120) {
  if (!Number.isInteger(count) || count < 0) {
    return [];
  }

  return Array.from({ length: count }, (_, index) => {
    const type = petTypes[index % petTypes.length];
    const nameIndex = index % petNames.length;
    const nameVersion = Math.floor(index / petNames.length);
    const listingType = index % 5 === 1 ? 'sale' : 'adoption';
    const pet = {
      id: index + 1,
      name: `${petNames[nameIndex]}${nameVersion ? ` ${nameVersion + 1}` : ''}`,
      type,
      breed: breedsByType[type][Math.floor(index / 2) % breedsByType[type].length],
      age: (index % 12) + 1,
      location: locations[Math.floor(index / 3) % locations.length],
      origin: origins[Math.floor(index / 4) % origins.length],
      listingType,
      description:
        descriptions[type][Math.floor(index / 2) % descriptions[type].length],
    };

    if (listingType === 'sale') {
      const startingPrice =
        type === 'Rabbit' ? 180000 : type === 'Cat' ? 350000 : 400000;
      pet.price = startingPrice + (index % 9) * 50000;
    }

    return pet;
  });
}

const demoPetListings = { generateDemoPets };

if (typeof module === 'object' && module.exports) {
  module.exports = demoPetListings;
} else {
  globalThis.DemoPetListings = demoPetListings;
}
