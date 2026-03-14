'use client'
import { useState } from 'react'
import axios from 'axios'
import Link from 'next/link'

const API = 'http://localhost:8000'

export default function YieldPage() {
  const [form, setForm] = useState({
    crop_id: 'basil',
    system_type: 'NFT',
    area_sqft: 500,
    experience_level: 'beginner'
  })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const estimate = async () => {
    setLoading(true)
    const res = await axios.get(`${API}/crops/yield`, { params: form })
    setResult(res.data)
    setLoading(false)
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-8">
      <Link href="/" className="text-green-400 text-sm mb-6 block">← Back</Link>
      <h1 className="text-4xl font-bold text-green-400 mb-2">Yield Estimator</h1>
      <p className="text-gray-400 mb-8">Predict your harvest output per cycle and annually</p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="text-sm text-gray-400">Crop</label>
          <select className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.crop_id}
            onChange={e => setForm({...form, crop_id: e.target.value})}>
            {['basil','mint','lettuce','spinach','kale','cherry_tomato','cucumber','strawberry'].map(c => (
              <option key={c} value={c}>{c.replace('_',' ').replace(/\b\w/g, l => l.toUpperCase())}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-sm text-gray-400">System</label>
          <select className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.system_type}
            onChange={e => setForm({...form, system_type: e.target.value})}>
            <option>NFT</option><option>DWC</option><option>Kratky</option>
          </select>
        </div>
        <div>
          <label className="text-sm text-gray-400">Area (sq ft)</label>
          <input type="number" className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.area_sqft}
            onChange={e => setForm({...form, area_sqft: Number(e.target.value)})} />
        </div>
        <div>
          <label className="text-sm text-gray-400">Experience</label>
          <select className="w-full mt-1 bg-gray-800 rounded p-2"
            value={form.experience_level}
            onChange={e => setForm({...form, experience_level: e.target.value})}>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="expert">Expert</option>
          </select>
        </div>
      </div>

      <button onClick={estimate}
        className="bg-green-500 hover:bg-green-400 text-black font-bold px-6 py-2 rounded mb-8">
        {loading ? 'Calculating...' : 'Estimate Yield'}
      </button>

      {result && !result.error && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 max-w-lg">
          <h2 className="text-2xl font-bold text-green-300 mb-4">{result.crop_name}</h2>
          <div className="space-y-3">
            {[
              ['System', result.system_type],
              ['Area', `${result.area_sqft} sq ft`],
              ['Experience', result.experience_level],
              ['Yield per Cycle', `${result.yield_per_cycle_kg} kg`],
              ['Cycles per Year', result.cycles_per_year],
              ['Annual Yield', `${result.annual_yield_kg} kg`],
              ['Growth Days', `${result.growth_days} days`],
              ['System Efficiency', result.system_efficiency],
              ['Experience Efficiency', result.experience_efficiency],
            ].map(([label, value]) => (
              <div key={label} className="flex justify-between border-b border-gray-800 pb-2">
                <span className="text-gray-400">{label}</span>
                <span className="font-medium">{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  )
}