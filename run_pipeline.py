import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline.orchestrator import PipelineOrchestrator


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run YottaFlex Customer 360 Pipeline')
    parser.add_argument('--data-dir', default='data/sample_small', help='Directory containing input CSV files')
    parser.add_argument('--output-dir', default='outputs', help='Output directory')
    args = parser.parse_args()
    
    orch = PipelineOrchestrator(data_dir=args.data_dir, output_dir=args.output_dir)
    orch.run()

