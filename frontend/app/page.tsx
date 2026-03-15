'use client'
import { useState, useEffect } from 'react'
import axios from 'axios'

const API = 'https://hydroiq.onrender.com'

const UNSPLASH = {
  hero:        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1200&q=80',
  hydro1:      'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=800&q=80',
  hydro2:      'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800&q=80',
  export:      'https://images.unsplash.com/photo-1542838132-92c53300491e?w=800&q=80',
}

const BENEFITS = [
  { icon: '💧', title: '90% Less Water',      desc: 'Hydroponics uses up to 90% less water than traditional soil farming through recirculation systems.' },
  { icon: '📈', title: '3-5x Higher Yield',   desc: 'Controlled environment and optimized nutrients deliver significantly higher yields per square foot.' },
  { icon: '🌍', title: 'Grow Anywhere',       desc: 'No soil needed. Grow fresh produce in urban spaces, rooftops, warehouses, or any indoor setting.' },
  { icon: '🚫', title: 'No Pesticides',       desc: 'Controlled environments eliminate most pests, reducing or eliminating the need for harmful chemicals.' },
  { icon: '📅', title: 'Year-Round Growing',  desc: 'Independent of seasons and weather — grow any crop any time of year.' },
  { icon: '💰', title: 'Export Premium',      desc: 'Pesticide-free hydroponic produce commands 3-8x higher prices in UAE, EU, and UK export markets.' },
]

