# 根目录：项目迁移后，需要设置此目录
base_path = ""

# 子目录
log_path = base_path + "log/"

# 豆瓣小组的id
group_id_list = [
    "",
    ""]
# 704476
group_sig_ts_list = [
    "",
    ""]
"""
通过抓豆瓣app登录包获得的client_secret
参考：https://bbs.125.la/thread-14226779-1-1.html
"""
client_secret = "bf7dddc7c9cfe6f7"  # 这是不变的

"""
通过抓豆瓣app小组首页帖子列表获得的headers和小组信息
"""
authorization = ""  # 每次重新登录后都要更新（与小组无关）
headers = {
    "Authorization": "Bearer " + authorization,
    "User-Agent": "api-client/1 com.douban.frodo/6.17.0(160) Android/23 product/PLK-CL00 vendor/HUAWEI model/PLK-CL00 rom/android network/wifi platform/mobile",
    "Host": "frodo.douban.com",
    "Connection": "close",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
}
device_info = ""  # 抓包后填入相应的值
# get并不要去实时更新sig和ts，可以使用固定的链接
group_topics_url = (
    "https://frodo.douban.com/api/v2/group/"
    + "{group_id}"
    + "/topics?count=50&sortby=new&"
    + device_info
    + "{sig_ts}"
)  # 第一次抓包后填入相应的值

# post需要实时更新sig和ts，不然服务器会拒绝
comment_url_template = (
    "https://frodo.douban.com/api/v2/group/topic/{topic_id}/create_comment"
)
comment_content_template = (
    "text={comment}&" + device_info + "&_sig={sig}&_ts={timestamp}"
)
sig_code_template = (
    "POST&%2Fapi%2Fv2%2Fgroup%2Ftopic%2F{topic_id}%2Fcreate_comment&"
    + authorization
    + "&{timestamp}"
)

"""
预设的回复列表, 回复列表的长度最好在50以上
"""
comment_list = [
    "kswlkswl"
]