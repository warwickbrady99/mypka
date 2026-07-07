// businessOsDb.js - local writeable MVP store for the hat Business OS.
//
// This module uses the cockpit-owned mypka-cockpit.db, not mypka.db. The main
// mypka.db remains a regenerated read-only mirror of markdown.
import Database from 'better-sqlite3';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BUSINESS_DB_PATH = path.resolve(__dirname, '..', 'mypka-cockpit.db');

const db = new Database(BUSINESS_DB_PATH);
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

function nowIso() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

function migrate() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS hat_suppliers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      contact_name TEXT,
      email TEXT,
      website_url TEXT,
      supplier_type TEXT NOT NULL DEFAULT 'unknown',
      notes TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS hat_designs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      hat_colour TEXT NOT NULL,
      logo_idea TEXT NOT NULL,
      front_design TEXT,
      side_back_design TEXT,
      target_customer TEXT,
      status TEXT NOT NULL DEFAULT 'idea',
      notes TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS hat_products (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      sku TEXT,
      design_id INTEGER,
      supplier_id INTEGER,
      ecommerce_product_url TEXT,
      selling_price REAL NOT NULL DEFAULT 0,
      status TEXT NOT NULL DEFAULT 'draft',
      notes TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      FOREIGN KEY (design_id) REFERENCES hat_designs(id) ON DELETE SET NULL,
      FOREIGN KEY (supplier_id) REFERENCES hat_suppliers(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS hat_product_costs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      product_id INTEGER NOT NULL UNIQUE,
      blank_cap_cost REAL NOT NULL DEFAULT 0,
      decoration_cost REAL NOT NULL DEFAULT 0,
      packaging_cost REAL NOT NULL DEFAULT 0,
      inbound_shipping_cost REAL NOT NULL DEFAULT 0,
      payment_platform_fee REAL NOT NULL DEFAULT 0,
      other_cost REAL NOT NULL DEFAULT 0,
      notes TEXT,
      updated_at TEXT NOT NULL,
      FOREIGN KEY (product_id) REFERENCES hat_products(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS hat_stock (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      product_id INTEGER NOT NULL UNIQUE,
      quantity_on_hand INTEGER NOT NULL DEFAULT 0,
      quantity_reserved INTEGER NOT NULL DEFAULT 0,
      reorder_level INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL,
      FOREIGN KEY (product_id) REFERENCES hat_products(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS hat_orders (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      product_id INTEGER NOT NULL,
      customer_label TEXT,
      quantity INTEGER NOT NULL DEFAULT 1,
      sell_price_each REAL NOT NULL DEFAULT 0,
      status TEXT NOT NULL DEFAULT 'enquiry',
      order_date TEXT NOT NULL,
      notes TEXT,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      FOREIGN KEY (product_id) REFERENCES hat_products(id) ON DELETE CASCADE
    );
  `);

  seedIfEmpty();
}

function seedIfEmpty() {
  const row = db.prepare(`SELECT COUNT(*) AS count FROM hat_designs`).get();
  if (row.count > 0) return;

  const ts = nowIso();
  const insertSupplier = db.prepare(`
    INSERT INTO hat_suppliers
      (name, contact_name, email, website_url, supplier_type, notes, created_at, updated_at)
    VALUES
      (@name, @contact_name, @email, @website_url, @supplier_type, @notes, @created_at, @updated_at)
  `);
  const insertDesign = db.prepare(`
    INSERT INTO hat_designs
      (name, hat_colour, logo_idea, front_design, side_back_design, target_customer, status, notes, created_at, updated_at)
    VALUES
      (@name, @hat_colour, @logo_idea, @front_design, @side_back_design, @target_customer, @status, @notes, @created_at, @updated_at)
  `);
  const insertProduct = db.prepare(`
    INSERT INTO hat_products
      (name, sku, design_id, supplier_id, ecommerce_product_url, selling_price, status, notes, created_at, updated_at)
    VALUES
      (@name, @sku, @design_id, @supplier_id, @ecommerce_product_url, @selling_price, @status, @notes, @created_at, @updated_at)
  `);
  const insertCosts = db.prepare(`
    INSERT INTO hat_product_costs
      (product_id, blank_cap_cost, decoration_cost, packaging_cost, inbound_shipping_cost, payment_platform_fee, other_cost, notes, updated_at)
    VALUES
      (@product_id, @blank_cap_cost, @decoration_cost, @packaging_cost, @inbound_shipping_cost, @payment_platform_fee, @other_cost, @notes, @updated_at)
  `);
  const insertStock = db.prepare(`
    INSERT INTO hat_stock
      (product_id, quantity_on_hand, quantity_reserved, reorder_level, updated_at)
    VALUES
      (@product_id, @quantity_on_hand, @quantity_reserved, @reorder_level, @updated_at)
  `);
  const insertOrder = db.prepare(`
    INSERT INTO hat_orders
      (product_id, customer_label, quantity, sell_price_each, status, order_date, notes, created_at, updated_at)
    VALUES
      (@product_id, @customer_label, @quantity, @sell_price_each, @status, @order_date, @notes, @created_at, @updated_at)
  `);

  const seed = db.transaction(() => {
    const supplier = insertSupplier.run({
      name: 'Supplier to confirm',
      contact_name: '',
      email: '',
      website_url: '',
      supplier_type: 'placeholder',
      notes: 'Dad/adult support should confirm suppliers before any order.',
      created_at: ts,
      updated_at: ts,
    }).lastInsertRowid;

    const designs = [
      {
        name: 'Black Everyday Training Cap',
        hat_colour: 'Black',
        logo_idea: 'Small white initials or original symbol',
        front_design: 'Small centre-front logo',
        side_back_design: 'Tiny wordmark on back strap or left side',
        target_customer: 'Gym, football training, and casual activewear',
      },
      {
        name: 'Grey Runner Cap',
        hat_colour: 'Grey',
        logo_idea: 'Small dark line mark or initials',
        front_design: 'Small front-left or centre logo',
        side_back_design: 'Optional simple reflective-style side detail',
        target_customer: 'Runners, walkers, and outdoor training',
      },
      {
        name: 'Navy Football Training Cap',
        hat_colour: 'Navy',
        logo_idea: 'White or light grey initials or simple badge shape',
        front_design: 'Small badge-style front logo',
        side_back_design: 'Optional small brand name on back',
        target_customer: 'Football players, coaches, and training outfits',
      },
    ];

    const designIds = designs.map((design) => insertDesign.run({
      ...design,
      status: 'idea',
      notes: 'Starter MVP record from first 5 hat design ideas.',
      created_at: ts,
      updated_at: ts,
    }).lastInsertRowid);

    const productIds = [
      {
        name: 'Black Everyday Training Cap',
        sku: 'HAT-BLK-001',
        design_id: designIds[0],
        selling_price: 18,
      },
      {
        name: 'Grey Runner Cap',
        sku: 'HAT-GRY-001',
        design_id: designIds[1],
        selling_price: 18,
      },
      {
        name: 'Navy Football Training Cap',
        sku: 'HAT-NVY-001',
        design_id: designIds[2],
        selling_price: 18,
      },
    ].map((product) => insertProduct.run({
      ...product,
      supplier_id: supplier,
      ecommerce_product_url: '',
      status: 'draft',
      notes: 'Add the live product page URL when the ecommerce site exists.',
      created_at: ts,
      updated_at: ts,
    }).lastInsertRowid);

    for (const product_id of productIds) {
      insertCosts.run({
        product_id,
        blank_cap_cost: 5,
        decoration_cost: 3,
        packaging_cost: 1,
        inbound_shipping_cost: 1,
        payment_platform_fee: 1,
        other_cost: 0,
        notes: 'Placeholder estimate only. Replace with real costs before selling.',
        updated_at: ts,
      });
      insertStock.run({
        product_id,
        quantity_on_hand: 0,
        quantity_reserved: 0,
        reorder_level: 5,
        updated_at: ts,
      });
    }

    insertOrder.run({
      product_id: productIds[0],
      customer_label: 'Example local feedback/pre-order',
      quantity: 1,
      sell_price_each: 18,
      status: 'enquiry',
      order_date: ts.slice(0, 10),
      notes: 'Example only. Replace with a real order when ready.',
      created_at: ts,
      updated_at: ts,
    });
  });

  seed();
}

migrate();

const overviewStmt = db.prepare(`
  SELECT
    p.id,
    p.name,
    p.sku,
    p.ecommerce_product_url AS ecommerceProductUrl,
    p.selling_price AS sellingPrice,
    p.status,
    p.notes,
    d.name AS designName,
    d.hat_colour AS hatColour,
    d.logo_idea AS logoIdea,
    s.name AS supplierName,
    c.blank_cap_cost AS blankCapCost,
    c.decoration_cost AS decorationCost,
    c.packaging_cost AS packagingCost,
    c.inbound_shipping_cost AS inboundShippingCost,
    c.payment_platform_fee AS paymentPlatformFee,
    c.other_cost AS otherCost,
    st.quantity_on_hand AS quantityOnHand,
    st.quantity_reserved AS quantityReserved,
    st.reorder_level AS reorderLevel
  FROM hat_products p
  LEFT JOIN hat_designs d ON d.id = p.design_id
  LEFT JOIN hat_suppliers s ON s.id = p.supplier_id
  LEFT JOIN hat_product_costs c ON c.product_id = p.id
  LEFT JOIN hat_stock st ON st.product_id = p.id
  ORDER BY p.id
`);

const designsStmt = db.prepare(`
  SELECT id, name, hat_colour AS hatColour, logo_idea AS logoIdea,
    front_design AS frontDesign, side_back_design AS sideBackDesign,
    target_customer AS targetCustomer, status, notes
  FROM hat_designs
  ORDER BY id
`);

const suppliersStmt = db.prepare(`
  SELECT id, name, contact_name AS contactName, email, website_url AS websiteUrl,
    supplier_type AS supplierType, notes
  FROM hat_suppliers
  ORDER BY id
`);

const ordersStmt = db.prepare(`
  SELECT o.id, o.product_id AS productId, p.name AS productName, o.customer_label AS customerLabel,
    o.quantity, o.sell_price_each AS sellPriceEach, o.status, o.order_date AS orderDate, o.notes
  FROM hat_orders o
  JOIN hat_products p ON p.id = o.product_id
  ORDER BY o.order_date DESC, o.id DESC
`);

function num(v) {
  return typeof v === 'number' && Number.isFinite(v) ? v : 0;
}

export function getBusinessOsOverview() {
  const products = overviewStmt.all().map((p) => {
    const unitCost =
      num(p.blankCapCost) +
      num(p.decorationCost) +
      num(p.packagingCost) +
      num(p.inboundShippingCost) +
      num(p.paymentPlatformFee) +
      num(p.otherCost);
    const profitEach = num(p.sellingPrice) - unitCost;
    const marginPercent = num(p.sellingPrice) > 0 ? (profitEach / num(p.sellingPrice)) * 100 : 0;
    const availableStock = Math.max(0, num(p.quantityOnHand) - num(p.quantityReserved));
    return {
      ...p,
      unitCost,
      profitEach,
      marginPercent,
      availableStock,
    };
  });

  const orders = ordersStmt.all();
  return {
    ok: true,
    generatedAt: nowIso(),
    products,
    designs: designsStmt.all(),
    suppliers: suppliersStmt.all(),
    orders,
    totals: {
      products: products.length,
      designs: designsStmt.all().length,
      suppliers: suppliersStmt.all().length,
      availableStock: products.reduce((sum, p) => sum + p.availableStock, 0),
      openOrders: orders.filter((o) => ['enquiry', 'pending', 'paid'].includes(o.status)).length,
      estimatedProfitIfSold: products.reduce((sum, p) => sum + p.profitEach * p.availableStock, 0),
    },
  };
}

export { BUSINESS_DB_PATH };
