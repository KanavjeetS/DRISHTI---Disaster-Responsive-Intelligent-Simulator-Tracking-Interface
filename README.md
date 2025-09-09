# DRISTI — Disaster Responsive Intelligent Simulation & Tracking Interface

An AI-powered system for **proactive disaster management** at large-scale events (e.g., Simhastha Kumbh Mela). DRISTI uses **reinforcement learning + simulation** to optimize evacuation, resource allocation, and first-responder routing in real time.

## Key Features
- **Simulation-first training** on realistic disaster scenarios.
- **RL agents** for dynamic path planning & resource dispatch.
- **Live dashboard** for authorities with density heatmaps and asset tracking.
- **Citizen app** concepts for safe-route guidance and alerts.
- Modular, production-ready Python package layout.

## Quickstart
```bash
# 1) Create environment
conda create -n dristi python=3.11 -y
conda activate dristi

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run a minimal simulation (placeholder)
python -m dristi.simulation.run_demo

# 4) Launch dashboard (placeholder Streamlit app)
streamlit run src/dristi/dashboard/app.py
```

## Repository Layout
```
src/dristi/          # Core library
  agents/            # RL agents, policies
  envs/              # Gym/Gymnasium environments
  policies/          # Policy networks / wrappers
  simulation/        # Scenario generators, city grid, crowd models
  training/          # Train loops, configs, logging
  evaluation/        # Metrics, rollouts, test suites
  utils/             # I/O, viz, geometry, map helpers
  api/               # FastAPI service to serve routes/actions
  dashboard/         # Streamlit/Gradio dashboard (authority view)
configs/             # YAML configs for experiments
data/                # Raw & processed data (git-ignored except .keep)
models/              # Saved weights (git-ignored except .keep)
notebooks/           # Research notebooks (your hackathon notebook placed here)
docs/                # Diagrams, writeups
tests/               # pytest-based tests
```

## How it works (high level)
- **Simulation**: a grid/graph city with hazards, dynamic blockages, agent-based crowd motion.
- **Observation**: crowd density, hazard map, resource locations, map features.
- **Action**: route updates, dispatch orders, traffic control (e.g., one-way lanes), public alerts.
- **Reward**: minimize casualties, congestion, and response time; penalize dead-ends and unsafe exposure.
- **Learning**: off-policy (e.g., DQN/TD3) or on-policy (e.g., PPO) via Gymnasium envs; curriculum for difficulty scaling.

## Datasets & Maps
- Integrate map layers (OSM/GeoJSON), CCTV feeds, and simulated sensors.
- Add a `data/README.md` explaining sources and licensing (see template).

## Reproducibility
- Deterministic seeds in configs, pinned dependencies, and training logs (W&B optional).

## Roadmap
- Multi-agent coordination (ambulance, fire, police) with joint rewards.
- Partial observability + comms constraints (POMDP).
- Real-time routing API deployed behind the dashboard.
- Hardware-in-the-loop (drones/edge devices) in later phases.

## License
MIT — see `LICENSE`.
