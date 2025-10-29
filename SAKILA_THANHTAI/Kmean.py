# kmeans_cluster.py
from connector.connector import Connector
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def load_features(conn):
    sql = """
    SELECT 
        c.customer_id,
        COUNT(r.rental_id) AS rental_count,
        AVG(DATEDIFF(r.return_date, r.rental_date)) AS avg_duration
    FROM customer c
    JOIN rental r ON c.customer_id = r.customer_id
    GROUP BY c.customer_id;
    """
    return conn.queryDataset(sql)

def kmeans_cluster(df, n_clusters=3):
    X = df[['rental_count', 'avg_duration']].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    df.to_csv("output/customer_clusters.csv", index=False)
    print("✅ Đã lưu output/customer_clusters.csv")
    return df

def plot_clusters(df):
    plt.scatter(df['rental_count'], df['avg_duration'], c=df['cluster'], cmap='viridis')
    plt.xlabel('Rental Count')
    plt.ylabel('Avg Duration')
    plt.title('Customer Clusters (KMeans)')
    plt.savefig("output/customer_clusters.png")
    plt.show()

if __name__ == "__main__":
    conn = Connector()
    df = load_features(conn)
    df_clustered = kmeans_cluster(df)
    print(df_clustered.groupby('cluster').mean())
    plot_clusters(df_clustered)
