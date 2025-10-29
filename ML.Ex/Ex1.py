import numpy as np
import matplotlib.pyplot as plt

# ===================== 1. DỮ LIỆU =====================
names = np.array([
    "John", "Peter", "Daisy", "Case", "Ronie",
    "Vitor", "Rehm", "Tom", "Bob", "Lie",
    "Tide", "Real", "Jassor"
])

X = np.array([
    [1, 1],
    [11, 12],
    [2, 3],
    [1, 2],
    [2, 6],
    [9, 8],
    [0, 1],
    [11, 10],
    [0, 2],
    [10, 11],
    [10, 12],
    [7, 4],
    [5, 6]
], dtype=float)

# ===================== 2. KHỞI TẠO =====================
# Chọn 3 tâm cụm ban đầu: Daisy(2,3), Vitor(9,8), Real(7,4)
centroids = np.array([
    [2, 3],  # Daisy
    [9, 8],  # Vitor
    [7, 4]   # Real
], dtype=float)

def euclidean(a, b):
    return np.sqrt(np.sum((a - b)**2, axis=1))

# ===================== 3. LẶP K-MEANS =====================
for step in range(5):  # lặp tối đa 5 lần
    # Gán điểm vào cụm gần nhất
    distances = np.array([euclidean(X, c) for c in centroids])  # (3, n)
    cluster_labels = np.argmin(distances, axis=0)
    
    # Tính tâm cụm mới
    new_centroids = np.array([X[cluster_labels == k].mean(axis=0) for k in range(3)])
    
    # In thông tin mỗi vòng
    print(f"\nVòng {step+1}")
    for k in range(3):
        members = names[cluster_labels == k]
        print(f"  Cụm {k+1}: tâm = {new_centroids[k]} gồm: {', '.join(members)}")
    
    # Nếu hội tụ (tâm không đổi), dừng
    if np.allclose(centroids, new_centroids):
        print("\n→ Hội tụ sau", step+1, "vòng lặp.")
        break
    centroids = new_centroids

# ===================== 4. VẼ BIỂU ĐỒ =====================
colors = ['red', 'green', 'blue']
plt.figure(figsize=(7,6))
for k in range(3):
    cluster_points = X[cluster_labels == k]
    plt.scatter(cluster_points[:,0], cluster_points[:,1],
                color=colors[k], label=f'Cụm {k+1}', s=80)
    # Hiển thị nhãn
    for i, name in enumerate(names[cluster_labels == k]):
        plt.text(cluster_points[i,0]+0.1, cluster_points[i,1]+0.1, name, fontsize=9)

# Vẽ tâm cụm
plt.scatter(centroids[:,0], centroids[:,1], c='black', s=150, marker='X', label='Tâm cụm')
plt.title("K-Means Clustering")
plt.xlabel("Attribute 1")
plt.ylabel("Attribute 2")
plt.legend()
plt.grid(True)
plt.show()
