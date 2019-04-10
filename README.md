# pytoolz

Collection of higher-order and utility functions built on top of `cytoolz`.

## Module overview
Pytoolz are split into few generic modules.

### itertoolz
This module contains functions that work with `Iterable` instances.

Table of contents

| Function | Description |
|----------|-------------|
| `associate(key_fn, iterable)` | associate elements of iterable to keys selected by `key_fn` |
| `associate_to(key_fn, value_fn, iterable)` | associate values obtained from iterable by `value_fn` to keys 
selected by `key_fn` |
| `collect(iterable)` | materialize iterable into a sequence if it's not one already |
| `empty(iterable)` | check if iterable is empty, returns flag and unchanged iterable |
| `enumerate_with_final(iterable)` | same as `iter_with_final` but adds index as third part |
| `filter_not_none(iterable)` | filter out `None` elements from iterable |
| `find(predicate, iterable)` | find first element of iterable satisfying predicate |
| `first(sequence)` | return first element of a sequence or `None` |
| `head_tail(iterable)` | split iterable into head element and tail iterable |
| `head_tail_list(iterable)` | same as `head_tail` but materialized tail into list |
| `iter_with_final(iterable)` | creates iterable of tuples of original element and final flag |
| `last(sequence)` | return last element of a sequence or `None` |
| `make_str(iterable, key_fn, separator)` | create string of tokens from iterable selected by `key_fn` with separator |
| `split_by(predicate, iterable)` | split elements of iterable by predicate to positives and negatives |
| `take(n, iterable)` | take first n elements of an iterable |
| `take_first(iterable)` | take first element of an iterable or fail |
| `try_take_first(iterable)` | same as `take_first` but returns `None` |
| `try_take_last(iterable)` |  take last element of an iterable or `None` |
| `unique_list(iterable)` |  return distinct elements of an iterable as `Seq` |
| `unique_sorted(iterable)` |  return distinct elements of an iterable in natural order as `Seq` |

### predicates
This module contains common `Predicate`s, i.e. functions from generic or concrete `A` to `bool`.

Table of contents

| Predicate | Description |
|-----------|-------------|
| `some(optional)` | `True` iff optional *is not* `None` |
| `none(optional)` | `True` iff optional *is* `None` |
| `even(integer)` | `True` iff integer is even |
| `odd(integer)` | `True` iff integer is odd |

### typing
Typing contains helpful type aliases and other type-related definitions.

## cytoolz
Cytoolz is a cython implementation of a python library supporting functional style called 
[toolz](https://toolz.readthedocs.io).

We highly recommend reading the API docs and using it in your project.

Pytoolz does not fork but rather extends cytoolz and provides typed stubs for it's API. 
Please note that the typed stubs do not cover all the functions from cytoolz. 

Also some valid cases might not be covered due to Python's restricted typing capabilities.

## Setup development environment
It is highly recommended to use virtual environment to develop and test `pytoolz`. For making things easy there are 
two make targets to setup `pytoolz`:
* `make setup-dev` which creates new virtual environment in `./venv`
* `make setup` that just installs dependencies for development

Of course one can use his/her own favourite tool to create and manage python venv.

To activate the prepared venv run:
```bash
source venv/bin/activate
```
and for deactivation simply `deactivate`.

## Running checks and tests

### Type checking
Type checking is done using `mypy` (for configuration see `mypy.ini`) and can be executed by:
```bash
make type-check
```

### Code style checking
Pytoolz uses [Flake8](http://flake8.pycqa.org/en/latest/index.html) for enforcing PEP 8 and other code smells.
```bash
make flake8-check
``` 

### Linting
Linting is configured in `.pylintrc` and can be run via:
```bash
make lint
```

### Tests
Unit and doc tests with coverage can be run by
```bash
make tests
```

One can also run all checks and tests at once via
```bash
make release-check
```

*Note*: Make sure you run these commands in an activate venv or a container.

## Distribution
Project uses `setuptools` for distribution. Check settings in `setup.py`.
