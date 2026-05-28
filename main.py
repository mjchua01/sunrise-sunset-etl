from extract import Extractor
from transform import Transformer
from load import Loader
from validation import Validator


def main():

    # ----------------------------
    # INIT CLASSES
    # ----------------------------
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader()
    validator = Validator()

    city = input("Enter a city: ")

    # ----------------------------
    # EXTRACT
    # ----------------------------
    raw_data = extractor.extract_all(city)

    if not raw_data:
        print("❌ Extraction failed")
        return

    print("✅ Extract successful")

    # ----------------------------
    # VALIDATE API RESPONSE (IMPORTANT FIRST CHECK)
    # ----------------------------
    if not validator.check_api_response(raw_data):
        print("❌ API validation failed")
        return

    # ----------------------------
    # TRANSFORM
    # ----------------------------
    transformed_data = transformer.transform(raw_data)

    if not transformed_data:
        print("❌ Transformation failed")
        return

    print("✅ Transform successful")

    print("\n📊 FINAL DATA:")
    print(transformed_data)

    # ----------------------------
    # VALIDATION PIPELINE (FULL DATA QUALITY FRAMEWORK)
    # ----------------------------

    # 1. Null checks
    if not validator.check_nulls(transformed_data):
        print("❌ Validation failed: null check")
        return

    # 2. Schema / type checks
    if not validator.check_schema(transformed_data):
        print("❌ Validation failed: schema check")
        return

    # 3. Range validation
    if not validator.check_range(transformed_data):
        print("❌ Validation failed: range check")
        return

    # 4. Logical validation
    if not validator.check_sun_logic(transformed_data):
        print("❌ Validation failed: logic check")
        return

    print("✅ All validations passed")

    # ----------------------------
    # LOAD (ONLY IF VALID)
    # ----------------------------
    loader.load_data(transformed_data)

    print("✅ Load successful")


if __name__ == "__main__":
    main()