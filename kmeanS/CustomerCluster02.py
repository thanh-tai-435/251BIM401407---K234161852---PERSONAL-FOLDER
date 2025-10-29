# ============================================
# CUSTOMER CLUSTERING (K-Means K=5)
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from K23416_retail.connector.connector import Connector  # ✅ dùng class tái sử dụng bạn viết trước

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
df2 = conn.queryDataset(sql)
df2.columns = ["CustomerID", "Age", "Annual Income", "Spending Score"]
print(df2.head())

# ----------------------------
# 3️⃣ Hàm xác định Elbow
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
    plt.title('Elbow Method for Optimal K')
    plt.grid(True)
    plt.show()

# ----------------------------
# 4️⃣ Hàm chạy K-Means
# ----------------------------
def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster, init='k-means++', max_iter=500, random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

# ----------------------------
# 5️⃣ Hàm trực quan hóa kết quả KMeans
# ----------------------------
def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10, 8))
    for i in range(cluster):
        plt.scatter(
            X[y_kmeans == i, 0],
            X[y_kmeans == i, 1],
            s=100,
            c=colors[i],
            label=f'Cluster {i+1}'
        )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

# ----------------------------
# 6️⃣ Thực nghiệm gom cụm K=5
# ----------------------------
columns = ['Annual Income', 'Spending Score']
print("\n🔹 Xác định K bằng Elbow cho", columns)
elbowMethod(df2, columns)

# theo slide, elbow point ở K = 5
cluster = 5
X = df2.loc[:, columns].values
colors = ["red", "green", "blue", "purple", "orange"]

y_kmeans, centroids, labels = runKMeans(X, cluster)
df2["Cluster_K5"] = labels

# In kết quả mẫu
print("\n🎯 Kết quả phân cụm (K=5):")
print(df2.head())
print("\n📍 Tọa độ tâm cụm:")
print(pd.DataFrame(centroids, columns=columns))

# ----------------------------
# 7️⃣ Trực quan hóa
# ----------------------------
visualizeKMeans(
    X,
    y_kmeans,
    cluster,
    title="Customer Clusters (Annual Income vs Spending Score) - K=5",
    xlabel="Annual Income",
    ylabel="Spending Score",
    colors=colors
)

conn.disConnect()
