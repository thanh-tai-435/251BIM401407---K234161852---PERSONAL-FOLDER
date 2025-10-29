from flask import Flask, render_template, request
from customer_clustering import CustomerClustering
import plotly.express as px
import json
import plotly
app = Flask(__name__)

@app.route("/", methods=["GET"])
def clusters():
    # Khởi tạo mô hình
    cc = CustomerClustering(k=6, features=['Age', 'Annual Income', 'Spending Score'])
    cc.load_data()
    cc.train_model()
    clusters_dict = cc.get_cluster_data()
    df = cc.df.copy()
    cc.close_connection()

    # Tạo biểu đồ 3D Plotly
    fig = px.scatter_3d(
        df,
        x="Age",
        y="Annual Income",
        z="Spending Score",
        color="Cluster",
        color_continuous_scale="Rainbow",
        title="Phân cụm khách hàng (K=6)",
        hover_data=["CustomerID"]
    )
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    selected_cluster = int(request.args.get("cluster", 1))
    cluster_df = clusters_dict[selected_cluster]

    return render_template(
        "clusters.html",
        clusters=clusters_dict,
        cluster_df=cluster_df,
        selected_cluster=selected_cluster,
        fig_json=fig_json
    )

if __name__ == "__main__":
    app.run(debug=True)
