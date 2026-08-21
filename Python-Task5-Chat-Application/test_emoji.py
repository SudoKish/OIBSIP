from emoji import convert_shortcodes


test_message = (
    "Hello :smile: "
    "This is :fire: "
    "and I :heart: Python! "
    ":rocket:"
)

converted_message = convert_shortcodes(
    test_message
)

print("Original:")
print(test_message)

print("\nConverted:")
print(converted_message)