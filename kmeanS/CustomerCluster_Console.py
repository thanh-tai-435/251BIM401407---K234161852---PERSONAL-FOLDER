from customer_clustering import CustomerClustering

if __name__ == "__main__":
    cc = CustomerClustering(k=6, features=['Age', 'Annual Income', 'Spending Score'])
    cc.load_data()
    cc.train_model()
    cc.show_clusters_console()
    cc.close_connection()
