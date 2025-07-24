
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import '../styles/globals.css';
import { Providers } from '@/components/providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Automotas AI - Multi-Agent Orchestrator',
  description: 'Advanced AI orchestration platform for automated workflows and intelligent agent management',
  keywords: ['AI', 'Automation', 'Multi-Agent', 'Orchestration', 'GitHub', 'Workflows', 'Automotas'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
