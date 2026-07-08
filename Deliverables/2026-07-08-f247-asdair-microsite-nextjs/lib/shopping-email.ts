import { Buffer } from "node:buffer";
import tls from "node:tls";

export type ShoppingEmailItem = {
  name: string;
  category: string;
  quantity: number;
  note?: string;
};

type ShoppingEmailInput = {
  items: ShoppingEmailItem[];
  anythingElse: string;
};

type GmailSmtpConfig = {
  user: string;
  appPassword: string;
  to: string;
};

const SMTP_HOST = "smtp.gmail.com";
const SMTP_PORT = 465;
const SAFETY_WORDING =
  "This is a shopping request only. Warwick remains responsible for final checkout.";

function requireEnv(name: string): string {
  const value = process.env[name]?.trim();

  if (!value) {
    throw new Error(`Missing ${name}`);
  }

  return value;
}

function getConfig(): GmailSmtpConfig {
  return {
    user: requireEnv("GMAIL_SMTP_USER"),
    appPassword: requireEnv("GMAIL_SMTP_APP_PASSWORD"),
    to: requireEnv("SHOPPING_EMAIL_TO"),
  };
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function formatTextEmail(input: ShoppingEmailInput): string {
  const lines = [
    "Mum's shopping list",
    "",
    "Items:",
    ...input.items.map((item) => {
      const note = item.note ? ` (${item.note})` : "";
      return `- ${item.name}${note}: x${item.quantity} [${item.category}]`;
    }),
    "",
    "Anything else?",
    input.anythingElse || "Nothing added.",
    "",
    "Safety boundary:",
    SAFETY_WORDING,
  ];

  return lines.join("\r\n");
}

function formatHtmlEmail(input: ShoppingEmailInput): string {
  const itemRows = input.items
    .map(
      (item) => `
        <tr>
          <td>${escapeHtml(item.name)}${item.note ? `<br><small>${escapeHtml(item.note)}</small>` : ""}</td>
          <td>${escapeHtml(item.category)}</td>
          <td style="text-align:right;">${item.quantity}</td>
        </tr>`,
    )
    .join("");

  return `<!doctype html>
<html>
  <body style="font-family:Arial,sans-serif;color:#181a1f;">
    <h1>Mum's shopping list</h1>
    <table style="border-collapse:collapse;width:100%;max-width:720px;">
      <thead>
        <tr>
          <th style="border-bottom:1px solid #d7d7cf;text-align:left;padding:8px;">Item</th>
          <th style="border-bottom:1px solid #d7d7cf;text-align:left;padding:8px;">Category</th>
          <th style="border-bottom:1px solid #d7d7cf;text-align:right;padding:8px;">Qty</th>
        </tr>
      </thead>
      <tbody>${itemRows}</tbody>
    </table>
    <h2>Anything else?</h2>
    <p>${input.anythingElse ? escapeHtml(input.anythingElse).replaceAll("\n", "<br>") : "Nothing added."}</p>
    <h2>Safety boundary</h2>
    <p>${escapeHtml(SAFETY_WORDING)}</p>
  </body>
</html>`;
}

function encodeAddress(email: string): string {
  return `<${email}>`;
}

function buildMessage(config: GmailSmtpConfig, input: ShoppingEmailInput): string {
  const boundary = `shopping-${Date.now()}`;
  const subject = "Mum's shopping list";
  const textBody = formatTextEmail(input);
  const htmlBody = formatHtmlEmail(input);

  return [
    `From: ${encodeAddress(config.user)}`,
    `To: ${encodeAddress(config.to)}`,
    `Subject: ${subject}`,
    "MIME-Version: 1.0",
    `Content-Type: multipart/alternative; boundary="${boundary}"`,
    "",
    `--${boundary}`,
    'Content-Type: text/plain; charset="UTF-8"',
    "Content-Transfer-Encoding: 8bit",
    "",
    textBody,
    `--${boundary}`,
    'Content-Type: text/html; charset="UTF-8"',
    "Content-Transfer-Encoding: 8bit",
    "",
    htmlBody,
    `--${boundary}--`,
    "",
  ].join("\r\n");
}

function readLine(socket: tls.TLSSocket): Promise<string> {
  return new Promise((resolve, reject) => {
    let data = "";

    function cleanup() {
      socket.off("data", onData);
      socket.off("error", onError);
    }

    function onError(error: Error) {
      cleanup();
      reject(error);
    }

    function onData(chunk: Buffer) {
      data += chunk.toString("utf8");

      const lines = data.split(/\r?\n/).filter(Boolean);
      const lastLine = lines.at(-1);

      if (lastLine && /^\d{3} /.test(lastLine)) {
        cleanup();
        resolve(data);
      }
    }

    socket.on("data", onData);
    socket.on("error", onError);
  });
}

async function expect(socket: tls.TLSSocket, code: number): Promise<void> {
  const response = await readLine(socket);

  if (!response.startsWith(String(code))) {
    throw new Error(`SMTP error: expected ${code}`);
  }
}

async function command(socket: tls.TLSSocket, line: string, code: number): Promise<void> {
  socket.write(`${line}\r\n`);
  await expect(socket, code);
}

export async function sendShoppingEmail(input: ShoppingEmailInput): Promise<void> {
  const config = getConfig();
  const message = buildMessage(config, input);

  const socket = tls.connect({
    host: SMTP_HOST,
    port: SMTP_PORT,
    servername: SMTP_HOST,
  });

  try {
    await expect(socket, 220);
    await command(socket, "EHLO localhost", 250);
    await command(socket, "AUTH LOGIN", 334);
    await command(socket, Buffer.from(config.user).toString("base64"), 334);
    await command(socket, Buffer.from(config.appPassword).toString("base64"), 235);
    await command(socket, `MAIL FROM:<${config.user}>`, 250);
    await command(socket, `RCPT TO:<${config.to}>`, 250);
    await command(socket, "DATA", 354);
    socket.write(`${message}\r\n.\r\n`);
    await expect(socket, 250);
    await command(socket, "QUIT", 221);
  } finally {
    socket.destroy();
  }
}
