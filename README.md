# facility\_location\_game

**One-line Description:** This project holds a simulation for a Facility Location Game developed in Python with players under Best Response Dynamics behavior.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Graph-based environment:**
  - Undirected, weighted tree graph where nodes represent demand locations and potential facility sites.
  - Edge weights model service cost; node weights model client demand.
- **Demand assignment:**
  - Each customer demand is assigned to its closest facility, based on shortest-path distance; ties broken at random.
- **Best Response Dynamics (BRD):**
  - Players iteratively relocate to maximize individual utility, converging to a pure Nash equilibrium in this potential game setting.
- **Visualization:**
  - After each simulation, plots of players’ utilities over time, facility-position changes, and the evolution of the global potential function are generated using Matplotlib.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/burjand/facility_location_game.git
   cd facility_location_game
   ```
2. **Create a Python 3.12 virtual environment**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Required packages include NumPy, NetworkX, Matplotlib, Statistics, and JSON5.

---

## Usage

The file Documentation_FLG_BRD_environment.pdf contains the essential Math concepts to understand the simulation.

Configure the simulation parameters in the provided configuration file or directly in `main.py`, then run:

```bash
python main.py
```

This will execute the basic Facility Location Game simulation with BRD and produce plots in the `output/` directory.

---

## Future Improvements

- **Dynamic edge weights:** Model time-varying travel costs (e.g., congestion) fileciteturn0file0.
- **Capacitated facilities:** Add capacity constraints and overflow handling for more realistic equilibria fileciteturn0file0.
- **Stochastic demand:** Incorporate evolving and random client demand profiles fileciteturn0file0.
- **Multi-criteria preferences:** Extend to client loyalty or price sensitivity models.
- **Regulatory RL Agent:** Integrate reinforcement learning–based regulation to influence dynamics.

---

## Contributing

For now, contributions are managed by the project owner. If you wish to report issues or suggest enhancements, please reach out via email:

> Andrés Burjand Torres Reyes [andresbur.torresreyes@gmail.com](mailto\:andresbur.torresreyes@gmail.com)

---

## License

This project is released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license. You are free to use, share, and adapt the work for non-commercial purposes. For any commercial use or recognition, please contact the author.

---

## Contact

**Author:** Andrés Burjand Torres Reyes\
Email: [andresbur.torresreyes@gmail.com](mailto\:andresbur.torresreyes@gmail.com)

---

*Acknowledgements:* Developed under the supervision of PhD. Rolando Menchaca as part of the author’s Master’s thesis work.
