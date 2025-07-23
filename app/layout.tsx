import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Orchestrator AI',
  description: 'Advanced AI orchestration platform for seamless automation and intelligent workflow management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body>
        {children}
      </body>
    </html>
  )
}