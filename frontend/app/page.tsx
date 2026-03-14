'use client'
import { useState } from 'react'
import axios from 'axios'

const API = 'http://localhost:8000'

export default function Home() {
  const [form, setForm] = useState({
    system_type: 'NFT',
    area_sqft: 500,
    target_market: 'export',
    budget: 50000
  })
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const recommend = async () => {
    setLoading(true)
    const res = await axios.get(`${API}/crops/recommend`, { params: { ...form, top_n: 5 } })
    setResults(res.data.recommendations)
    setLoading(false)
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-8">
      <h1 className="text-4xl font-bold text-green-400 mb-2">HydroIQ</h1>
      <p className="text-gray-400 mb-8">Crop intelligence for hydroponic growers</p>

      {/* Form */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="text-sm text-gray-400">System Type</label>
          <select className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.system_type}
            onChange={e => setForm({...form, system_type: e.target.value})}>
            <option>NFT</option>
            <option>DWC</option>
            <option>Kratky</option>
          </select>
        </div>
        <div>
          <label className="text-sm text-gray-400">Area (sq ft)</label>
          <input type="number" className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.area_sqft}
            onChange={e => setForm({...form, area_sqft: Number(e.target.value)})} />
        </div>
        <div>
          <label className="text-sm text-gray-400">Target Market</label>
          <select className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.target_market}
            onChange={e => setForm({...form, target_market: e.target.value})}>
            <option value="export">Export</option>
            <option value="local">Local</option>
          </select>
        </div>
        <div>
          <label className="text-sm text-gray-400">Budget (₹)</label>
          <input type="number" className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.budget}
            onChange={e => setForm({...form, budget: Number(e.target.value)})} />
        </div>
      </div>

      <button onClick={recommend}
        className="bg-green-500 hover:bg-green-400 text-black font-bold px-6 py-2 rounded mb-8">
        {loading ? 'Analyzing...' : 'Get Recommendations'}
      </button>

      {/* Results */}
      {results.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {results.map((crop, i) => (
            <div key={i} className="bg-gray-900 rounded-xl p-5 border border-gray-800">
              <div className="flex justify-between items-start mb-3">
                <h2 className="text-xl font-bold text-green-300">{crop.name}</h2>
                <span className={`text-xs px-2 py-1 rounded ${
                  crop.difficulty === 'Easy' ? 'bg-green-900 text-green-300' :
                  crop.difficulty === 'Medium' ? 'bg-yellow-900 text-yellow-300' :
                  'bg-red-900 text-red-300'}`}>
                  {crop.difficulty}
                </span>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Annual Revenue</span>
                  <span className="text-white font-medium">₹{crop.annual_revenue.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Per Cycle</span>
                  <span className="text-white">₹{crop.revenue_per_cycle.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Cycles/Year</span>
                  <span className="text-white">{crop.cycles_per_year}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Growth Days</span>
                  <span className="text-white">{crop.growth_days} days</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Yield/Cycle</span>
                  <span className="text-white">{crop.yield_per_cycle_kg} kg</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Price/kg</span>
                  <span className="text-white">₹{crop.price_per_kg}</span>
                </div>
              </div>
              <div className="mt-3 flex flex-wrap gap-1">
                {crop.export_markets.map((m: string) => (
                  <span key={m} className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">
                    {m}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}