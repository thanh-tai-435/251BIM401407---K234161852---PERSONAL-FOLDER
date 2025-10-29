import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from K23416_retail.connector.connector import Connector
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

class CustomerClustering:
    def __init__(self, k=4, features=None):
        self.k = k
        self.features = features or ['Age', 'Annual Income', 'Spending Score']
        self.df = None
        self.model = None
        self.conn = Connector(
            server="localhost",
            port=3306,
            database="salesdatabase",
            username="root",
            password="pipinp123A@"
        )

    # ------------------------------------------
    # 1️⃣ Load dữ liệu từ MySQL
    # ------------------------------------------
    def load_data(self):
        sql = """
        SELECT DISTINCT customer.CustomerID, Age, Annual_Income, Spending_Score
        FROM customer, customer_spend_score
        WHERE customer.CustomerID = customer_spend_score.CustomerID;
        """
        self.df = self.conn.queryDataset(sql)
        if self.df is not None:
            self.df.columns = ["CustomerID", "Age", "Annual Income", "Spending Score"]
        else:
            raise ValueError("❌ Không load được dữ liệu từ MySQL!")
        return self.df


    def train_model(self):
        if self.df is None:
            raise ValueError("Dataset chưa được load!")
        X = self.df[self.features].values
        self.model = KMeans(n_clusters=self.k, init='k-means++', max_iter=500, random_state=42)
        self.df['Cluster'] = self.model.fit_predict(X)
        return self.df


    def show_clusters_console(self):
        if 'Cluster' not in self.df.columns:
            raise ValueError("Chưa chạy train_model()!")
        print(f"\n DANH SÁCH KHÁCH HÀNG THEO CỤM (K = {self.k})")
        for i in range(self.k):
            group = self.df[self.df['Cluster'] == i]
            print(f"\n----- Cluster {i+1} -----")
            print(group.to_string(index=False))

    def get_cluster_data(self):
        """Trả về dict {cluster: DataFrame} để render trên web"""
        if 'Cluster' not in self.df.columns:
            raise ValueError("Chưa chạy train_model()!")

        clusters_dict = {}
        for i in range(self.k):
            clusters_dict[i+1] = self.df[self.df['Cluster'] == i]
        return clusters_dict    
    def close_connection(self):
        self.conn.disConnect()
if __name__ == "__main__":
    print("✅ File customer_clustering.py loaded successfully!")