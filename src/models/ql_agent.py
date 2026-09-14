
import numpy as np

class QLearningAgent:
    """Enhanced Q-Learning agent with state normalization"""
    def __init__(self, q_table=None):
        self.q_table = q_table if q_table is not None else np.zeros((100, 2))  # Default small table
        self.state_bins = {
            'task_size': [1, 25, 50, 75, 100],
            'cpu_demand': [0.1, 25, 50, 75, 100],
            'memory_demand': [1, 16, 32, 48, 64],
            'network_latency': [0.1, 50, 100, 150, 200],
            'io_operations': [1, 250, 500, 750, 1000],
            'disk_usage': [1, 25, 50, 75, 100],
            'num_connections': [1, 250, 500, 750, 1000],
            'priority_level': [0, 1]
        }

    def get_action(self, state, epsilon=0.1):
        """Epsilon-greedy action selection"""
        if np.random.random() < epsilon:
            return np.random.choice(len(self.q_table[0]))
        return np.argmax(self.q_table[state])

    def discretize_state(self, features):
        """Convert continuous features to discrete state index"""
        if features.ndim == 2:
            features = features[0]

        discretized = []
        for i, (feature, bins) in enumerate(zip(features, self.state_bins.values())):
            discretized.append(np.digitize(feature, bins) - 1)  # 0-based index

        # Calculate multi-dimensional index
        state = 0
        for i, val in enumerate(discretized):
            state += val * (len(bins) ** i)  # Assuming 5 bins per feature

        return min(state, len(self.q_table) - 1)  # Ensure state is within bounds



