EMOJI_MAP = {
    ":smile:": "😄",
    ":happy:": "😊",
    ":heart:": "❤️",
    ":laugh:": "😂",
    ":sad:": "😢",
    ":angry:": "😡",
    ":love:": "😍",
    ":thumbsup:": "👍",
    ":thumbsdown:": "👎",
    ":ok:": "👌",
    ":fire:": "🔥",
    ":star:": "⭐",
    ":wave:": "👋",
    ":clap:": "👏",
    ":party:": "🎉",
    ":cool:": "😎"
}


def convert_emojis(message):

    for shortcode, emoji in EMOJI_MAP.items():

        message = message.replace(
            shortcode,
            emoji
        )

    return message


def format_message(username, message, timestamp):

    return f"[{timestamp}] {username}: {message}"