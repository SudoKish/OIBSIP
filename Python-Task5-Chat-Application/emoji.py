EMOJI_MAP = {
    ":smile:": "😄",
    ":laughing:": "😂",
    ":heart:": "❤️",
    ":thumbsup:": "👍",
    ":thumbsdown:": "👎",
    ":fire:": "🔥",
    ":cry:": "😢",
    ":angry:": "😠",
    ":sad:": "😔",
    ":love:": "😍",
    ":wink:": "😉",
    ":wave:": "👋",
    ":clap:": "👏",
    ":party:": "🎉",
    ":rocket:": "🚀",
    ":ok:": "👌",
    ":cool:": "😎",
    ":thinking:": "🤔",
    ":surprised:": "😮",
    ":laugh:": "🤣",
}


def convert_shortcodes(text):
    for shortcode, emoji in EMOJI_MAP.items():
        text = text.replace(
            shortcode,
            emoji
        )

    return text