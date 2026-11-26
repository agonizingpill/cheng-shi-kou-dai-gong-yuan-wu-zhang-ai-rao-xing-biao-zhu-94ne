from domain.entrances_api import router as entrances
from domain.walk_profiles_api import router as walk_profiles
from domain.tag_aliases_api import router as tag_aliases
from domain.detours_api import router as detours
from domain.map_notes_api import router as map_notes

routers = (entrances, walk_profiles, tag_aliases, detours, map_notes,)
