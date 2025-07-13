import argparse

parser = argparse.ArgumentParser(description="Lesson Generator")
parser.add_argument("filename", type=str, help="Lesson file name")

from generator import process_lesson

if __name__ == "__main__":
    args = parser.parse_args()
    process_lesson(args.filename)