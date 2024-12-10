import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# Database connection parameters (replace with your credentials)
db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "sednev23",  # Replace with your actual password
    "options": "-c client_encoding=UTF8"
}

try:
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Fetch points data
    cur.execute("SELECT x, y, g FROM kmeans.points")
    points_data = cur.fetchall()

    # Fetch centroid data
    cur.execute("SELECT x, y, cluster FROM kmeans.models")  # Include 'cluster' for legend
    centroids_data = cur.fetchall()

    # Separate data (more robust error handling)
    x_points = np.array([point[0] for point in points_data])
    y_points = np.array([point[1] for point in points_data])
    clusters = np.array([point[2] for point in points_data])

    x_centroids = np.array([centroid[0] for centroid in centroids_data])
    y_centroids = np.array([centroid[1] for centroid in centroids_data])
    centroid_clusters = np.array([centroid[2] for centroid in centroids_data])


    # Create scatter plot
    plt.figure(figsize=(10, 8))  # Slightly larger figure
    plt.scatter(x_points, y_points, c=clusters, cmap='viridis', s=50, label='Data Points')
    plt.scatter(x_centroids, y_centroids, marker='X', s=200, c='red', label='Centroids')

    #Improved Legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    # Add labels and title
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.title("K-means Clustering Results")
    plt.grid(True) #add grid

    # Display the plot
    plt.show()

    cur.close()
    conn.close()

except psycopg2.Error as e:
    print(f"PostgreSQL error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")