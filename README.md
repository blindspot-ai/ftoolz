# ftoolz
[![Build Status](https://travis-ci.com/blindspot-ai/ftoolz.svg?branch=master)](https://travis-ci.com/blindspot-ai/ftoolz) [![Coverage Status](https://coveralls.io/repos/github/blindspot-ai/ftoolz/badge.svg?branch=master)](https://coveralls.io/github/blindspot-ai/ftoolz?branch=master) [![PyPI version](https://badge.fury.io/py/ftoolz.svg)](https://badge.fury.io/py/ftoolz) [![PyPI status](https://img.shields.io/pypi/status/ftoolz.svg)](https://pypi.python.org/pypi/ftoolz/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ftoolz.svg)](https://pypi.python.org/pypi/ftoolz/)

Collection of higher-order and utility functions built on top of `cytoolz`.

## Module overview
Ftoolz are split into few generic modules.

### functoolz package
Package that provides higher-order functions commonly associated with Functor, Applicative and Monad. 

Moreover, there are general package-level functions implemented in `__init__.py`.
 
| Function | Description |
|----------|-------------|
| `attempt(ex, f, args, kwargs)` | equivalent to `try_except` with `g = lambda _: None` |
| `chain(*fs)` | reversed function composition `chain(f, g) = g o f` |
| `silence(errors)` | decorator that silences (selected/all) errors raised by decorated function |
| `try_apply(f, args, kwargs)` | equivalent to `attempt` with `ex = Exception` |
| `try_except(ex, f, g, args, kwargs)` | `f(args, kwargs)` and on exception(s) `ex` fallback to `g(args, kwargs)` |

The package content is organized into modules by individual type class:
1. `iter.py` for class `Iterable`. **Warn** some functions might not be pure because input iterable is consumed.
1. `opt.py` for class `Optional` 
1. `seq.py` for class `Seq` (`Sequece`). Methods typically return `tuple` instances to preserve immutability.

#### Module function overview
| def / .py | iter | opt | seq |
|-----------|------|-----|-----|
|`apply`| x | x | x |
|`apply2`| - | x | - |
|`applyN`| - | + | - |
|`flatmap`| x | x | x |
|`flatten`| x | x | x |
|`fmap`| x | x | x |
|`fmap2`| x | x | x |
|`fmap3`| - | x | - |
|`fmapN`| - | + | - |
|`fproduct`| x | x | x |
|`generate`| x | - | x |
|`lift`| x | x | x |
|`product`| x | x | x |
|`unit`| x | * | x |
|`zip_map`| + | - | + |

* `x` - implemented, statically type checked
* `+` - implemented, possible runtime type errors
* `*` - not implemented, supported natively
* `-` - not implemented 

#### traverse package
Each module contains traversable-related functions for traversables `Iterable` and `Seq`. 
Individual modules are named and reserved for single functor that wraps elements of the traversable sequence.

List of currently implemented functions in modules (functors): 

| def / .py | opt |
|-----------|-----|
|`sequence_iter`| x |
|`sequence_seq`| x |
|`traverse_iter`| x |
|`traverse_iter`| x |

### unsafe package
Package `unsafe` is dedicated to all *impure* functions that are prone to or 
will directly use side-effects.

#### reflection
This module contains functions for class discovery, inspection and 
modifications.

Table of contents

| Function | Description |
|----------|-------------|
| `abstract(type)` | `True` iff `type` has abstract methods |
| `implementations(type, package)` | discover all non-protected implementations of `type` under `package` |
| `import_all(package)` | recursively import everything under `package` |
| `protected(type)` | `True` iff `type` defines attribute `__protected__ = True` |
| `subclasses(type, package)` | discover all subclasses of `type` under `package` |

### dicttoolz
This module contains functions that work with `Map` (`Mapping`) instances.

Table of contents

| Function | Description |
|----------|-------------|
| `map_val(dict, key, f)` | apply value transformation `f` on value in `dict` under `key` |
| `swap(dict, key1, key2)` | swap arbitrary values for `key1` and `key2` in given mapping |
| `swap_values(dict, key1, key2)` | same as `swap` but preserving concrete value type `V` |

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
| `fold_right(op, iterable, z)` | fold iterable by applying binary operator `op` from the *right* |
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

Ftoolz does not fork but rather extends cytoolz and provides typed stubs for it's API. 
Please note that the typed stubs do not cover all the functions from cytoolz. 

Also some valid cases might not be covered due to Python's restricted typing capabilities.

## Setup development environment
It is highly recommended to use virtual environment to develop and test `ftoolz`. For making things easy there are 
two make targets to setup `ftoolz`:
* `make setup` which creates new virtual environment managed by `pipenv` with both dev and `ftoolz` dependencies.
* `make install` same as `make setup` but installs `ftoolz` dependencies only.

To python console in [pipenv](https://pipenv.readthedocs.io/en/latest/) environment, run:
```bash
pipenv shell
```
and for running specific command:
```bash
pipenv run <command>
```

## Running checks and tests

### Type checking
Type checking is done using `mypy` (for configuration see `mypy.ini`) and can be executed by:
```bash
make type-check
```

### Code style checking
Ftoolz uses [Flake8](http://flake8.pycqa.org/en/latest/index.html) for enforcing PEP 8 and other code smells.
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

*Note*: All these commands run on python managed by `pipenv`.

## Distribution
Project uses `setuptools` for distribution. Check settings in `setup.py`.
