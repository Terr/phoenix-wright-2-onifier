# Phoenix Wright 2 Onifier

Improves a Phoenix Wright 2 ROM by copying the better music from a Phoenix Wright 1 ROM. Take that!

Should work with both EU and USA ROMs interchangeably, perhaps even with the Japanese ROMs.

All the heavy lifting is done by the amazing [ndspy](https://github.com/RoadrunnerWMC/ndspy) library.

## Installation & usage

## From a binary release

Download the release for your platform.

```
pw2-onifier [path to Phoenix Wright 1 ROM] [path to Phoenix Wright 2 ROM] [path to write the modified ROM to]
```

## From source

The project uses [Poetry](https://python-poetry.org/) for dependency management.

```
cd pw2-onifier
poetry install
poetry run pw2-onifier.py [path to Phoenix Wright 1 ROM] [path to Phoenix Wright 2 ROM] [path to write the modified ROM to]
```
