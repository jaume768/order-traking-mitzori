import './globals.css';

export const metadata = {
  title: 'Order Tracking - Mitzori',
  description: 'Real-time order tracking system',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
