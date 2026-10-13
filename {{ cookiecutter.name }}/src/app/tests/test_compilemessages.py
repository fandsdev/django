import gettext

import pytest
from django.core.management import call_command


@pytest.fixture
def messages_dir(tmp_path, settings):
    settings.LOCALE_PATHS = [tmp_path]
    messages_dir = tmp_path / "ru" / "LC_MESSAGES"
    messages_dir.mkdir(parents=True)
    (messages_dir / "django.po").write_text(
        r"""#, fuzzy
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"
"Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"

msgid "Active"
msgstr "Активна"

msgid "day"
msgid_plural "days"
msgstr[0] "день"
msgstr[1] "дня"
msgstr[2] "дней"

#, fuzzy
msgid "Paused"
msgstr "Приостановлена"
"""
    )
    return messages_dir


@pytest.fixture
def translations(messages_dir):
    call_command("compilemessages", verbosity=0)

    with (messages_dir / "django.mo").open("rb") as mo_file:
        return gettext.GNUTranslations(mo_file)


def test_translates(translations):
    assert translations.gettext("Active") == "Активна"


@pytest.mark.parametrize(("count", "expected"), [(1, "день"), (3, "дня"), (5, "дней"), (11, "дней"), (21, "день")])
def test_keeps_plural_forms(translations, count, expected):
    assert translations.ngettext("day", "days", count) == expected


def test_skips_fuzzy_messages(translations):
    assert translations.gettext("Paused") == "Paused"


def test_skips_other_locales(messages_dir):
    call_command("compilemessages", locale=["en"], verbosity=0)

    assert not (messages_dir / "django.mo").exists()
