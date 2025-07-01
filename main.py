from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_all

def main():
    # Extract
    raw_data = extract_data()

    # Transform
    cleaned_data = transform_data(raw_data)

    # Load
    load_all(cleaned_data)

if __name__ == '__main__':
    main()
