from models.schemas.link import ShowLink


async def serialize_dict_to_link(link: dict) -> ShowLink:
    return ShowLink(
        link_id=link["link_id"],
        user_id=link["user_id"],
        entry_link=link["entry_link"],
        short_link=link["short_link"],
        clicks=link["clicks"],
    )
