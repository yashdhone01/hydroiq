'use client'
import { useState, useEffect } from 'react'
import axios from 'axios'
import Link from 'next/link'

const API = 'http://localhost:8000'

export default function ExportPage() {
  const [crops, setCrops] = useState<any[]>([])
  const [markets, setMarkets] = useState<any[]>([])

  useEffect(() => {
    axios.get(`${API}/export/intel`).then(r => setCrops(r.data.crops))
    axios.get(`${API}/export/markets`).then(r => setMarkets(r.data.markets))
  }, [])

  return (
    <main className="min-h-screen bg-gray-950 text-white p-8">
      <Link href="/" className="text-green-400 text-sm mb-6 block">← Back</Link>
      <h1 className="text-4xl font-bold text-green-400 mb-2">Export Intelligence</h1>
      <p className="text-gray-400 mb-8">Compare local vs export prices and discover market opportunities</p>

      {/* Price Comparison Table */}
      <h2 className="text-xl font-semibold mb-4 text-white">Price Comparison</h2>
      <div className="overflow-x-auto mb-10">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-400 border-b border-gray-800">
              <th className="text-left py-3 pr-6">Crop</th>
              <th className="text-right py-3 pr-6">Local ₹/kg</th>
              <th className="text-right py-3 pr-6">Export ₹/kg</th>
              <th className="text-right py-3 pr-6">Premium</th>
              <th className="text-right py-3 pr-6">Difference</th>
              <th className="text-left py-3">Markets</th>
            </tr>
          </thead>
          <tbody>
            {crops.map((crop, i) => (
              <tr key={i} className="border-b border-gray-800 hover:bg-gray-900">
                <td className="py-3 pr-6 font-medium text-green-300">{crop.name}</td>
                <td className="text-right py-3 pr-6">₹{crop.local_price_per_kg}</td>
                <td className="text-right py-3 pr-6">₹{crop.export_price_per_kg}</td>
                <td className="text-right py-3 pr-6">
                  <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                    crop.best_for_export ? 'bg-green-900 text-green-300' : 'bg-gray-800 text-gray-400'}`}>
                    {crop.export_premium}
                  </span>
                </td>
                <td className="text-right py-3 pr-6 text-green-400">+₹{crop.price_difference}</td>
                <td className="py-3">
                  <div className="flex gap-1 flex-wrap">
                    {crop.export_markets.map((m: string) => (
                      <span key={m} className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">{m}</span>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Markets */}
      <h2 className="text-xl font-semibold mb-4 text-white">Export Markets</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {markets.map((m, i) => (
          <div key={i} className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-lg font-bold text-white">{m.name}</h3>
              <span className={`text-xs px-2 py-1 rounded ${
                m.demand === 'High' ? 'bg-green-900 text-green-300' :
                m.demand === 'Medium' ? 'bg-yellow-900 text-yellow-300' :
                'bg-blue-900 text-blue-300'}`}>
                {m.demand}
              </span>
            </div>
            <p className="text-gray-400 text-sm mb-3">{m.notes}</p>
            <div className="flex flex-wrap gap-1">
              {m.top_crops.map((c: string) => (
                <span key={c} className="text-xs bg-gray-800 text-gray-300 px-2 py-0.5 rounded">{c}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </main>
  )
}