# prime_link_knot_10
A list of pd_codes for prime knots and prime links constructed for those with ≤ 10 crossings

## Install

```bash
pip install prime-link-knot-10
```

## Usage

```python
import prime_link_knot_10

knot_name = prime_link_knot_10.get_all_prime_under10()[15]
pd_code   = prime_link_knot_10.load_pd_code()[knot_name]
print(knot_name, pd_code)
print(len(prime_link_knot_10.get_all_combination(10)))
```

## TODO

- add amphicheiral link list.
