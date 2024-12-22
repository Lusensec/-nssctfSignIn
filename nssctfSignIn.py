import logging
import requests

USER_AGENT = (
        "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
        + "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
)

# 如果需要多人则复制多个userinfo 内容
userinfos = [
    {
        "username": "用户1账号",
        "password": "用户1密码",
    },
    {
        "username": "用户2账号",
        "password": "用户2密码",
    }
    # ...
]


def login(session: requests.Session, username, password):
    """使用session登陆，并将token写入session中

    Args:
        session (requests.Session): requests的session
    """
    resp = session.post(
        "https://www.nssctf.cn/api/user/login/",
        headers={"User-Agent": USER_AGENT},
        data={
            "username": username,
            "password": password,
        },
    )
    data = resp.json()
    assert data["code"] == 200
    session.cookies["token"] = data["data"]["token"]


def signin(session: requests.Session):
    """进行签到（虽然只有两三个硬币

    Args:
        session (requests.Session): 使用的session

    Returns:
        bool: 是否签到成功
    """
    resp = session.post(
        "https://www.nssctf.cn/api/user/clockin/",
        headers={"User-Agent": USER_AGENT},
    )
    logging.warning(resp.text)
    data = resp.json()
    return data["code"] == 200


def coin_num(session: requests.Session) -> int:
    """获取硬币数量

    Args:
        session (requests.Session): 使用的session

    Returns:
        int: 硬币数量，失败时为None
    """
    resp = session.get(
        "https://www.nssctf.cn/api/user/info/opt/setting/",
        headers={"User-Agent": USER_AGENT},
    )
    logging.warning(resp.text)
    data = resp.json()
    assert data["code"] == 200
    num = data.get("data", {}).get("coin", None)
    assert num is not None
    return num


def main():
    # 进行多人循环签到
    for userinfo in userinfos:
        # 登陆，签到并打印coin数量
        session = requests.Session()
        login(session, userinfo["username"], userinfo["password"])
        signin(session)
        num = coin_num(session)
        print(f"现金币数量：{num}")


if __name__ == "__main__":
    main()
