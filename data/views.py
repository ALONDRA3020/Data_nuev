import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Para generar gráficas sin interfaz
import matplotlib.pyplot as plt
import io, base64
from django.shortcuts import render
from scipy.io import arff
from sklearn.model_selection import train_test_split

def index(request):
    context = {}
    if request.method == 'POST':
        url = request.POST.get('dataset_url')

        try:
            # Cargar dataset desde URL .arff
            data, meta = arff.loadarff(url)
            df = pd.DataFrame(data)
            df['protocol_type'] = df['protocol_type'].astype(str)

            # Reducir dataset al 20%
            df = df.sample(frac=0.2, random_state=42)
            df.to_csv('dataset_reducido.csv', index=False)

            # División estratificada
            train_set, temp_set = train_test_split(df, test_size=0.4, stratify=df['protocol_type'], random_state=42)
            val_set, test_set = train_test_split(temp_set, test_size=0.5, stratify=temp_set['protocol_type'], random_state=42)

            # Longitudes
            context['len_df'] = len(df)
            context['len_train'] = len(train_set)
            context['len_val'] = len(val_set)
            context['len_test'] = len(test_set)

            # Graficar y guardar en base64
            figs = []
            for dataset, name in zip([df, train_set, val_set, test_set],
                                     ['Dataset Completo (Reducido 20%)', 'Training Set', 'Validation Set', 'Test Set']):
                fig, ax = plt.subplots()
                dataset['protocol_type'].value_counts().plot(kind='bar', ax=ax)
                ax.set_title(name)
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                plt.close(fig)
                buf.seek(0)
                image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                figs.append(image_base64)

            context['plots'] = figs
            context['success'] = True

        except Exception as e:
            context['error'] = f"Error al cargar el dataset: {e}"

    return render(request, 'index.html', context)