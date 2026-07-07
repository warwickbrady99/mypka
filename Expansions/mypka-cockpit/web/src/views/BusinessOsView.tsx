import { AlertCircle, ArrowUpRight, Boxes, Calculator, PackageCheck, Store } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { PageHeader } from '../components/PageHeader';
import { useFetch } from '../lib/useCockpit';
import './business-os.css';

interface Product {
  id: number;
  name: string;
  sku: string | null;
  ecommerceProductUrl: string | null;
  sellingPrice: number;
  status: string;
  designName: string | null;
  hatColour: string | null;
  logoIdea: string | null;
  supplierName: string | null;
  blankCapCost: number;
  decorationCost: number;
  packagingCost: number;
  inboundShippingCost: number;
  paymentPlatformFee: number;
  otherCost: number;
  quantityOnHand: number;
  quantityReserved: number;
  reorderLevel: number;
  unitCost: number;
  profitEach: number;
  marginPercent: number;
  availableStock: number;
}

interface Design {
  id: number;
  name: string;
  hatColour: string;
  logoIdea: string;
  targetCustomer: string | null;
  status: string;
}

interface Supplier {
  id: number;
  name: string;
  supplierType: string;
  websiteUrl: string | null;
  notes: string | null;
}

interface Order {
  id: number;
  productName: string;
  customerLabel: string | null;
  quantity: number;
  sellPriceEach: number;
  status: string;
  orderDate: string;
}

interface BusinessOsOverview {
  ok: boolean;
  generatedAt: string;
  products: Product[];
  designs: Design[];
  suppliers: Supplier[];
  orders: Order[];
  totals: {
    products: number;
    designs: number;
    suppliers: number;
    availableStock: number;
    openOrders: number;
    estimatedProfitIfSold: number;
  };
}

const money = new Intl.NumberFormat('en-GB', {
  style: 'currency',
  currency: 'GBP',
  maximumFractionDigits: 2,
});

function fmtMoney(value: number): string {
  return money.format(Number.isFinite(value) ? value : 0);
}

function fmtPercent(value: number): string {
  return `${Math.round((Number.isFinite(value) ? value : 0) * 10) / 10}%`;
}

