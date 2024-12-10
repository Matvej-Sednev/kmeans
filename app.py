import psycopg2
import matplotlib.pyplot as plt

# Database connection details (replace with your credentials)
db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1",
}

try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Fetch data from the points table
    cur.execute("SELECT x, y, g FROM points")
    points_data = cur.fetchall()

    # Fetch data from the models table
    cur.execute("SELECT x, y, cluster FROM models")
    centroids_data = cur.fetchall()

    # Separate x, y, and cluster data
    x_points = [point[0] for point in points_data]
    y_points = [point[1] for point in points_data]
    clusters = [point[2] for point in points_data]

    x_centroids = [centroid[0] for centroid in centroids_data]
    y_centroids = [centroid[1] for centroid in centroids_data]
    cluster_labels = [centroid[2] for centroid in centroids_data]



    # Create the scatter plot
    plt.figure(figsize=(8, 6))  # Adjust figure size as needed
    scatter = plt.scatter(x_points, y_points, c=clusters, cmap='viridis', s=50) #Use viridis or other cmap
    plt.scatter(x_centroids, y_centroids, marker='X', s=200, c='red', label='Centroids') #Mark centroids with 'X'

    # Add labels and legend
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.title("K-means Clustering Results")
    plt.legend(*scatter.legend_elements(), title="Clusters")
    plt.legend()

    # Show the plot
    plt.show()

    # Close the cursor and connection
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print(f"PostgreSQL error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")