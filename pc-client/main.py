import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app import main

if __name__ == "__main__":
    sys.exit(main())
