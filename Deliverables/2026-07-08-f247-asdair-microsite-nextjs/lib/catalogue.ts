export type CatalogueItem = {
  id: string;
  category: string;
  name: string;
  defaultQuantity: number;
  note?: string;
};

export const catalogueItems: CatalogueItem[] = [
  { id: "cravendale-semi-milk", category: "Dairy and chilled", name: "Cravendale semi milk", defaultQuantity: 3 },
  { id: "semi-milk-for-frank", category: "Dairy and chilled", name: "Semi milk for Frank", defaultQuantity: 1, note: "six-pint pack" },
  { id: "double-gloucester-cheese", category: "Dairy and chilled", name: "Double Gloucester Cheese", defaultQuantity: 2 },
  { id: "lurpack-butter", category: "Dairy and chilled", name: "Lurpack butter", defaultQuantity: 2 },
  { id: "choc-yazoo", category: "Dairy and chilled", name: "Choc Yazoo", defaultQuantity: 2 },
  { id: "large-free-range-eggs", category: "Dairy and chilled", name: "Large free-range eggs", defaultQuantity: 1 },
  { id: "warburtons-danish", category: "Bakery", name: "Warburtons Danish", defaultQuantity: 2 },
  { id: "richmond-sausages", category: "Meat and meals", name: "Richmond sausages", defaultQuantity: 1 },
  { id: "lean-corned-beef", category: "Meat and meals", name: "Lean corned beef", defaultQuantity: 1 },
  { id: "pasta-cheese-leek-and-ham-ready-meal", category: "Meat and meals", name: "Pasta Cheese Leek and Ham ready meal", defaultQuantity: 4 },
  { id: "chips", category: "Meat and meals", name: "Chips", defaultQuantity: 1 },
  { id: "orange-lucozade-sport-4pk", category: "Drinks", name: "Orange Lucozade Sport 4pk", defaultQuantity: 2 },
  { id: "raspberry-lucozade-sport", category: "Drinks", name: "Raspberry Lucozade Sport", defaultQuantity: 1 },
  { id: "fruit-splits", category: "Cereals and snacks", name: "Fruit Splits", defaultQuantity: 1 },
  { id: "custard-and-jelly-pots", category: "Cereals and snacks", name: "Custard and Jelly pots", defaultQuantity: 1 },
  { id: "toffees", category: "Cereals and snacks", name: "Toffees", defaultQuantity: 2 },
  { id: "weetabix-protein", category: "Cereals and snacks", name: "Weetabix Protein", defaultQuantity: 1 },
  { id: "frosties", category: "Cereals and snacks", name: "Frosties", defaultQuantity: 1 },
  { id: "nescafe-azera-coffee", category: "Cereals and snacks", name: "Nescafe Azera coffee", defaultQuantity: 1 },
  { id: "picnic-bars", category: "Cereals and snacks", name: "Picnic Bars", defaultQuantity: 1 },
  { id: "tissues", category: "Toiletries and health", name: "Tissues", defaultQuantity: 1 },
  { id: "aquafresh-toothpaste", category: "Toiletries and health", name: "Aquafresh toothpaste", defaultQuantity: 1 },
  { id: "sure-deodorant-male", category: "Toiletries and health", name: "Sure deodorant male", defaultQuantity: 3 },
  { id: "sure-deodorant-female", category: "Toiletries and health", name: "Sure deodorant female", defaultQuantity: 1 },
  { id: "always-discreet-normal", category: "Toiletries and health", name: "Always Discreet normal", defaultQuantity: 1 },
  { id: "hay-fever-tablets", category: "Toiletries and health", name: "Hay fever tablets", defaultQuantity: 1 },
  { id: "heinz-tomato-sauce", category: "Cleaning and household", name: "Heinz tomato sauce", defaultQuantity: 1 },
  { id: "toilet-rolls", category: "Cleaning and household", name: "Toilet rolls", defaultQuantity: 1 },
  { id: "fairy-max", category: "Cleaning and household", name: "Fairy Max", defaultQuantity: 1 },
  { id: "lenor-outdoor", category: "Cleaning and household", name: "Lenor Outdoor", defaultQuantity: 1 },
  { id: "vanish-pink-tub", category: "Cleaning and household", name: "Vanish Pink tub", defaultQuantity: 1 },
  { id: "vanish-white-tub", category: "Cleaning and household", name: "Vanish White tub", defaultQuantity: 1 },
  { id: "bleach", category: "Cleaning and household", name: "Bleach", defaultQuantity: 1 },
  { id: "gourmet-cat-meat", category: "Pet food", name: "Gourmet cat meat", defaultQuantity: 3 },
];
