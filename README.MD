# HydroIQ

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

**Live:** [hydroiq.vercel.app](https://hydroiq.vercel.app) · **API:** [hydroiq.onrender.com/docs](https://hydroiq.onrender.com/docs)

Full stack crop intelligence platform for hydroponic growers. Input your setup, get ranked crop recommendations with yield estimates, ROI projections, and export market intelligence.

Built this because hydroponic growers — especially those targeting export markets — make critical crop selection decisions based on intuition. HydroIQ gives them data.

---

## What it does

**Crop Recommender** — input system type, area, target market and budget → get crops ranked by ROI per sq ft

**Yield Estimator** — predict harvest output per cycle and annually, adjusted for system efficiency and experience level

**Export Intelligence** — compare local vs export prices, identify which crops fetch the highest premium and in which markets

**ROI Calculator** — input setup and operating costs → get break-even timeline, annual profit, and cross-crop comparison chart

---

## Stack

**Backend** — FastAPI · Python · Pandas · Scikit-learn
**Frontend** — Next.js 15 · TypeScript · Tailwind · Recharts
**Infra** — Docker · GitHub Actions

---

## Quickstart

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
# API running at http://localhost:8000
# Docs at http://localhost:8000/docs
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# App running at http://localhost:3000
```

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /crops/recommend` | Ranked crop recommendations |
| `GET /crops/yield` | Yield estimation per crop |
| `GET /crops/list` | All available crops |
| `GET /export/intel` | Local vs export price comparison |
| `GET /export/markets` | Export market intelligence |
| `GET /roi/calculate` | ROI for a specific crop |
| `GET /roi/compare` | Cross-crop ROI comparison |

---

## Project Structure
```
hydroiq/
├── backend/
│   └── app/
│       ├── data/crops.json         # crop database
│       ├── models/
│       │   ├── recommender.py      # crop ranking engine
│       │   └── yield_estimator.py  # yield & ROI calculations
│       ├── routes/
│       │   ├── crops.py
│       │   ├── export.py
│       │   └── roi.py
│       └── main.py
└── frontend/
    └── app/
        ├── page.tsx                # recommendations
        ├── yield/page.tsx          # yield estimator
        ├── export/page.tsx         # export intel
        └── roi/page.tsx            # ROI calculator
```

---

**Yash Dhone** · [Portfolio](https://yashdhone.vercel.app) · [Twitter](https://x.com/Yash354642)