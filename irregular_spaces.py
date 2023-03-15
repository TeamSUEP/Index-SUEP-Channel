# https://eslint.org/docs/rules/no-irregular-whitespace
def fix_irregular_spaces(s: str) -> str:
    replace_dict = {
        "\u000B": "",  # Line Tabulation (\v) - <VT>
        "\u000C": "",  # Form Feed (\f) - <FF>
        "\u00A0": " ",  # No-Break Space - <NBSP>
        "\u0085": "",  # Next Line
        "\u1680": " ",  # Ogham Space Mark
        "\u180E": "",  # Mongolian Vowel Separator - <MVS>
        "\uFEFF": "",  # Zero Width No-Break Space - <BOM>
        "\u2000": "",  # En Quad
        "\u2001": "",  # Em Quad
        "\u2002": " ",  # En Space - <ENSP>
        "\u2003": " ",  # Em Space - <EMSP>
        "\u2004": "",  # Three-Per-Em
        "\u2005": "",  # Four-Per-Em
        "\u2006": "",  # Six-Per-Em
        "\u2007": " ",  # Figure Space
        "\u2008": " ",  # Punctuation Space - <PUNCSP>
        "\u2009": " ",  # Thin Space
        "\u200A": " ",  # Hair Space
        "\u200B": "",  # Zero Width Space - <ZWSP>
        "\u2028": "",  # Line Separator
        "\u2029": "",  # Paragraph Separator
        "\u202F": " ",  # Narrow No-Break Space
        "\u205F": " ",  # Medium Mathematical Space
        "\u3000": " ",  # Ideographic Space
    }
    for k, v in replace_dict.items():
        s = s.replace(k, v)
    return s
