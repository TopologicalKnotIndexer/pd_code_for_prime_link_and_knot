# prime-link-knot-10

Provide the prime knot and link catalogue used by the TopLink generator.

## Installation

```bash
pip install prime-link-knot-10
```

## Usage example

```python
import prime_link_knot_10

catalogue = prime_link_knot_10.load_pd_code()
print(catalogue["K3a1"])
print(prime_link_knot_10.get_all_prime_under10()[:5])
print("K4a1" in prime_link_knot_10.load_amphicheiral())
```

## Algorithm

Package data is loaded once and cached in deterministic filename order. Every name and PD record is validated, duplicate definitions are rejected, and mirror duplicates of amphicheiral objects are omitted. Names are sorted structurally by crossing number, object type, alternating class, table index, and mirror status. A pruned depth-first multiset enumeration supplies every non-empty prime-factor combination up to a validated crossing bound.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

No external software is required. All catalogue files are included in the wheel and sdist.

## Development

Python 3.10 or newer is required. Run the catalogue and enumeration tests with the declared `link-rep` dependency available:

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of repository maintenance.

## License

MIT. See `LICENSE`.
