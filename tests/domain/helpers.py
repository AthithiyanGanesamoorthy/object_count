from counter.domain.models import Prediction, Box
import sys
import os
# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_prediction(class_name, score=1.0):
    return Prediction(class_name=class_name, score=score, box=Box(0, 0, 0, 0))