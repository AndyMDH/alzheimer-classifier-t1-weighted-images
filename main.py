"""
Main script for Alzheimer's detection using transfer learning on vision transformers and CNNs.
"""

import argparse
import yaml
from pathlib import Path
from data.data_loader import prepare_data
from models.train import train_model
from models.evaluate import evaluate_model
from utils.logger import setup_logger

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    parser = argparse.ArgumentParser(description="Alzheimer's Detection Model Training")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    parser.add_argument('--model_type', type=str, choices=['2d_vit', '3d_vit', '3d_cnn'],
                        help='Type of model to use (overrides config file)')
    args = parser.parse_args()

    config = load_config(args.config)
    logger = setup_logger('alzheimer_detection', Path(config['paths']['log_dir']))

    model_type = args.model_type if args.model_type else config['model']['type']
    logger.info(f"Using model type: {model_type}")

    train_loader, val_loader, test_loader = prepare_data(
        config['dataset']['name'],
        model_type,
        config['dataset']['batch_size']
    )

    model = create_model(model_type, config['model']['num_labels'], config['model']['freeze_layers'])

    train_model(model, train_loader, val_loader, config['training'])

    results = evaluate_model(model, test_loader)
    logger.info(f"Evaluation results: {results}")

if __name__ == "__main__":
    main()