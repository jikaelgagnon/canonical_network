<div align="center">

<h1>Canonical Network</h1>

<p><strong>Learned canonicalization for equivariant neural networks</strong></p>

<p>A research extension with a Transformer implementation, expanded documentation, and bug fixes.</p>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch">
</p>

<p>
  <a href="https://arxiv.org/abs/2211.06489">Research paper</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/oumarkaba/canonical_network">Original implementation</a>
  &nbsp;·&nbsp;
  <a href="setup.md">Setup guide</a>
</p>

<br>

<img src="https://alexjbrinson.github.io/ComputationalPhysicsLab/nBodySimulator/nBodyWithTraceHistory.gif" alt="Illustrative N-body simulation showing interacting particles and their trajectories" width="360">

<p><sub>Illustrative N-body simulation by <a href="https://alexjbrinson.github.io/nBodySim/">Alex Brinson</a>.</sub></p>

</div>

## Overview

How can a neural network recognize the same underlying structure when its input is rotated or transformed?

**Learned canonicalization** addresses this by learning to map inputs into a consistent reference frame. This allows conventional neural network architectures to be used within an equivariant framework.

This repository builds on [Kaba et al.’s implementation](https://github.com/oumarkaba/canonical_network) of [*Equivariance with Learned Canonicalization Functions*](https://arxiv.org/abs/2211.06489).

## My contributions

- **Transformer implementation** — added a Transformer architecture to extend the existing implementation.
- **Function documentation** — expanded documentation to make the code easier to understand and navigate.
- **Bug fixes** — addressed issues in the existing code.

## Explore the code

| Area | Location |
| :--- | :--- |
| Model implementations | [`canonical_network/models/`](canonical_network/models/) |
| N-body training | [`train_nbody.py`](canonical_network/train_nbody.py) |
| Image training | [`train_images.py`](canonical_network/train_images.py) |
| ModelNet training | [`train_modelnet.py`](canonical_network/train_modelnet.py) |
| ShapeNet training | [`train_shapenet.py`](canonical_network/train_shapenet.py) |
| Visualization utilities | [`canonical_network/visualization/`](canonical_network/visualization/) |

## Getting started

See the **[setup guide](setup.md)** for environment configuration, dependencies, and troubleshooting notes.

The guide documents the setup used with Windows Subsystem for Linux (WSL). The N-body dataset is not included in this repository and must be supplied separately.

## Acknowledgments

This project extends the work of **Sékou-Oumar Kaba, Arnab Kumar Mondal, Yan Zhang, Yoshua Bengio, and Siamak Ravanbakhsh**.

- [Equivariance with Learned Canonicalization Functions](https://arxiv.org/abs/2211.06489)
- [Original code repository](https://github.com/oumarkaba/canonical_network)

The illustrative animation above is credited to [Alex Brinson](https://alexjbrinson.github.io/nBodySim/).

---

<div align="center">
  <a href="https://jikaelgagnon.github.io/">Portfolio</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/jikaelgagnon">GitHub</a>
</div>
