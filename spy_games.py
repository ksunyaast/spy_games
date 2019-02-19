from pprint import pprint
import requests
import json

if __name__ == '__main__':
    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
    # eshmargunov 171691064
    user = input('Введите имя пользователя или id для поиска: ')
    params = {
        'v': '5.92',
        'access_token': token,
    }
    response = requests.get('https://api.vk.com/method/users.get?user_ids=' + user, params)
    print('-')
    user_ids = response.json()
    user_id = user_ids['response'][0]['id']

    response = requests.get('https://api.vk.com/method/friends.get?user_id=' + str(user_id), params)
    print('-')
    user_friends = response.json()
    user_friends_list = user_friends['response']['items']

    response = requests.get('https://api.vk.com/method/groups.get?user_id=' + str(user_id), params)
    print('-')
    user_groups = response.json()
    user_groups_list = user_groups['response']['items']

    no_match_groups_list = list()
    for group in user_groups_list:
        response = requests.get('https://api.vk.com/method/groups.getMembers?group_id=' + str(group), params)
        print('-')
        group_members = response.json()
        group_members_list = group_members['response']['items']
        match_members = list(set(user_friends_list) & set(group_members_list))
        if len(match_members) == 0:
            no_match_groups_list.append(group)
        else:
            pass

    no_match_groups_info_list = list()
    for no_match_group in no_match_groups_list:
        response = requests.get('https://api.vk.com/method/groups.getById?group_ids=' + str(no_match_group) +
                                '&fields=members_count', params)
        print('-')
        groups_info = response.json()
        no_match_group_dict = dict()
        no_match_group_dict['name'] = groups_info['response'][0]['name']
        no_match_group_dict['gid'] = str(groups_info['response'][0]['id'])
        no_match_group_dict['members_count'] = groups_info['response'][0]['members_count']
        no_match_groups_info_list.append(no_match_group_dict)

    with open('no_match_groups.json', 'w', encoding='utf-8') as f:
        json.dump(no_match_groups_info_list, f, ensure_ascii=False, indent=2)
        print('Файл записан')