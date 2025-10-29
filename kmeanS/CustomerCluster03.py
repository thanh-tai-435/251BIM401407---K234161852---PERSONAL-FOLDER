# ============================================
# CUSTOMER CLUSTERING (K-Means K=6 - 3D Visualization)
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import plotly.express as px
from K23416_retail.connector.connector import Connector    # ✅ dùng class tái sử dụng
import plotly.io as pio
pio.renderers.default = "browser"
# ----------------------------
# 1️⃣ Kết nối CSDL
# ----------------------------
conn = Connector(
    server="localhost",
    port=3306,
    database="salesdatabase",
    username="root",
    password="pipinp123A@"
)
db = conn.connect()

# ----------------------------
# 2️⃣ Lấy dữ liệu phục vụ Clustering
# ----------------------------
sql = """
SELECT DISTINCT customer.CustomerID, Age, Annual_Income, Spending_Score
FROM customer, customer_spend_score
WHERE customer.CustomerID = customer_spend_score.CustomerID;
"""
df3 = conn.queryDataset(sql)
df3.columns = ["CustomerID", "Age", "Annual Income", "Spending Score"]
print(df3.head())

# ----------------------------
# 3️⃣ Elbow method để xác định K
# ----------------------------
def elbowMethod(df, cols):
    X = df.loc[:, cols].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n, init='k-means++', max_iter=500, random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(1, 11), inertia, 'bo-')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
    plt.title('Elbow Method for Optimal K (3D features)')
    plt.grid(True)
    plt.show()

# ----------------------------
# 4️⃣ Chạy Elbow + chọn K=6
# ----------------------------
columns = ['Age', 'Annual Income', 'Spending Score']
elbowMethod(df3, columns)
print("👉 Elbow point ~ K = 6")

# ----------------------------
# 5️⃣ Chạy K-Means với K=6
# ----------------------------
X = df3.loc[:, columns].values
cluster = 6
model = KMeans(n_clusters=cluster, init='k-means++', max_iter=500, random_state=42)
labels = model.fit_predict(X)
centroids = model.cluster_centers_

df3["Cluster_K6"] = labels

print("\n🎯 Một số nhãn cụm:")
print(df3["Cluster_K6"].value_counts())
print("\n📍 Tọa độ tâm cụm:")
print(pd.DataFrame(centroids, columns=columns))

# ----------------------------
# 6️⃣ Biểu đồ 3D bằng Plotly
# ----------------------------
fig = px.scatter_3d(
    df3,
    x="Age",
    y="Annual Income",
    z="Spending Score",
    color="Cluster_K6",
    hover_data=["CustomerID", "Age", "Annual Income", "Spending Score"],
    title="Customer Clusters (Age - Annual Income - Spending Score) [K=6]",
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig.update_traces(marker=dict(size=6))
fig.show()

conn.disConnect()
