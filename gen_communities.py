# by Eldar Khuzin 20220824
import json

communities = {
    '<group_name_for_you>': '<group_id/group_beauty_name>',
}

with open('communities.json', 'w') as file:
    json.dump(communities, file)
