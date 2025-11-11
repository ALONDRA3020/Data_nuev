import pandas as pd

# Ruta del dataset original
ruta_original = "/home/alondraac63/datasets /datasets/NSL-KDD/KDDTrain+.txt"

# Columnas exactas según el archivo .arff
columnas = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'label', 'difficulty'
]

# Leer el dataset original
df = pd.read_csv(ruta_original, names=columnas, header=None)

# Insertar columna ID al inicio
df.insert(0, 'id', range(1, len(df) + 1))

# Reducir el tamaño (5% de los datos para Render)
df_reducido = df.sample(frac=0.05, random_state=42)

# Guardar dataset limpio y reducido
ruta_salida = "NSL-KDD_reducido.csv"
df_reducido.to_csv(ruta_salida, index=False)