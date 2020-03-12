import os
from .transcoding.names_map import human_names


def map_names(item, lang="it"):
    if isinstance(item, str):
        return human_names[lang][item]
    if hasattr(item, "rename"):
        return item.rename(columns=human_names[lang])
