# WDT_Analysis

A package to analyze the figure of merit convergence of Serpent
Monte-Carlo simulations.

The `Analysis` package contains two modules:

- `core`, which contains the `DataFile` object used to contain Serpent
  output data.

- `fom`, which contains the tools for analyzing multiple `DataFiles`

An iPython notebook outlining its use is included [here](WDT_analysis.ipynb).

Full documentation can be built in the `docs` folder using:

```
make html
```

Tests can be run using `nosetests` in the main directory.

## Dependencies:

- [PyNE](https://github.com/pyne/pyne)
