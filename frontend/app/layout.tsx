import type { Metadata } from 'next'
import { Geist } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const geist = Geist({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'HydroIQ',
  description: 'Crop intelligence for hydroponic growers',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${geist.className} bg-gray-950`}>
        <nav className="border-b border-gray-800 px-8 py-4 flex gap-6 items-center">
          <Link href="/" className="text-green-400 font-bold text-lg">HydroIQ</Link>
          <Link href="/" className="text-gray-400 hover:text-white text-sm">Recommend</Link>
          <Link href="/yield" className="text-gray-400 hover:text-white text-sm">Yield</Link>
          <Link href="/export" className="text-gray-400 hover:text-white text-sm">Export</Link>
          <Link href="/roi" className="text-gray-400 hover:text-white text-sm">ROI</Link>
        </nav>
        {children}
      </body>
    </html>
  )
}