import { notFound } from "next/navigation";
import { catalogueItems } from "../../../lib/catalogue";
import { ShoppingPage } from "../../../components/ShoppingPage";

type MumPageProps = {
  params: Promise<{
    token: string;
  }>;
};

export default async function MumPage({ params }: MumPageProps) {
  const { token } = await params;
  const configuredToken = process.env.MUM_ACCESS_TOKEN;

  if (!configuredToken || token !== configuredToken) {
    notFound();
  }

  return (
    <main className="page-shell">
      <ShoppingPage accessToken={token} items={catalogueItems} />
    </main>
  );
}
