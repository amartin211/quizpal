import json
from main import lambda_handler


def create_s3_event(bucket_name, object_key):
    return {"Records": [{"s3": {"bucket": {"name": bucket_name}, "object": {"key": object_key}}}]}


def test_short_press():
    # Simulate a short press event
    event = create_s3_event(
        bucket_name="bucketlambdafunc", object_key="00000000261981f9/image_20241201_181822_773474.jpg"
    )

    context = None  # You can create a mock context if needed
    response = lambda_handler(event, context)
    print("Short press test response:", json.dumps(response, indent=2))


def test_long_press():
    # Simulate a long press event (manifest file upload)
    event = create_s3_event(
        bucket_name="bucketlambdafunc", object_key="00000000261981f9/24e049d5-bf74-45eb-8fc5-7b2d8e6773e2/manifest.json"
    )

    context = None
    response = lambda_handler(event, context)
    print("Long press test response:", json.dumps(response, indent=2))


if __name__ == "__main__":
    test_short_press()
    # test_long_press()
