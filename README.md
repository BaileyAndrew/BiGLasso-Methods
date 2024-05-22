# BiGLasso-Methods

This package Python provides wrappers for [TeraLasso](https://github.com/kgreenewald/teralasso/tree/master) and [DNNLasso](https://github.com/YangjingZhang/DNNLasso).  As they were originally written in Matlab, you will need Matlab on your machine to run them.

These are included as "git submodules", i.e. we are just wrapping whatever happens to be in their repository.

EiGLasso is git-submoduled as well, but since it requires compilation (a bit trickier to wrap), I haven't included it in the pip package.  However, downloading this repository and following EiGLasso's compilation steps would allow it to work.

## Installation

```
pip install biglasso-methods
```

### Installation Troubleshooting

If you do not have the latest Matlab version, the install may fail, with an error like:

```
RuntimeError: MATLAB R2024a installation not found. Install to default location, or add <matlabroot>/bin/maca64 to DYLD_LIBRARY_PATH, where <matlabroot> is the root of a MATLAB R2024a installation.
```

You can either solve this by installing the newest Matlab version, or finding out which version you have and [looking through PyPI](https://pypi.org/project/matlabengine/#history) to find which `matlabengine` version corresponds to your Matlab version.  For example, I had MATLAB R2023b, which works with `matlabengine 9.15`, so I ran:

```
pip install matlabengine==9.15.2
pip install biglasso-methods
```