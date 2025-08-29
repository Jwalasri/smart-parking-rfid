# Smart Parking with RFID

Simulate a smart parking system that uses RFID tags for entry/exit and tracks occupancy over time. Includes a pipeline for merging events with a tag registry and a placeholder hook for computer‑vision based occupancy detection.

## Problem → Approach → Results → Next Steps

- **Problem.** Parking facilities need to track access and occupancy efficiently using low‑cost hardware; manual counts or expensive parking cameras are not ideal.
- **Approach.** Created a registry of RFID tags and a gate event simulator. The ETL pipeline merges events with the registry to maintain occupancy state and compute a placeholder occupancy score. The design includes a hook for a computer‑vision model (e.g., YOLO or ResNet) to verify occupancy using camera feeds.
- **Results.** Processes 120 simulated minutes of events with clear logs; modular design allows plugging in YOLO/ResNet for real occupancy detection.
- **Next steps.** Integrate a camera model for stall detection; implement anti‑tailgating rules; expose REST endpoints for live dashboards; evaluate accuracy against labeled camera footage.

## Installation

```bash
git clone https://github.com/yourname/smart-parking-rfid.git
cd smart-parking-rfid
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

### Simulate Gate Events

```bash
python src/simulate_gate.py --duration 120 --tags 50 --output data/events.csv
```

### Run the Pipeline

```bash
python src/pipeline.py --registry data/registry.csv --events data/events.csv --output data/occupancy.csv
```

This merges the RFID registry with event logs and computes occupancy over time.

### Add Computer Vision

The file `src/cv_hook.py` contains a stub where you can integrate a computer‑vision model for stall detection. Replace the stub with a call to your model.

## Project Structure

```
smart-parking-rfid/
├── src/
│   ├── registry.py
│   ├── simulate_gate.py
│   ├── pipeline.py
│   └── cv_hook.py
├── data/
├── tests/
├── requirements.txt
├── .gitignore
├── .github/workflows/python-ci.yml
├── LICENSE
└── README.md
```

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.