import Link from "next/link";

export default function AccessHelpPage() {
  return (
    <main className="page-shell">
      <section className="shopping-panel" aria-labelledby="page-title">
        <h1 id="page-title">Private shopping link</h1>
        <p>Open Mum's private shopping link to send a shopping request to Warwick.</p>
        <p className="empty-message">
          The link should look like <span className="inline-code">/mum/your-private-token</span>.
        </p>
        <Link className="back-link" href="/">
          Keep this page private
        </Link>
      </section>
    </main>
  );
}
