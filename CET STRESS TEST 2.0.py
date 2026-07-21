import numpy as np


def run_cet_simulation(grid_dim=10, coupling_strength=0.05, noise_floor=1.0, seed=42):
    """
    Conceptual CET stress test.

    This simulation explores whether a weak structured signal embedded in
    stochastic noise can become more detectable after applying a simple
    geometric constraint filter.

    It is intended as a conceptual demonstration, not a physical proof.
    """
    rng = np.random.default_rng(seed)

    # 1. Define a 3D coordinate grid
    x = np.linspace(-5, 5, grid_dim)
    y = np.linspace(-5, 5, grid_dim)
    z = np.linspace(-5, 5, grid_dim)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    # 2. Define an underlying structured field
    radius = np.sqrt(X**2 + Y**2) + 1e-9
    signal_x = -Y / radius**2
    signal_y = X / radius**2
    signal_z = np.zeros_like(Z)

    true_signal = np.sqrt(signal_x**2 + signal_y**2 + signal_z**2)

    # 3. Add stochastic noise
    stochastic_noise = rng.normal(0, noise_floor, size=true_signal.shape)
    raw_daq_stream = (coupling_strength * true_signal) + stochastic_noise

    # 4. Apply a simple geometric constraint filter
    relational_mask = np.where(radius <= 4.0, 1.0, 0.0)
    filtered_output = raw_daq_stream * relational_mask

    # 5. Estimate signal and residual noise consistently
    expected_signal = coupling_strength * true_signal
    raw_residual = raw_daq_stream - expected_signal
    filtered_residual = filtered_output - (expected_signal * relational_mask)

    signal_to_noise_raw = np.mean(expected_signal) / np.std(raw_residual)
    signal_to_noise_filtered = np.mean(expected_signal * relational_mask) / np.std(filtered_residual)

    print("=== CET CONCEPTUAL STRESS-TEST RESULTS ===")
    print(f"Grid configuration      : {grid_dim}x{grid_dim}x{grid_dim}")
    print(f"Noise floor             : {noise_floor:.2f}")
    print(f"Raw SNR estimate        : {signal_to_noise_raw:.6f}")
    print(f"Filtered SNR estimate   : {signal_to_noise_filtered:.6f}")
    print("==========================================")

    if signal_to_noise_filtered > signal_to_noise_raw:
        print("STATUS: Filter improved detectability of the structured signal.")
    else:
        print("STATUS: No improvement detected under current parameters.")


run_cet_simulation(grid_dim=12, coupling_strength=0.08, noise_floor=1.2)
