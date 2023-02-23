from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from digital_patient._patient import DigitalPatient
from digital_patient.conformal import cp, base, evaluation, icp
from digital_patient.conformal.base import RegressorAdapter
from digital_patient.conformal.icp import IcpRegressor
from digital_patient.conformal.nc import RegressorNc
from digital_patient.load_data import load_physiology
from digital_patient.plot_graph import plot_graph

import os
import dgl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
import joblib
import digital_patient
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "HumanDigitalTwinModelingService.settings")
django.setup()


class DigitalTwinViewSet(viewsets.ViewSet):
    
    @csrf_exempt
    @require_http_methods(['POST'])
    def HumanDigitalTwinModeling(request):
        data = request.POST

        if request.method == 'POST' and request.FILES:
            # Collection of multi-scale datasets provided by patient
            dataset = request.FILES['dataset']
            save_dir = '~/datasets'
            with open(save_dir + dataset.name, 'wb+') as destination:
                for chunk in dataset.chunks():
                    destination.write(chunk)
        else:
            return JsonResponse({'status': 'error', 'message': 'No datasets received.'})

        try:
            # create directory to save results
            result_dir = 'results/patient-old5/'
            if not os.path.isdir(result_dir):
                os.makedirs(result_dir)

            # load data
            window_size = 500
            x_train, y_train, x_val, y_val, x_test, y_test, edge_list, addendum, scaler = load_physiology(
                window_size)
            joblib.dump(scaler, f'{result_dir}scaler.joblib')

            # instantiate a digital patient model
            G = dgl.DGLGraph(edge_list)

            dp = digital_patient.DigitalPatient(
                G, epochs=20, lr=0.01, window_size=window_size-2)

            # plot the graph corresponding to the digital patient
            nx_G = dp.G.to_networkx()
            pos = nx.spring_layout(nx_G)
            node_labels = {}
            for i, cn in enumerate(list(addendum["RAS"][1]) + list(addendum["CARDIO"][1])):
                node_labels[i] = cn

            # instantiate the model, train and predict
            dp.fit(x_train, y_train)
            predictions = dp.predict(x_test)

            # plot the results
            sns.set_style('whitegrid')
            for i, name in enumerate(list(addendum["RAS"][1]) + list(addendum["CARDIO"][1])):
                for j in range(predictions.shape[0]):
                    xi = y_test[j, :, i]
                    pi = predictions[j, :, i]

                    if name == 't' or name == 't2':
                        continue

                    if name in addendum["RAS"][1]:
                        ti = addendum["RAS"][0][j]
                        ylabel = 'concentration [ng/mL]'
                        xlabel = 't [days]'
                    else:
                        ti = addendum["CARDIO"][0][j]
                        ylabel = 'pressure [mmHg]'
                        xlabel = 't [sec]'

                    tik = np.repeat(ti, pi.shape[0])
                    pik = np.hstack(pi)

                    df = pd.DataFrame(
                        np.vstack([ti[np.newaxis, :], xi[np.newaxis, :], pi]).T)
                    df.to_csv(f'{result_dir}/{name}_{j}.csv')

                    plt.figure()
                    plt.plot(ti, xi, label='true')
                    for pik in pi:
                        plt.plot(ti, pik, c='r', alpha=0.2)
                    plt.title(name)
                    plt.legend()
                    plt.ylabel(ylabel)
                    plt.xlabel(xlabel)
                    plt.tight_layout()
                    plt.savefig(f'{result_dir}/{name}_{j}.png')
                    # plt.show()
                    break
        except Exception as error:
            return JsonResponse({'Error': error})

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
