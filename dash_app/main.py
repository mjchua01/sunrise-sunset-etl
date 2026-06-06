from extract import Extractor
from transform import Transformer
from load import Loader
from validation import Validator


def main():

    extractor = Extractor()
    transformer = Transformer()
    loader = Loader()
    validator = Validator()

    city = input("Enter a city: ")

    raw = extractor.extract_all(city)

    if not raw:
        print("❌ Extract failed")
        return

    transformed = transformer.transform(raw)

    if not transformed:
        print("❌ Transform failed")
        return

    print("\n📊 FINAL DATA")
    print(transformed)

    if not validator.check_nulls(transformed):
        print("❌ Validation failed")
        return

    if not validator.check_format(transformed):
        print("❌ Validation failed")
        return

    if not validator.check_logic(transformed):
        print("❌ Validation failed")
        return

    print("✅ All validations passed")

    loader.load_data(transformed)
    print("✅ Pipeline complete")


if __name__ == "__main__":
    main()