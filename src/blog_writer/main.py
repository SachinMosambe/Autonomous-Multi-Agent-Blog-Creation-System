#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from crew import BlogWriter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the blog writer crew.
    """
    # Get topic from command line argument or use default
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI"
    
    print(f"\n=== Generating blog post about: {topic} ===\n")
    
    inputs = {
        'topic': topic,
        "current_date": str(datetime.now())
    }

    # Create and run the crew
    result = BlogWriter().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL BLOG POST ===\n\n")
    
    # Handle different result types
    if hasattr(result, 'raw'):
        print(result.raw)
    else:
        print(result)


if __name__ == "__main__":
    run()