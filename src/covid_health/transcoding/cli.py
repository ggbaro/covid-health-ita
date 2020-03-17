import click
from .names.human import lang
from .names.eurostat import EurostatDict


def field_code_to_human(language, field):
    codes = lang[language].get(field)
    if not field:
        print(f"field {field} has not yet been coded.")
    else:
        for ix, (code, descr) in enumerate(codes.items()):
            # descr_split = []  # IN CASE WE WANT TO SPLIT LINES
            # row = ""
            # for n, word in enumerate(descr.split(" ")):
            #     if len(f"{row} {word}") > 109:
            #         descr_split.append(row)
            #         row = ""
            #     row += f" {word}"
            # descr_split.append(row)
            # descr = "\n    ".join(descr_split)
            print(f"[{ix:3d}] {code} -> {descr}")

it = ", ".join(lang['it'].keys())
en = ", ".join(lang['en'].keys())

# --- CLI ---


@click.group(help="Util tools and info for transcoding.")
def cli():
    pass

@cli.command(name="eurostat-std", help="Print code metadata for a certain field.")
@click.argument("field")
def list_eurostat_std_code(field):
    dic = EurostatDict()[field]
    for ix, (code, descr) in enumerate(dic):
        print(f"[{ix:3d}] {code} -> {descr}")


@cli.command(
    name="translate-field-codes",
    help=f"""List human names of every code in a certain field.
    The field "col" returns human names of standard column codes (instead of field codes).

    Available for lang=it: {it}

    Available for lang=en: {en}

    """)
@click.argument("field")
@click.argument("lang", default="it")
def translate_field_codes(field, lang):
    field_code_to_human(lang, field)


# cli.add_command(translate_field_codes)


if __name__ == "__main__":
    cli()
