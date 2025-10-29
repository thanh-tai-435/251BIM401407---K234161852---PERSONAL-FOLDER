from flask import Flask
from flask_mysqldb import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pipinp123A@'
app.config['MYSQL_DB'] = 'salesdatabase'

mysql = MySQL(app)

def queryDataset(sql):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=cols)
        cur.close()
        return df

def showHistogram(df, columns):
    plt.figure(1, figsize=(7, 8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.histplot(df[column], bins=32, kde=True)
        plt.title(f'Histogram of {column}')
    plt.show()

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(
            n_clusters=n,
            init='k-means++',
            max_iter=500,
            random_state=42
        )
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize=(10, 6))
    plt.plot(np.arange(1, 11), inertia, 'bo-')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Cluster sum of squared distances (WCSS)')
    plt.title('Elbow Method for Optimal K')
    plt.grid(True)
    plt.show()

def runKMeans(X, cluster):
    model = KMeans(
        n_clusters=cluster,
        init='k-means++',
        max_iter=500,
        random_state=42
    )
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels

def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10, 10))
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

if __name__ == "__main__":
    sql = """
    SELECT DISTINCT customer.CustomerID, Age, Annual_Income, Spending_Score
    FROM customer, customer_spend_score
    WHERE customer.CustomerID = customer_spend_score.CustomerID;
    """
    df2 = queryDataset(sql)
    df2.columns = ["CustomerID", "Age", "Annual Income", "Spending Score"]
    print(df2.head())
    print(df2.describe())
    showHistogram(df2, df2.columns[1:])
    columns = ['Age', 'Spending Score']
    elbowMethod(df2, columns)
    print("👉 Elbow point xác định K = 4")
    # Chạy KMeans với K=4
    X = df2.loc[:, columns].values
    cluster = 4
    colors = ["red", "green", "blue", "purple", "orange", "pink"]
    y_kmeans, centroids, labels = runKMeans(X, cluster)
    print("Labels:", labels[:10])
    print("Centroids:\n", centroids)
    # Thêm cột cluster vào df2
    df2["Cluster"] = labels
    # Vẽ trực quan hóa cụm
    visualizeKMeans(
        X, y_kmeans, cluster,
        title="Customer Clusters (Age vs Spending Score)",
        xlabel="Age",
        ylabel="Spending Score",
        colors=colors
    )
    print(df2.head())
