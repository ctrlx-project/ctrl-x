## Getting Started

This project requires these dependencies:
- docker
- python 3.10

To run the project, you can use the following commands. Run `make` to see the available targets. 
Some of them are not implemented yet.

```bash
make scan <ip or subnet> # Scan the subnet or ip and adds the results to the db (requires root)
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