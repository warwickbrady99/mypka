"use client";

import { FormEvent, useMemo, useState } from "react";
import type { CatalogueItem } from "../lib/catalogue";

type ShoppingPageProps = {
  accessToken: string;
  items: CatalogueItem[];
};

type SubmittedItem = {
  id: string;
  name: string;
  category: string;
  quantity: number;
  note?: string;
};

type SubmissionPreview = {
  items: SubmittedItem[];
  anythingElse: string;
};

type SubmitStatus =
  | { state: "idle"; message: string }
  | { state: "sending"; message: string }
  | { state: "success"; message: string; preview: SubmissionPreview }
  | { state: "error"; message: string };

function clampQuantity(value: number): number {
  if (!Number.isFinite(value) || value < 0) {
    return 0;
  }

  return Math.floor(value);
}

function buildInitialQuantities(items: CatalogueItem[]): Record<string, number> {
  return Object.fromEntries(items.map((item) => [item.id, item.defaultQuantity]));
}

export function ShoppingPage({ accessToken, items }: ShoppingPageProps) {
  const [quantities, setQuantities] = useState<Record<string, number>>(() =>
    buildInitialQuantities(items),
  );
  const [anythingElse, setAnythingElse] = useState("");
  const [submitStatus, setSubmitStatus] = useState<SubmitStatus>({ state: "idle", message: "" });

  const groupedItems = useMemo(() => {
    return items.reduce<Record<string, CatalogueItem[]>>((groups, item) => {
      groups[item.category] = groups[item.category] ?? [];
      groups[item.category].push(item);
      return groups;
    }, {});
  }, [items]);

  function updateQuantity(itemId: string, value: number) {
    setQuantities((current) => ({
      ...current,
      [itemId]: clampQuantity(value),
    }));
  }

  function resetToUsualShop() {
    setQuantities(buildInitialQuantities(items));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const selectedItems = items
      .map((item) => ({
        id: item.id,
        name: item.name,
        category: item.category,
        quantity: clampQuantity(quantities[item.id] ?? 0),
        note: item.note,
      }))
      .filter((item) => item.quantity > 0);

    const preview = {
      items: selectedItems,
      anythingElse: anythingElse.trim(),
    };

    setSubmitStatus({ state: "sending", message: "Sending the shopping list to Warwick..." });

    try {
      const response = await fetch("/api/shopping-list", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          accessToken,
          items: selectedItems.map((item) => ({ id: item.id, quantity: item.quantity })),
          anythingElse: preview.anythingElse,
        }),
      });

      const result = (await response.json()) as { message?: string };

      if (!response.ok) {
        throw new Error(result.message || "The shopping list could not be sent.");
      }

      setSubmitStatus({
        state: "success",
        message: result.message || "Thanks, the shopping list has been sent to Warwick.",
        preview,
      });
    } catch (error) {
      setSubmitStatus({
        state: "error",
        message:
          error instanceof Error
            ? error.message
            : "Sorry, the shopping list could not be sent just now. Please try again in a minute.",
      });
    }
  }

  if (submitStatus.state === "success") {
    return (
      <section className="shopping-panel confirmation-panel" aria-labelledby="page-title">
        <h1 id="page-title">Shopping list sent.</h1>
        <p>{submitStatus.message}</p>

        {submitStatus.preview.items.length > 0 ? (
          <div className="confirmation-note">
            <h2>Items included</h2>
            <ul className="summary-list">
              {submitStatus.preview.items.map((item) => (
                <li key={item.id}>
                  <span>{item.name}</span>
                  <span className="quantity">x{item.quantity}</span>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <p className="empty-message">No item quantities were selected.</p>
        )}

        {submitStatus.preview.anythingElse ? (
          <div className="confirmation-note">
            <h2>Anything else?</h2>
            <p>{submitStatus.preview.anythingElse}</p>
          </div>
        ) : null}

        <div className="confirmation-note">
          <h2>Safety boundary</h2>
          <p>This is a shopping request only. Warwick remains responsible for final checkout.</p>
        </div>

        <button className="link-button" type="button" onClick={() => setSubmitStatus({ state: "idle", message: "" })}>
          Back to Mum's Shopping
        </button>
      </section>
    );
  }

  return (
    <section className="shopping-panel" aria-labelledby="page-title">
      <h1 id="page-title">Mum's Shopping</h1>
      <p>Change anything different this week, then send it to Warwick.</p>

      <form className="shopping-form" onSubmit={handleSubmit}>
        <input type="hidden" name="access_token" value={accessToken} />

        <div className="form-actions form-actions-top">
          <button className="usual-button" type="button" onClick={resetToUsualShop}>
            Use usual shop
          </button>
        </div>

        <div className="seeded-items" aria-label="Regular shopping items">
          {Object.entries(groupedItems).map(([category, categoryItems], categoryIndex) => (
            <section className="item-category" aria-labelledby={`category-${categoryIndex}`} key={category}>
              <h2 id={`category-${categoryIndex}`}>{category}</h2>
              <div className="item-list">
                {categoryItems.map((item) => (
                  <div className="shopping-item" key={item.id}>
                    <div className="item-details">
                      <label htmlFor={`item-${item.id}`}>{item.name}</label>
                      {item.note ? <span className="note">{item.note}</span> : null}
                    </div>
                    <div className="quantity-controls">
                      <button
                        className="quantity-button"
                        type="button"
                        aria-label={`Reduce ${item.name}`}
                        onClick={() => updateQuantity(item.id, (quantities[item.id] ?? 0) - 1)}
                      >
                        -
                      </button>
                      <input
                        id={`item-${item.id}`}
                        name={`item_${item.id}`}
                        type="number"
                        min="0"
                        inputMode="numeric"
                        value={quantities[item.id] ?? 0}
                        aria-label={`Quantity for ${item.name}`}
                        onChange={(event) => updateQuantity(item.id, Number(event.target.value))}
                      />
                      <button
                        className="quantity-button"
                        type="button"
                        aria-label={`Add ${item.name}`}
                        onClick={() => updateQuantity(item.id, (quantities[item.id] ?? 0) + 1)}
                      >
                        +
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>

        <label className="anything-else" htmlFor="anything-else">
          <span>Anything else?</span>
          <textarea
            id="anything-else"
            name="anything_else"
            rows={5}
            value={anythingElse}
            onChange={(event) => setAnythingElse(event.target.value)}
          />
        </label>

        <div className="form-actions">
          <button className="submit-button" type="submit" disabled={submitStatus.state === "sending"}>
            {submitStatus.state === "sending" ? "Sending..." : "Send list to Warwick"}
          </button>
        </div>

        {submitStatus.state === "sending" || submitStatus.state === "error" ? (
          <p className={`submit-message ${submitStatus.state}`} role="status" aria-live="polite">
            {submitStatus.message}
          </p>
        ) : null}
      </form>
    </section>
  );
}
