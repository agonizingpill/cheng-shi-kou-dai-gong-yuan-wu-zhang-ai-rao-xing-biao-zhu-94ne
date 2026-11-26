from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import tag_aliases_service as service
from domain.tag_aliases_model import tag_aliases
from domain.tag_aliases_schemas import MergeTags

router = APIRouter()

@router.get('/tag_aliases')
def list_tag_aliases(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, tag_aliases)


@router.post('/tag_aliases/merge-tags')
def merge_tags(data: MergeTags, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.merge_tags(conn, user, data)
        record(conn, user, 'tag_aliases.merge_tags')
        return output
