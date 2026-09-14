
# -*- mode: python ; coding: utf-8 -*-

# Hidden imports for all modules that might be dynamically imported
hiddenimports = [
    'src.data.download_data',
    'src.data.preprocess_data',
    'src.features.feature_engineering',
    'src.models.predict_model',
    'src.models.ql_agent',
    'src.models.train_model',
    'src.utils.logging_config',
    'src.visualization.visualize_data',
    # Add any other modules that might be imported dynamically
]

# Data files to include (models, configs, etc.)
datas = [
    ('models/best_xgb_model.joblib', 'models'),
    ('models/best_xgb_model.pkl', 'models'),
    ('models/q_learning_agent.pkl', 'models'),
    ('models/model_output/best_model.joblib', 'models/model_output'),
    ('models/model_output/model_config.json', 'models/model_output'),
    ('models/model_output/model_metrics.json', 'models/model_output'),
    ('models/model_output/q_learning_agent.pkl', 'models/model_output'),
    ('models/model_output/q_learning_agent2.joblib', 'models/model_output'),
    ('models/model_output/q_learning_agent2.pkl', 'models/model_output'),
    ('models/model_output/state_bins.pkl', 'models/model_output'),
]

# Main analysis configuration
a = Analysis(
    ['src/ui/load_balancer_ui.py'],  # Main script entry point
    pathex=['.'],  # Additional paths to search for imports
    binaries=[],  # External binaries to include
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],  # Paths to custom hooks
    hooksconfig={},  # Hooks configuration
    runtime_hooks=[],  # Runtime hooks
    excludes=['PySide6'],  # Explicitly exclude PySide6 if not needed
    noarchive=False,
    optimize=0,  # 0 = no optimization, 1 = basic, 2 = max
)

# Create the PYZ (Python Zip Archive)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None  # Add cipher=block_cipher for encryption if needed
)

# Executable configuration
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],  # Additional options
    name='loadbalancerui',  # Output filename
    debug=False,  # Set to True for debug builds
    bootloader_ignore_signals=False,
    strip=False,  # Strip symbols for smaller size (Linux/macOS)
    upx=False,  # Disable UPX compression to avoid potential issues
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hides the console window (windowed mode)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,  # Specify 'x86_64' or 'arm64' if needed
    codesign_identity=None,  # For macOS code signing
    entitlements_file=None,  # For macOS entitlements
    icon=None  # Add path to .ico file for Windows icons
)


