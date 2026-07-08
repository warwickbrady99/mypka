import { NextResponse } from "next/server";
import { catalogueItems } from "../../../lib/catalogue";
import { sendShoppingEmail, type ShoppingEmailItem } from "../../../lib/shopping-email";

export const runtime = "nodejs";

type ShoppingListRequest = {
  accessToken?: unknown;
  items?: unknown;
  anythingElse?: unknown;
};

function cleanText(value: unknown, maxLength: number): string {
  if (typeof value !== "string") {
    return "";
  }

  return value.trim().slice(0, maxLength);
}

function cleanQuantity(value: unknown): number {
  if (typeof value !== "number" || !Number.isFinite(value) || value < 0) {
    return 0;
  }

  return Math.floor(value);
}

function selectedItemsFromPayload(payloadItems: unknown): ShoppingEmailItem[] {
  if (!Array.isArray(payloadItems)) {
    return [];
  }

  const quantityById = new Map<string, number>();

  for (const item of payloadItems) {
    if (!item || typeof item !== "object") {
      continue;
    }

    const id = "id" in item ? item.id : undefined;
    const quantity = "quantity" in item ? item.quantity : undefined;

    if (typeof id === "string") {
      quantityById.set(id, cleanQuantity(quantity));
    }
  }

  return catalogueItems
    .map((item) => ({
      name: item.name,
      category: item.category,
      quantity: quantityById.get(item.id) ?? 0,
      note: item.note,
    }))
    .filter((item) => item.quantity > 0);
}

export async function POST(request: Request) {
  const configuredToken = process.env.MUM_ACCESS_TOKEN;

  if (!configuredToken) {
    return NextResponse.json({ message: "The private shopping link is not configured yet." }, { status: 500 });
  }

  let payload: ShoppingListRequest;

  try {
    payload = (await request.json()) as ShoppingListRequest;
  } catch {
    return NextResponse.json({ message: "That shopping list could not be read." }, { status: 400 });
  }

  if (payload.accessToken !== configuredToken) {
    return NextResponse.json({ message: "This private shopping link is not valid." }, { status: 403 });
  }

  const selectedItems = selectedItemsFromPayload(payload.items);
  const anythingElse = cleanText(payload.anythingElse, 2000);

  if (selectedItems.length === 0 && !anythingElse) {
    return NextResponse.json(
      { message: "Please choose at least one item or add a note before sending." },
      { status: 400 },
    );
  }

  try {
    await sendShoppingEmail({ items: selectedItems, anythingElse });
    return NextResponse.json({ message: "Thanks, the shopping list has been sent to Warwick." });
  } catch (error) {
    console.error("Shopping email failed", error);
    return NextResponse.json(
      { message: "Sorry, the shopping list could not be sent just now. Please try again in a minute." },
      { status: 502 },
    );
  }
}
