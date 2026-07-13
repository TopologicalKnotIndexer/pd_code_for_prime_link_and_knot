# prime-link-knot-10

Provide prime knot/link PD codes, component data, mirror variants, and amphicheiral names.

## Installation

```bash
pip install pd-code-for-prime-link-and-knot
```

## Quick start

`import prime_link_knot_10` then `prime_link_knot_10.load_pd_code()`.

PD codes are lists of four-entry crossings. Each arc label must occur exactly twice. Functions validate their inputs and do not mutate caller-owned PD-code lists unless explicitly documented.

## Development

Use Python 3.10 or newer for Python packages. Build distributions with `poetry build`. Run the package's tests or examples before publishing. C++ projects require a modern standards-compliant compiler.

## License

MIT. See `LICENSE`.