export function BusinessOsView() {
  const { data, loading, error } = useFetch<BusinessOsOverview>('/api/business-os/overview');

  return (
    <section className="business-os-view animate-fade-rise">
      <PageHeader
        title="Hat Business OS"
        icon={Store}
        subtitle="A simple admin dashboard for products, designs, suppliers, costs, stock, orders, and live product page links."
      />

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      {data && (
        <main className="bos-main">
          <section className="bos-summary-grid" aria-label="Business summary">
            <SummaryCard label="Products" value={String(data.totals.products)} icon={PackageCheck} />
            <SummaryCard label="Designs" value={String(data.totals.designs)} icon={Store} />
            <SummaryCard label="Available stock" value={String(data.totals.availableStock)} icon={Boxes} />
            <SummaryCard label="Profit if stock sells" value={fmtMoney(data.totals.estimatedProfitIfSold)} icon={Calculator} />
          </section>

          <section className="bos-panel">
            <div className="bos-panel-head">
              <div>
                <h2 className="bos-panel-title">Products And Profit</h2>
                <p className="bos-panel-sub">Each card includes the live website URL field and a simple per-product profit calculator.</p>
              </div>
            </div>
            <div className="bos-product-grid">
              {data.products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </section>

          <section className="bos-two-col">
            <div className="bos-panel">
              <h2 className="bos-panel-title">Designs</h2>
              <div className="bos-table-wrap">
                <table className="bos-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Colour</th>
                      <th>Logo idea</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.designs.map((design) => (
                      <tr key={design.id}>
                        <td>{design.name}</td>
                        <td>{design.hatColour}</td>
                        <td>{design.logoIdea}</td>
                        <td>{design.status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="bos-panel">
              <h2 className="bos-panel-title">Suppliers</h2>
              <div className="bos-list">
                {data.suppliers.map((supplier) => (
                  <div className="bos-list-row" key={supplier.id}>
                    <div>
                      <p className="bos-row-title">{supplier.name}</p>
                      <p className="bos-row-sub">{supplier.supplierType}</p>
                    </div>
                    {supplier.websiteUrl ? (
                      <a className="bos-link" href={supplier.websiteUrl} target="_blank" rel="noreferrer">
                        Open <ArrowUpRight size={14} strokeWidth={1.5} aria-hidden="true" />
                      </a>
                    ) : (
                      <span className="bos-muted">Not chosen</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="bos-panel">
            <h2 className="bos-panel-title">Orders</h2>
            <div className="bos-table-wrap">
              <table className="bos-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Product</th>
                    <th>Customer</th>
                    <th>Qty</th>
                    <th>Status</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {data.orders.map((order) => (
                    <tr key={order.id}>
                      <td>{order.orderDate}</td>
                      <td>{order.productName}</td>
                      <td>{order.customerLabel || 'TBC'}</td>
                      <td>{order.quantity}</td>
                      <td>{order.status}</td>
                      <td>{fmtMoney(order.quantity * order.sellPriceEach)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </main>
      )}
    </section>
  );
}

function ProductCard({ product }: { product: Product }) {
  const stockTone = product.availableStock <= product.reorderLevel ? 'is-low' : 'is-ok';
  return (
    <article className="bos-product-card">
      <div className="bos-product-head">
        <div>
          <h3 className="bos-product-title">{product.name}</h3>
          <p className="bos-row-sub">{product.sku || 'No SKU yet'} · {product.status}</p>
        </div>
        <span className={`bos-stock-pill ${stockTone}`}>{product.availableStock} available</span>
      </div>

      <dl className="bos-facts">
        <div>
          <dt>Design</dt>
          <dd>{product.designName || 'Not linked'}</dd>
        </div>
        <div>
          <dt>Colour</dt>
          <dd>{product.hatColour || 'TBC'}</dd>
        </div>
        <div>
          <dt>Supplier</dt>
          <dd>{product.supplierName || 'TBC'}</dd>
        </div>
      </dl>

      <div className="bos-profit-box">
        <div>
          <span className="bos-profit-label">Selling price</span>
          <strong>{fmtMoney(product.sellingPrice)}</strong>
        </div>
        <div>
          <span className="bos-profit-label">Unit cost</span>
          <strong>{fmtMoney(product.unitCost)}</strong>
        </div>
        <div className="bos-profit-total">
          <span className="bos-profit-label">Profit each</span>
          <strong>{fmtMoney(product.profitEach)}</strong>
          <small>{fmtPercent(product.marginPercent)} margin</small>
        </div>
      </div>

      <div className="bos-cost-list" aria-label="Cost breakdown">
        <span>Blank {fmtMoney(product.blankCapCost)}</span>
        <span>Decoration {fmtMoney(product.decorationCost)}</span>
        <span>Packaging {fmtMoney(product.packagingCost)}</span>
        <span>Shipping {fmtMoney(product.inboundShippingCost)}</span>
        <span>Fees {fmtMoney(product.paymentPlatformFee)}</span>
      </div>

      <div className="bos-product-link">
        <span>Live product page</span>
        {product.ecommerceProductUrl ? (
          <a href={product.ecommerceProductUrl} target="_blank" rel="noreferrer">
            Open page <ArrowUpRight size={14} strokeWidth={1.5} aria-hidden="true" />
          </a>
        ) : (
          <strong>Add URL when website is live</strong>
        )}
      </div>
    </article>
  );
}

function SummaryCard({ label, value, icon: Icon }: { label: string; value: string; icon: LucideIcon }) {
  return (
    <article className="bos-summary-card">
      <Icon size={18} strokeWidth={1.5} aria-hidden="true" className="bos-summary-icon" />
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function LoadingState() {
  return (
    <div className="bos-loading" aria-busy="true" aria-live="polite">
      <div />
      <div />
      <div />
    </div>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <div role="alert" className="bos-error">
      <AlertCircle size={20} strokeWidth={1.5} aria-hidden="true" />
      <div>
        <p>Could not load the Business OS</p>
        <span>{message}</span>
      </div>
    </div>
  );
}
