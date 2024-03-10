## Getting Started

This project requires these dependencies:
- docker
- python 3.10

Run `make` to see the available targets. 
Main app is available at `http://localhost:5000` and the daemon at `http://localhost:8000` in dev mode.

```bash
make dev # Start the database, main app and the scanner daemon
``` 

```bash
make stop # Stop the database (will be replaced by an interrupt handler later)
```

```bash
make clean # Stop the db, removes virtual environment and the db container. Data is kept
```

```bash
make reset # Similar to clean, but also removes the data
```

## Note
- If you're on windows, use WSL to run the project. Do not clone this repo into a mounted directory - performance will 
be terrible and virtual environment may not work.