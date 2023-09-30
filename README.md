# sfcollapse

Scalar field collapse exploration tool leveraging on [nrpytutorial](https://github.com/zachetienne/nrpytutorial).

## Quickstart

```
# get nrpytutorial tagged repo
TAG=ET_2022_11_v0; git clone --depth=1 --branch=${TAG} https://github.com/zachetienne/nrpytutorial.git "nrpytutorial-${TAG}"
git clone URL
cd sfcollapse
pyseed=/path/python3.10.x make development
make install-nrpy
```

## Usage

### General remark

The `nrpy` module uses global state to communicate `C` modules being loaded and
synchronized. That comes with certain drawbacks, such as that user cannot relay
on not having unexpected changes, e.g. `ScalarField` python module contains also
header files for the functionality; those are copied into production. From
loading the module in python to building the source code and compilation they
might be altered due to the `ScalarField` package (which contains them) or other
loaded module.

The approach in the project installs `nrpy` modules using symbolic links. It
also creates a `build` environment to run notebooks with symbolic links pointing
to header home. Meaning if a change occurs due to loading the module, or
somewhere in between, it will be in sync with the one hard copied from same
place.

Try out `make setup-sfcollapse` and explore its recipes.