export default function Home() {
  const [form, setForm]           = useState({ system_type: 'NFT', area_sqft: 500, target_market: 'export', budget: 50000 })
  const [roiForm, setRoiForm]     = useState({ crop_id: 'basil', setup_cost: 50000, monthly_operating_cost: 5000, experience_level: 'beginner' })
  const [results, setResults]     = useState<any[]>([])
  const [yieldData, setYieldData] = useState<any>(null)
  const [prices, setPrices]       = useState<any>(null)
  const [roi, setRoi]             = useState<any>(null)
  const [loading, setLoading]     = useState(false)
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    axios.get(`${API}/prices/live`).then(r => setPrices(r.data)).catch(() => {})
  }, [])

  const analyze = async () => {
    setLoading(true)
    try {
      const rec = await axios.get(`${API}/crops/recommend`, { params: { ...form, top_n: 5 } })
      setResults(rec.data.recommendations)
      if (rec.data.recommendations.length > 0) {
        const topCrop = rec.data.recommendations[0].id
        setRoiForm(f => ({ ...f, crop_id: topCrop }))
        const [yld, roiRes] = await Promise.all([
          axios.get(`${API}/crops/yield`, { params: { crop_id: topCrop, system_type: form.system_type, area_sqft: form.area_sqft, experience_level: roiForm.experience_level } }),
          axios.get(`${API}/roi/calculate`, { params: { crop_id: topCrop, system_type: form.system_type, area_sqft: form.area_sqft, target_market: form.target_market, setup_cost: roiForm.setup_cost, monthly_operating_cost: roiForm.monthly_operating_cost, experience_level: roiForm.experience_level } })
        ])
        setYieldData(yld.data)
        setRoi(roiRes.data)
      }
      setSubmitted(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ fontFamily: "'DM Sans', sans-serif", background: '#f8f6f1', color: '#1a1a1a', minHeight: '100vh' }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet" />

      {/* NAV */}
      <nav style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100, background: 'rgba(248,246,241,0.92)', backdropFilter: 'blur(12px)', borderBottom: '1px solid #e8e4dc', padding: '0 2rem', height: '60px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontFamily: "'Playfair Display', serif", fontWeight: 900, fontSize: '1.3rem', color: '#2d5a27' }}>HydroIQ</span>
        <div style={{ display: 'flex', gap: '2rem' }}>
          {['About', 'Analyze', 'Prices', 'Contact'].map(l => (
            <a key={l} href={`#${l.toLowerCase()}`} style={{ fontSize: '0.85rem', color: '#555', textDecoration: 'none', fontWeight: 500 }}>{l}</a>
          ))}
        </div>
      </nav>

      {/* HERO */}
      <section style={{ paddingTop: '60px', position: 'relative', height: '92vh', display: 'flex', alignItems: 'center', overflow: 'hidden' }}>
        <img src={UNSPLASH.hero} alt="hydroponics" style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.35)' }} />
        <div style={{ position: 'relative', zIndex: 2, padding: '0 4rem', maxWidth: '700px' }}>
          <div style={{ display: 'inline-block', background: 'rgba(255,255,255,0.15)', border: '1px solid rgba(255,255,255,0.3)', borderRadius: '20px', padding: '4px 14px', fontSize: '0.78rem', color: '#b8ffb0', marginBottom: '1.2rem', backdropFilter: 'blur(8px)' }}>
            AI-Powered · Live Market Data · Export Intelligence
          </div>
          <h1 style={{ fontFamily: "'Playfair Display', serif", fontSize: 'clamp(2.8rem, 6vw, 5rem)', fontWeight: 900, color: '#fff', lineHeight: 1.1, marginBottom: '1.2rem' }}>
            Grow Smarter.<br />
            <span style={{ color: '#7ddd6f' }}>Profit More.</span>
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '1.1rem', lineHeight: 1.7, marginBottom: '2rem', maxWidth: '500px' }}>
            HydroIQ tells you exactly which crops to grow, what yield to expect, and how much you'll earn — powered by machine learning and real Indian market prices.
          </p>
          <a href="#analyze" style={{ display: 'inline-block', background: '#4caf50', color: '#fff', padding: '14px 32px', borderRadius: '8px', fontWeight: 600, fontSize: '1rem', textDecoration: 'none', transition: 'background 0.2s' }}>
            Analyze My Setup →
          </a>
        </div>
      </section>

      {/* ABOUT HYDROPONICS */}
      <section id="about" style={{ padding: '6rem 4rem', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5rem', alignItems: 'center' }}>
          <div>
            <p style={{ color: '#4caf50', fontWeight: 600, fontSize: '0.85rem', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '1rem' }}>What is Hydroponics?</p>
            <h2 style={{ fontFamily: "'Playfair Display', serif", fontSize: '2.8rem', fontWeight: 900, lineHeight: 1.2, marginBottom: '1.5rem' }}>Farming without soil.<br />Results beyond belief.</h2>
            <p style={{ color: '#555', lineHeight: 1.9, fontSize: '1rem', marginBottom: '1rem' }}>
              Hydroponics is a method of growing plants using mineral nutrient solutions in water, without soil. Plants receive nutrients directly through their roots in a controlled environment — resulting in faster growth, higher yields, and year-round production.
            </p>
            <p style={{ color: '#555', lineHeight: 1.9, fontSize: '1rem' }}>
              India's hydroponic market is growing at 13% annually, driven by urban farming demand and premium export opportunities to UAE, EU, and UK markets where pesticide-free produce commands 3-8x higher prices.
            </p>
          </div>
          <div style={{ position: 'relative' }}>
            <img src={UNSPLASH.hydro1} alt="hydroponics farm" style={{ width: '100%', borderRadius: '16px', boxShadow: '0 20px 60px rgba(0,0,0,0.15)' }} />
            <div style={{ position: 'absolute', bottom: '-20px', left: '-20px', background: '#fff', borderRadius: '12px', padding: '16px 20px', boxShadow: '0 8px 30px rgba(0,0,0,0.1)' }}>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#4caf50' }}>13%</div>
              <div style={{ fontSize: '0.8rem', color: '#666' }}>Annual market growth in India</div>
            </div>
          </div>
        </div>
      </section>

      {/* BENEFITS */}
      <section style={{ background: '#fff', padding: '6rem 4rem' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <p style={{ color: '#4caf50', fontWeight: 600, fontSize: '0.85rem', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '1rem', textAlign: 'center' }}>Why Hydroponics</p>
          <h2 style={{ fontFamily: "'Playfair Display', serif", fontSize: '2.5rem', fontWeight: 900, textAlign: 'center', marginBottom: '3rem' }}>Built for the modern grower</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem' }}>
            {BENEFITS.map((b, i) => (
              <div key={i} style={{ background: '#f8f6f1', borderRadius: '16px', padding: '2rem', border: '1px solid #eee' }}>
                <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>{b.icon}</div>
                <h3 style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: '0.6rem' }}>{b.title}</h3>
                <p style={{ color: '#666', fontSize: '0.9rem', lineHeight: 1.7 }}>{b.desc}</p>
              </div>
            ))}
          </div>
          <div style={{ marginTop: '4rem', borderRadius: '20px', overflow: 'hidden', height: '350px', position: 'relative' }}>
            <img src={UNSPLASH.hydro2} alt="hydroponic produce" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to right, rgba(0,0,0,0.6), transparent)', display: 'flex', alignItems: 'center', padding: '3rem' }}>
              <div>
                <h3 style={{ fontFamily: "'Playfair Display', serif", color: '#fff', fontSize: '2rem', fontWeight: 900, marginBottom: '0.5rem' }}>Ready to start growing?</h3>
                <p style={{ color: 'rgba(255,255,255,0.8)', marginBottom: '1.5rem' }}>Let HydroIQ find the most profitable crop for your setup.</p>
                <a href="#analyze" style={{ background: '#4caf50', color: '#fff', padding: '12px 28px', borderRadius: '8px', fontWeight: 600, textDecoration: 'none', fontSize: '0.95rem' }}>Get Started</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ANALYZE FORM */}
      <section id="analyze" style={{ padding: '6rem 4rem', maxWidth: '1200px', margin: '0 auto' }}>
        <p style={{ color: '#4caf50', fontWeight: 600, fontSize: '0.85rem', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '1rem' }}>AI Analysis</p>
        <h2 style={{ fontFamily: "'Playfair Display', serif", fontSize: '2.5rem', fontWeight: 900, marginBottom: '0.5rem' }}>Tell us about your setup</h2>
        <p style={{ color: '#666', marginBottom: '3rem' }}>Our ML model will recommend the best crops, estimate your yield, and calculate your ROI.</p>

        <div style={{ background: '#fff', borderRadius: '20px', padding: '2.5rem', boxShadow: '0 4px 30px rgba(0,0,0,0.06)', border: '1px solid #eee', marginBottom: '1.5rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '1.5rem' }}>
            {[
              { label: 'System Type', key: 'system_type', type: 'select', options: ['NFT', 'DWC', 'Kratky'] },
              { label: 'Area (sq ft)', key: 'area_sqft', type: 'number' },
              { label: 'Target Market', key: 'target_market', type: 'select', options: ['export', 'local'] },
              { label: 'Budget (₹)', key: 'budget', type: 'number' },
            ].map(({ label, key, type, options }) => (
              <div key={key}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#444', marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</label>
                {type === 'select' ? (
                  <select style={{ width: '100%', padding: '10px 12px', borderRadius: '8px', border: '1.5px solid #e0ddd8', background: '#f8f6f1', fontSize: '0.95rem', outline: 'none' }}
                    value={(form as any)[key]}
                    onChange={e => setForm({ ...form, [key]: e.target.value })}>
                    {options!.map(o => <option key={o} value={o}>{o.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</option>)}
                  </select>
                ) : (
                  <input type="number" style={{ width: '100%', padding: '10px 12px', borderRadius: '8px', border: '1.5px solid #e0ddd8', background: '#f8f6f1', fontSize: '0.95rem', outline: 'none', boxSizing: 'border-box' }}
                    value={(form as any)[key]}
                    onChange={e => setForm({ ...form, [key]: Number(e.target.value) })} />
                )}
              </div>
            ))}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
            {[
              { label: 'Setup Cost (₹)', key: 'setup_cost', type: 'number' },
              { label: 'Monthly Operating Cost (₹)', key: 'monthly_operating_cost', type: 'number' },
              { label: 'Experience Level', key: 'experience_level', type: 'select', options: ['beginner', 'intermediate', 'expert'] },
            ].map(({ label, key, type, options }) => (
              <div key={key}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#444', marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</label>
                {type === 'select' ? (
                  <select style={{ width: '100%', padding: '10px 12px', borderRadius: '8px', border: '1.5px solid #e0ddd8', background: '#f8f6f1', fontSize: '0.95rem', outline: 'none' }}
                    value={(roiForm as any)[key]}
                    onChange={e => setRoiForm({ ...roiForm, [key]: e.target.value })}>
                    {options!.map(o => <option key={o} value={o}>{o.charAt(0).toUpperCase() + o.slice(1)}</option>)}
                  </select>
                ) : (
                  <input type="number" style={{ width: '100%', padding: '10px 12px', borderRadius: '8px', border: '1.5px solid #e0ddd8', background: '#f8f6f1', fontSize: '0.95rem', outline: 'none', boxSizing: 'border-box' }}
                    value={(roiForm as any)[key]}
                    onChange={e => setRoiForm({ ...roiForm, [key]: Number(e.target.value) })} />
                )}
              </div>
            ))}
          </div>
          <button onClick={analyze} disabled={loading}
            style={{ background: loading ? '#aaa' : '#4caf50', color: '#fff', border: 'none', padding: '14px 40px', borderRadius: '8px', fontWeight: 700, fontSize: '1rem', cursor: loading ? 'not-allowed' : 'pointer', transition: 'background 0.2s' }}>
            {loading ? 'Analyzing...' : 'Analyze My Setup →'}
          </button>
        </div>

        {/* RECOMMENDATIONS */}
        {submitted && results.length > 0 && (
          <div style={{ marginTop: '3rem' }}>
            <h3 style={{ fontFamily: "'Playfair Display', serif", fontSize: '1.8rem', fontWeight: 900, marginBottom: '1.5rem' }}>
              🌱 Crop Recommendations
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '3rem' }}>
              {results.map((crop, i) => (
                <div key={i} style={{ background: '#fff', borderRadius: '16px', padding: '1.8rem', border: i === 0 ? '2px solid #4caf50' : '1px solid #eee', position: 'relative', boxShadow: i === 0 ? '0 8px 30px rgba(76,175,80,0.15)' : '0 2px 10px rgba(0,0,0,0.04)' }}>
                  {i === 0 && <div style={{ position: 'absolute', top: '-12px', left: '20px', background: '#4caf50', color: '#fff', fontSize: '0.75rem', fontWeight: 700, padding: '3px 12px', borderRadius: '20px' }}>TOP PICK</div>}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                    <h4 style={{ fontWeight: 700, fontSize: '1.2rem' }}>{crop.name}</h4>
                    <span style={{ fontSize: '0.75rem', padding: '3px 10px', borderRadius: '20px', fontWeight: 600, background: crop.difficulty === 'Easy' ? '#e8f5e9' : crop.difficulty === 'Medium' ? '#fff8e1' : '#fce4ec', color: crop.difficulty === 'Easy' ? '#2e7d32' : crop.difficulty === 'Medium' ? '#f57f17' : '#c62828' }}>
                      {crop.difficulty}
                    </span>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.6rem', fontSize: '0.85rem' }}>
                    {[
                      ['Annual Revenue', `₹${crop.annual_revenue.toLocaleString()}`],
                      ['Per Cycle', `₹${crop.revenue_per_cycle.toLocaleString()}`],
                      ['Cycles/Year', crop.cycles_per_year],
                      ['Growth Days', `${crop.growth_days}d`],
                      ['Price/kg', `₹${crop.price_per_kg}`],
                      ['Source', crop.price_source],
                    ].map(([l, v]) => (
                      <div key={l}>
                        <div style={{ color: '#999', fontSize: '0.75rem' }}>{l}</div>
                        <div style={{ fontWeight: 600, color: l === 'Source' && v === 'live' ? '#4caf50' : '#1a1a1a' }}>{v}</div>
                      </div>
                    ))}
                  </div>
                  <div style={{ marginTop: '1rem', display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                    {crop.export_markets.map((m: string) => (
                      <span key={m} style={{ fontSize: '0.72rem', background: '#e3f2fd', color: '#1565c0', padding: '2px 8px', borderRadius: '12px' }}>{m}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* YIELD */}
            {yieldData && !yieldData.error && (
              <div style={{ background: '#fff', borderRadius: '16px', padding: '2rem', border: '1px solid #eee', marginBottom: '2rem' }}>
                <h3 style={{ fontFamily: "'Playfair Display', serif", fontSize: '1.6rem', fontWeight: 900, marginBottom: '1.5rem' }}>📊 Yield Estimate — {yieldData.crop_name}</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem' }}>
                  {[
                    ['Yield / Cycle', `${yieldData.yield_per_cycle_kg} kg`],
                    ['Annual Yield', `${yieldData.annual_yield_kg} kg`],
                    ['Cycles / Year', yieldData.cycles_per_year],
                    ['Growth Days', `${yieldData.growth_days} days`],
                  ].map(([l, v]) => (
                    <div key={l} style={{ background: '#f8f6f1', borderRadius: '12px', padding: '1.2rem', textAlign: 'center' }}>
                      <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#2d5a27' }}>{v}</div>
                      <div style={{ fontSize: '0.8rem', color: '#888', marginTop: '4px' }}>{l}</div>
                    </div>
                  ))}
                </div>
                <p style={{ marginTop: '1rem', fontSize: '0.8rem', color: '#999' }}>Model: {yieldData.model} · R² = {yieldData.r2_score}</p>
              </div>
            )}

            {/* ROI */}
            {roi && !roi.error && (
              <div style={{ background: '#fff', borderRadius: '16px', padding: '2rem', border: '1px solid #eee', marginBottom: '2rem' }}>
                <h3 style={{ fontFamily: "'Playfair Display', serif", fontSize: '1.6rem', fontWeight: 900, marginBottom: '1.5rem' }}>💰 ROI Calculator — {roi.crop_name}</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem' }}>
                  {[
                    ['Annual Revenue', `₹${roi.annual_revenue.toLocaleString()}`, '#4caf50'],
                    ['Annual Profit', `₹${roi.annual_profit.toLocaleString()}`, roi.annual_profit > 0 ? '#2e7d32' : '#c62828'],
                    ['Break-even', `${roi.breakeven_months} months`, '#1565c0'],
                    ['ROI', `${roi.roi_percentage}%`, '#f57f17'],
                  ].map(([l, v, c]) => (
                    <div key={l} style={{ background: '#f8f6f1', borderRadius: '12px', padding: '1.2rem', textAlign: 'center' }}>
                      <div style={{ fontSize: '1.5rem', fontWeight: 800, color: c as string }}>{v}</div>
                      <div style={{ fontSize: '0.8rem', color: '#888', marginTop: '4px' }}>{l}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      {/* LIVE PRICES */}
      <section id="prices" style={{ background: '#fff', padding: '6rem 4rem' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5rem', alignItems: 'center' }}>
            <div>
              <p style={{ color: '#4caf50', fontWeight: 600, fontSize: '0.85rem', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '1rem' }}>Live Market Data</p>
              <h2 style={{ fontFamily: "'Playfair Display', serif", fontSize: '2.5rem', fontWeight: 900, marginBottom: '1rem' }}>Real prices.<br />Real decisions.</h2>
              <p style={{ color: '#666', lineHeight: 1.8, marginBottom: '2rem' }}>
                HydroIQ fetches live mandi prices from the Government of India's Agmarknet database (data.gov.in) on every startup — so your ROI calculations are always based on today's actual market prices, not guesses.
              </p>
              {prices && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                  {Object.entries(prices.prices).map(([crop, price]: [string, any]) => (
                    <div key={crop} style={{ background: '#f8f6f1', borderRadius: '12px', padding: '1rem 1.2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: 600, textTransform: 'capitalize' }}>{crop.replace('_', ' ')}</span>
                      <span style={{ color: '#4caf50', fontWeight: 700 }}>₹{price}/kg</span>
                    </div>
                  ))}
                </div>
              )}
              <p style={{ marginTop: '1rem', fontSize: '0.75rem', color: '#aaa' }}>Source: data.gov.in · Agmarknet · Updated on server startup</p>
            </div>
            <img src={UNSPLASH.export} alt="market prices" style={{ width: '100%', borderRadius: '16px', boxShadow: '0 20px 60px rgba(0,0,0,0.12)' }} />
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer id="contact" style={{ background: '#1a1a1a', color: '#fff', padding: '4rem', textAlign: 'center' }}>
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <span style={{ fontFamily: "'Playfair Display', serif", fontWeight: 900, fontSize: '1.8rem', color: '#7ddd6f' }}>HydroIQ</span>
          <p style={{ color: '#aaa', margin: '1rem 0 2rem', lineHeight: 1.8 }}>
            Open source crop intelligence for hydroponic growers.<br />
            Built with FastAPI · Next.js · Scikit-learn · Agmarknet API
          </p>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginBottom: '2rem' }}>
            <a href="https://github.com/yashdhone01/hydroiq" target="_blank" style={{ color: '#7ddd6f', textDecoration: 'none', fontWeight: 600 }}>⌥ Source Code</a>
            <a href="https://x.com/Yash354642" target="_blank" style={{ color: '#7ddd6f', textDecoration: 'none', fontWeight: 600 }}>𝕏 Twitter</a>
            <a href="https://linkedin.com/in/yashdhone" target="_blank" style={{ color: '#7ddd6f', textDecoration: 'none', fontWeight: 600 }}>in LinkedIn</a>
            <a href="mailto:yash.dhone01@gmail.com" style={{ color: '#7ddd6f', textDecoration: 'none', fontWeight: 600 }}>✉ Email</a>
          </div>
          <p style={{ color: '#555', fontSize: '0.8rem' }}>© {new Date().getFullYear()} Yash Dhone · MIT License</p>
        </div>
      </footer>
    </main>
  )
}