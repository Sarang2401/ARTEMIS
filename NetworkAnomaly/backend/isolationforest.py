import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import datetime
import json

class NetworkAnomalyDetector:
    def __init__(self, contamination=0.1):
        """
        Initialize the Network Anomaly Detector
        
        Parameters:
        contamination (float): Expected proportion of anomalies in the dataset
        """
        self.model = None
        self.scaler = StandardScaler()
        self.contamination = contamination
        self.feature_columns = [
            'duration', 'protocol_type', 'service', 
            'flag', 'src_bytes', 'dst_bytes', 
            'land', 'wrong_fragment', 'urgent', 
            'hot', 'num_failed_logins', 'logged_in', 
            'num_compromised', 'root_shell', 'su_attempted',
            'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 
            'is_host_login', 'is_guest_login'
        ]

    def load_dataset(self, filepath):
        """
        Load and preprocess network connection dataset
        """
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                print(f"Dataset not found at {filepath}")
                
                # Generate synthetic dataset if original is missing
                print("Generating synthetic dataset...")
                return self.generate_synthetic_dataset()
            
            # Load dataset 
            print(f"Loading dataset from {filepath}")
            
            # Try different parsing methods
            try:
                # First, try reading with headers
                df = pd.read_csv(filepath)
                
                # If columns don't match, try without headers
                if len(df.columns) != len(self.feature_columns) + 1:
                    df = pd.read_csv(filepath, header=None, names=self.feature_columns + ['label'])
            except Exception:
                # Fallback to reading without headers
                df = pd.read_csv(filepath, header=None, names=self.feature_columns + ['label'])
            
            # Convert categorical variables to numeric
            categorical_cols = ['protocol_type', 'service', 'flag']
            for col in categorical_cols:
                df[col] = pd.Categorical(df[col]).codes
            
            # Separate features and labels
            X = df[self.feature_columns]
            y = df['label']
            
            print(f"Dataset loaded successfully. Shape: {X.shape}")
            return X, y
        
        except Exception as e:
            print(f"Error loading dataset: {e}")
            print("Generating synthetic dataset as fallback...")
            return self.generate_synthetic_dataset()

    def generate_synthetic_dataset(self, num_samples=1000):
        """
        Generate a synthetic network dataset when real dataset is unavailable
        """
        data = {
            'duration': np.random.uniform(0, 3600, num_samples),
            'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], num_samples),
            'service': np.random.choice(['http', 'ftp', 'smtp', 'dns'], num_samples),
            'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTO'], num_samples),
            'src_bytes': np.random.uniform(0, 10000, num_samples),
            'dst_bytes': np.random.uniform(0, 10000, num_samples),
            # Add more columns with realistic distributions
            'land': np.random.randint(0, 2, num_samples),
            'wrong_fragment': np.random.randint(0, 5, num_samples),
            'urgent': np.random.randint(0, 2, num_samples),
            'hot': np.random.randint(0, 10, num_samples),
            'num_failed_logins': np.random.randint(0, 3, num_samples),
            'logged_in': np.random.randint(0, 2, num_samples),
            'num_compromised': np.random.randint(0, 5, num_samples),
            'root_shell': np.random.randint(0, 2, num_samples),
            'su_attempted': np.random.randint(0, 2, num_samples),
            'num_root': np.random.randint(0, 3, num_samples),
            'num_file_creations': np.random.randint(0, 5, num_samples),
            'num_shells': np.random.randint(0, 2, num_samples),
            'num_access_files': np.random.randint(0, 3, num_samples),
            'num_outbound_cmds': np.random.randint(0, 2, num_samples),
            'is_host_login': np.random.randint(0, 2, num_samples),
            'is_guest_login': np.random.randint(0, 2, num_samples),
            'label': np.random.choice(['normal', 'attack'], num_samples, p=[0.8, 0.2])
        }
        
        df = pd.DataFrame(data)
        
        # Ensure dataset directory exists
        os.makedirs('datasets', exist_ok=True)
        
        # Save synthetic dataset
        synthetic_path = 'datasets/synthetic_network_data.csv'
        df.to_csv(synthetic_path, index=False)
        print(f"Synthetic dataset generated and saved to {synthetic_path}")
        
        # Convert categorical variables to numeric
        categorical_cols = ['protocol_type', 'service', 'flag']
        for col in categorical_cols:
            df[col] = pd.Categorical(df[col]).codes
        
        X = df[self.feature_columns]
        y = df['label']
        
        return X, y

    def preprocess_data(self, X):
        """
        Preprocess data by scaling numerical features using StandardScaler
        
        Parameters:
        X (pandas.DataFrame): Input feature matrix
        
        Returns:
        numpy.ndarray: Scaled feature matrix
        """
        # Select only numeric columns
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        
        # Create a copy of the dataframe with only numeric columns
        X_numeric = X[numeric_columns]
        
        # Fit and transform the numeric data
        X_scaled = self.scaler.fit_transform(X_numeric)
        
        return X_scaled

    def train_anomaly_detector(self, X_scaled):
        """
        Train Isolation Forest anomaly detector
        
        Parameters:
        X_scaled (numpy.ndarray): Scaled feature matrix
        """
        try:
            # Initialize and train Isolation Forest
            self.model = IsolationForest(
                contamination=self.contamination, 
                random_state=42
            )
            self.model.fit(X_scaled)
            print("Anomaly detector trained successfully.")
        except Exception as e:
            print(f"Error training anomaly detector: {e}")

    def predict_anomalies(self, X):
        """
        Predict anomalies using trained Isolation Forest
        
        Parameters:
        X (pandas.DataFrame): Original feature matrix
        
        Returns:
        tuple: Predictions and anomaly scores
        """
        try:
            # Preprocess data
            X_scaled = self.preprocess_data(X)
            
            # Predict anomalies
            # -1 indicates anomalies, 1 indicates normal instances
            predictions = self.model.predict(X_scaled)
            
            # Get anomaly scores (lower scores indicate more anomalous)
            scores = self.model.score_samples(X_scaled)
            
            return predictions, scores
        except Exception as e:
            print(f"Error predicting anomalies: {e}")
            return None, None

    def generate_threat_report(self, X, predictions):
        """
        Generate a comprehensive threat report
        
        Parameters:
        X (pandas.DataFrame): Original feature matrix
        predictions (numpy.ndarray): Anomaly predictions
        """
        try:
            # Select only numeric columns for analysis
            numeric_columns = X.select_dtypes(include=[np.number]).columns
            X_numeric = X[numeric_columns]

            # Count anomalies
            anomaly_count = np.sum(predictions == -1)
            total_samples = len(predictions)
            anomaly_percentage = (anomaly_count / total_samples) * 100

            # Create report dictionary
            report = {
                'timestamp': datetime.datetime.now().isoformat(),
                'total_samples': total_samples,
                'anomaly_count': int(anomaly_count),
                'anomaly_percentage': round(anomaly_percentage, 2),
                'top_anomalous_features': self.identify_anomalous_features(X_numeric, predictions)
            }

            # Ensure reports directory exists
            os.makedirs('reports', exist_ok=True)

            # Generate filename with timestamp
            filename = f'reports/threat_report_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

            # Save report
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4)

            print(f"Threat report generated: {filename}")
            print(f"Anomaly Percentage: {anomaly_percentage:.2f}%")
        except Exception as e:
            print(f"Error generating threat report: {e}")

    def identify_anomalous_features(self, X, predictions):
        """
        Identify most significant features contributing to anomalies
        
        Parameters:
        X (pandas.DataFrame): Numeric feature matrix
        predictions (numpy.ndarray): Anomaly predictions
        
        Returns:
        list: Top anomalous features
        """
        try:
            # Ensure X is numeric and predictions is a numpy array
            X = pd.DataFrame(X)
            predictions = np.array(predictions)

            # Identify anomalous instances
            anomalous_data = X[predictions == -1]

            # Calculate feature importance based on variance in anomalous data
            feature_variances = anomalous_data.var()
            
            # Sort features by variance and return top 5
            top_features = feature_variances.nlargest(5).index.tolist()
            
            return top_features
        except Exception as e:
            print(f"Error identifying anomalous features: {e}")
            return []

    def save_model(self, filepath='models/anomaly_detector.joblib'):
        """
        Save trained model and scaler
        
        Parameters:
        filepath (str): Path to save the model
        """
        try:
            # Ensure models directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save model and scaler
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, filepath)
            
            print(f"Model saved successfully to {filepath}")
        except Exception as e:
            print(f"Error saving model: {e}")

def main():
    # Initialize detector
    detector = NetworkAnomalyDetector(contamination=0.1)
    
    # Load dataset from the specified path
    X, y = detector.load_dataset('datasets/network_data.csv')
    
    if X is not None:
        # Preprocess data
        X_scaled = detector.preprocess_data(X)
        
        # Train model
        detector.train_anomaly_detector(X_scaled)
        
        # Predict anomalies
        predictions, scores = detector.predict_anomalies(X)
        
        if predictions is not None:
            # Generate threat report
            detector.generate_threat_report(X, predictions)
            
            # Save model for future use
            detector.save_model()

if __name__ == "__main__":
    main()