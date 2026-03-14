'use client'
import { useState } from 'react'
import axios from 'axios'
import Link from 'next/link'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const API = 'http://localhost:8000'

export default function ROIPage() {
  const [form, setForm] = useState({
    crop_id: 'basil',
    system_type: 'NFT',
    area_sqft: 500,
    target_market: 'export',
    setup_cost: 50000,
    monthly_operating_cost: 5000,
    experience_level: 'beginner'
  })
  const [result, setResult] = useState<any>(null)
  const [comparison, setComparison] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const calculate = async () => {
    setLoading(true)
    const [roiRes, compRes] = await Promise.all([
      axios.get(`${API}/roi/calculate`, { params: form }),
      axios.get(`${API}/roi/compare`, { params: {
        system_type: form.system_type,
        area_sqft: form.area_sqft,
        target_market: form.target_market,
        setup_cost: form.setup_cost,
        monthly_operating_cost: form.monthly_operating_cost,
        experience_level: form.experience_level
      }})
    ])
    setResult(roiRes.data)
    setComparison(compRes.data.comparison)
    setLoading(false)
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-8">
      <Link href="/" className="text-green-400 text-sm mb-6 block">← Back</Link>
      <h1 className="text-4xl font-bold text-green-400 mb-2">ROI Calculator</h1>
      <p className="text-gray-400 mb-8">Calculate break-even and annual profit for your setup</p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {[
          { label: 'Crop', key: 'crop_id', type: 'select',
            options: ['basil','mint','lettuce','spinach','kale','cherry_tomato','cucumber','strawberry'] },
          { label: 'System', key: 'system_type', type: 'select', options: ['NFT','DWC','Kratky'] },
          { label: 'Area (sq ft)', key: 'area_sqft', type: 'number' },
          { label: 'Market', key: 'target_market', type: 'select', options: ['export','local'] },
          { label: 'Setup Cost (₹)', key: 'setup_cost', type: 'number' },
          { label: 'Monthly Cost (₹)', key: 'monthly_operating_cost', type: 'number' },
          { label: 'Experience', key: 'experience_level', type: 'select',
            options: ['beginner','intermediate','expert'] },
        ].map(({ label, key, type, options }) => (
          <div key={key}>
            <label className="text-sm text-gray-400">{label}</label>
            {type === 'select' ? (
              <select className="w-full mt-1 bg-gray-800 rounded p-2"
                value={(form as any)[key]}
                onChange={e => setForm({...form, [key]: e.target.value})}>
                {options!.map(o => <option key={o} value={o}>{o.replace('_',' ').replace(/\b\w/g,l=>l.toUpperCase())}</option>)}
              </select>
            ) : (
              <input type="number" className="w-full mt-1 bg-gray-800 rounded p-2"
                value={(form as any)[key]}
                onChange={e => setForm({...form, [key]: Number(e.target.value)})} />
            )}
          </div>
        ))}
      </div>

      <button onClick={calculate}
        className="bg-green-500 hover:bg-green-400 text-black font-bold px-6 py-2 rounded mb-8">
        {loading ? 'Calculating...' : 'Calculate ROI'}
      </button>

      {result && !result.error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Stats */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
            <h2 className="text-xl font-bold text-green-300 mb-4">{result.crop_name}</h2>
            <div className="space-y-3">
              {[
                ['Annual Revenue', `₹${result.annual_revenue.toLocaleString()}`],
                ['Annual Operating Cost', `₹${result.annual_operating_cost.toLocaleString()}`],
                ['Annual Profit', `₹${result.annual_profit.toLocaleString()}`],
                ['Setup Cost', `₹${result.setup_cost.toLocaleString()}`],
                ['Break-even', `${result.breakeven_months} months`],
                ['ROI', `${result.roi_percentage}%`],
                ['Price/kg', `₹${result.price_per_kg}`],
                ['Market', result.target_market],
              ].map(([label, value]) => (
                <div key={label} className="flex justify-between border-b border-gray-800 pb-2">
                  <span className="text-gray-400">{label}</span>
                  <span className={`font-medium ${label === 'Annual Profit' ? 'text-green-400' :
                    label === 'ROI' ? 'text-yellow-400' : 'text-white'}`}>{value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Chart */}
          <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
            <h2 className="text-xl font-bold mb-4">Crop Comparison — Annual Profit</h2>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={comparison.slice(0,6)}>
                <XAxis dataKey="crop_name" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <YAxis tick={{ fill: '#9ca3af', fontSize: 11 }}
                  tickFormatter={v => `₹${(v/1000).toFixed(0)}k`} />
                <Tooltip formatter={(v: any) => [`₹${v.toLocaleString()}`, 'Profit']}
                  contentStyle={{ background: '#111827', border: '1px solid #374151' }} />
                <Bar dataKey="annual_profit" radius={[4,4,0,0]}>
                  {comparison.slice(0,6).map((entry, i) => (
                    <Cell key={i} fill={entry.crop_name === result.crop_name ? '#4ade80' : '#1f2937'}
                      stroke={entry.crop_name === result.crop_name ? '#4ade80' : '#374151'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </main>
  )
}