# HydroIQ

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

**Live:** [hydroiq.vercel.app](https://hydroiq.vercel.app)

Full stack crop intelligence platform for hydroponic growers. HydroIQ replaces intuition-based farming with a data-driven recommendation engine for yield, ROI, and export market potential.

---

## How it works: Core Methodology

### 1. Identify Optimal Crop Profiles
The system iterates through a multidimensional crop database to identify candidates based on the physical constraints of the user's setup.
* **System Matching**: Each crop is validated against the identified system type (e.g., NFT, DWC, Aeroponics).
* **Budget Thresholding**: A threshold is set to exclude crops whose initial nutrient and seed costs exceed the user's stated budget.

### 2. Yield Estimation Logic
The `yield_estimator.py` model calculates potential harvest output using a cycle-based mathematical model.
* **Calculation**: Annual output is calculated by multiplying the yield per cycle by the frequency of harvest cycles possible within 365 days.
* **Efficiency Scaling**: The model applies a dynamic efficiency factor based on the grower's experience level and system precision to adjust the final output.

### 3. Market Intelligence & ROI Analysis
The tool fetches live market data from government APIs to calculate the "Export Premium".
* **Effective Profit**: This is calculated as: 
  $$Profit = (MarketPrice - OperatingCosts) \times TotalYield$$
* **ROI Logic**: The system identifies the break-even timeline by dividing initial setup costs by the projected net profit per month.

### 4. Recommendation Ranking Engine
The `recommender.py` module uses a weighted scoring algorithm to rank crops based on economic and operational viability.
* **Scoring Formula**: Crops are ranked by: 
  $$Score = (w_1 \cdot ROI) + (w_2 \cdot Demand) - (w_3 \cdot ResourceComplexity)$$
* This allows the tool to penalize high-profit crops that have a prohibitive maintenance complexity for beginners.

---

## System Architecture



The platform is designed as a decoupled full-stack application:
* **Data Processing Layer**: Python/Pandas handles the ingestion of live market intelligence and crop biological data.
* **Intelligence Layer**: Scikit-learn powered recommendation engine that processes user inputs to generate ranked output.
* **API Layer**: FastAPI serves high-performance endpoints for real-time yield and ROI calculations.
* **Presentation Layer**: A Next.js 15 frontend utilizing Recharts for dynamic visualization of ROI projections and yield curves.

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /crops/recommend` | Ranked crop recommendations |
| `GET /crops/yield` | Yield estimation per crop |
| `GET /export/intel` | Local vs export price comparison |
| `GET /roi/calculate` | ROI and break-even analysis |

---

**Yash Dhone** · [Portfolio](https://yashdhone.vercel.app)