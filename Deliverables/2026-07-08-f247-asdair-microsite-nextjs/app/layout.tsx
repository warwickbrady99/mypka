import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "F247 AsdAIr Microsite",
  description: "Private shopping request page for the staged AsdAIr build.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
