import toml
file = './coolq/plugins/pretty_boy/the_boy.toml'
data = toml.load(file)
the_boy = data['the_boy']
the_boy_sex = the_boy['sex']
user_id = the_boy['user_id']

sex = {
    'male': '靓仔',
    'famale': '靓妞'
}

group_id = '97795387'
bot_id = '732599980'
message = f'今日{the_boy_sex}诞生啦！{user_id}'

