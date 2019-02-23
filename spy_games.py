import requests
import json
import time


def get_data(url, params):
    while True:
        response = requests.get(url, params=params).json()
        print('-')
        try:
            return response['response']
        except KeyError:
            print('request error: ', response)
            time.sleep(1)

if __name__ == '__main__':
    token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
    # eshmargunov 171691064
    user = input('Введите имя пользователя или id для поиска: ')
    params = {
        'v': '5.92',
        'access_token': token,
    }

    url = 'https://api.vk.com/method/users.get?user_ids=' + user
    user_id = get_data(url, params)[0]['id']

    url = 'https://api.vk.com/method/friends.get?user_id=' + str(user_id)
    user_friends_list = get_data(url, params)['items']

    url = 'https://api.vk.com/method/groups.get?user_id=' + str(user_id)
    user_groups_list = get_data(url, params)['items']

    no_match_groups_list = list()
    mutual_friends_groups_list = list()
    for i, group in enumerate(user_groups_list):
        url = 'https://api.vk.com/method/groups.isMember?group_id=' + str(group) + '&user_ids=' + str(user_friends_list)
        members = 0
        for match in get_data(url, params):
            members += match['member']
        if members == 0:
            no_match_groups_list.append(group)
        else:
            pass
        if members == 4:
            mutual_members = members
            mutual_friends_groups_list.append(group)
        else:
            pass
        if i+1 == len(user_groups_list):
            print(f'Все {len(user_groups_list)} групп обработаны.')
        else:
            print(f'Осталось обработать {len(user_groups_list)-(i+1)} групп(ы) из {len(user_groups_list)} групп.')

    no_match_groups_info_list = list()
    for i, no_match_group in enumerate(no_match_groups_list):
        url = 'https://api.vk.com/method/groups.getById?group_ids=' + str(no_match_group) + '&fields=members_count'
        no_match_group_dict = dict()
        no_match_group_dict['name'] = get_data(url, params)[0]['name']
        no_match_group_dict['gid'] = str(get_data(url, params)[0]['id'])
        no_match_group_dict['members_count'] = get_data(url, params)[0]['members_count']
        no_match_groups_info_list.append(no_match_group_dict)
        if i+1 == len(no_match_groups_list):
            print(f'Все {len(no_match_groups_list)} групп(ы) без общих друзей записаны.')
        else:
            print(f'Осталось записать {len(no_match_groups_list)-(i+1)} групп(ы) из {len(no_match_groups_list)} групп без общих друзей.')

    with open('no_match_groups.json', 'w', encoding='utf-8') as f:
        json.dump(no_match_groups_info_list, f, ensure_ascii=False, indent=2)
        print('Файл записан')

    print(f'Группы с {mutual_members} общими друзьями: {mutual_friends_groups_list}')