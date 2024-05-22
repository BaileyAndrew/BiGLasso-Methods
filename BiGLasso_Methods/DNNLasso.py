"""
This is a python wrapper for TeraLasso
"""

import matlab.engine
import io
import os
import numpy as np
from GmGM import Dataset
from GmGM.core.preprocessing import create_gram_matrices
from GmGM.typing import Axis
import scipy.sparse as sparse

eng = matlab.engine.start_matlab()
path = os.path.dirname(os.path.abspath(__file__))
eng.addpath(
    f'{path}/DNNLasso'
)


def DNNLasso(
    dataset: Dataset,
    beta: float,
    use_nonparanormal_skeptic: bool = False,
    max_iter: int = 100,
    tol: float = 1e-8
) -> Dataset:
    if len(dataset.dataset) != 1:
        raise ValueError(
            'DNNLasso only supports one dataset'
        )
    if len(dataset.batch_axes) == 0:
        raise ValueError(
            "Please make the first axis of the dataset a batch axis!"
        )
    tensor = list(dataset.dataset.values())[0]
    if tensor.ndim != 3:
        raise ValueError(
            'DNNLasso only supports two-dimensional (i.e. matrix-variate) datasets, with a batch axis.'
        )
    structure = list(dataset.structure.values())[0]
    if structure[0] != '':
        tensor = tensor.reshape(1, *tensor.shape)
    _, *d = tensor.shape
    K = len(d)
    
    dataset = create_gram_matrices(
        dataset,
        use_nonparanormal_skeptic=use_nonparanormal_skeptic,
    )
    Ss = {
        axis: matlab.double(matrix)
        for axis, matrix
        in dataset.gram_matrices.items()
    }

    d_matlab = matlab.double(d)
    betas_matlab = matlab.double([beta for _ in range(K)])
    tol_matlab = matlab.double(tol)

    _, Psi_matlab, Theta_matlab = eng.DNNLasso(
        *[matrix for _, matrix in Ss.items()],
        *betas_matlab,
        tol_matlab,
        max_iter,
        nargout=3,
        stdout=io.StringIO()
    )
    Psis = [Psi_matlab, Theta_matlab]
    
    Psis = {
        axis: sparse.csr_array(np.asarray(Psis[i]))
        for i, axis in enumerate(Ss.keys())
    }
    
    dataset.precision_matrices = Psis
    return dataset