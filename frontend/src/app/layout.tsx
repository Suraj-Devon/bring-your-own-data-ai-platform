import "./globals.css";

export const metadata = {
  title: "BYOD AI Decision Engine",
  description: "AI-powered decision intelligence from your own data",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
