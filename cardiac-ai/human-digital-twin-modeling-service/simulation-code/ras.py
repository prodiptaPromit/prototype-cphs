import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.integrate import solve_ivp

import digital_patient
from scipy import interpolate

from digital_patient.conformal.base import RegressorAdapter
from digital_patient.conformal.icp import IcpRegressor
from digital_patient.conformal.nc import RegressorNc


def main():
    result_dir = 'results/RAS/'
    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)

    x_ras = pd.read_csv(
        'data/70/DKD_drug-5_glu-17_infection-0_renal-normal.csv')
    x_ras.drop(['angII_norm', 'IR'], axis=1, inplace=True)
    x_diabetes = pd.read_csv('data/70/DIABETES_glu-5.csv')
    tx_ras = x_ras['t']
    tx_diabetes = x_diabetes['t']

    t = np.linspace(3, 4.99, 200)

    x_list = []
    for c in x_ras.columns:
        f = interpolate.interp1d(tx_ras, x_ras[c].values)
        x_list.append(f(t))

    x = np.vstack(x_list).T
    x = x.astype('float32')
    t2 = t

    reps = 20
    x = np.tile(x.T, reps=reps).T
    t2 = np.arange(0, len(x)) / (np.max(t) * reps)
    x[:, 0] = t2

    scaler = StandardScaler()
    scaler = scaler.fit(x)
    x = scaler.transform(x)

    window_size = 1000
    samples = []
    labels = []
    t_list = []
    for batch in range(x.shape[0]-2*window_size+1):
        print(
            f"{batch} - {batch+window_size-2} -> {batch+window_size-1} - {batch+2*window_size-3}")
        samples.append(x[batch:batch+window_size-2])
        labels.append(x[batch+window_size-1:batch+2*window_size-3])
        t_list.append(t2[batch+window_size-1:batch+2*window_size-3])

    samples = np.array(samples)
    labels = np.array(labels)
    t_list = np.array(t_list)

    skf = KFold(n_splits=5, shuffle=True)
    trainval_index, test_index = [split for split in skf.split(samples)][0]
    skf2 = KFold(n_splits=5, shuffle=True)
    train_index, val_index = [split for split in skf2.split(
        np.arange(trainval_index.size))][0]
    x_train, x_val = samples[trainval_index[train_index]
                             ], samples[trainval_index[val_index]]
    y_train, y_val = labels[trainval_index[train_index]
                            ], labels[trainval_index[val_index]]
    x_test, y_test = samples[test_index], labels[test_index]
    t_list = t_list[test_index]

    dp = digital_patient.DigitalPatient(
        epochs=30, lr=0.01, window_size=window_size-2)
    elist = [
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (0, 7), (0, 8), (0, 9), (0, 10),
        (4, 1), (3, 1), (1, 7), (1, 5), (6, 5), (5, 3),
        (5, 7), (5, 8), (5, 9), (10, 7), (10, 1)
    ]
    dp.build_graph(elist)

    nx_G = dp.G_.to_networkx()
    pos = nx.circular_layout(nx_G)
    node_labels = {}
    for i, cn in enumerate(x_ras.columns):
        node_labels[i] = cn
    plt.figure()
    nx.draw(nx_G, pos, alpha=0.3)
    nx.draw_networkx_labels(nx_G, pos, labels=node_labels)
    plt.tight_layout()
    plt.savefig(f'{result_dir}/graph.png')
    plt.show()

    underlying_model = RegressorAdapter(dp)
    nc = RegressorNc(underlying_model)
    icp = IcpRegressor(nc)
    icp.fit(x_train, y_train)
    icp.calibrate(x_val, y_val)
    predictions = icp.predict(x_test, significance=0.01)

    sns.set_style('whitegrid')

    for i, name in enumerate(x_ras.columns):
        for j in range(predictions.shape[0]):
            xi = y_test[j, :, i]
            pi = predictions[j, :, i]
            ti = t_list[j]

            plt.figure()
            plt.plot(ti, xi, label='true')
            plt.fill_between(ti, pi[:, 0], pi[:, 1],
                             alpha=0.2, label='predicted')
            plt.title(name)
            plt.legend()
            plt.ylabel('concentration [ng/mL]')
            plt.xlabel('t [days]')
            plt.tight_layout()
            plt.savefig(f'{result_dir}/{name}_{j}.png')
            plt.show()
            break

    return


if __name__ == '__main__':
    main()
