from datetime import datetime
import yaml
import pytz


class Account(object):

    def __init__(self, domain,
                 login_id="", login_password="",
                 basic_id="", basic_password=""):
        self.domain = domain
        self.login_id = login_id
        self.login_password = login_password
        self.basic_id = basic_id
        self.basic_password = basic_password

    @classmethod
    def load(cls, path):
        apps = None

        with open(path, "rb") as f:
            a_dict = yaml.load(f)
            apps = cls.loads(a_dict)

        return apps

    @classmethod
    def loads(cls, account_dict):
        account = None

        # create account
        args = {
            "domain": account_dict["domain"]
        }
        for k in ["login", "basic"]:
            if k in account_dict:
                args[k + "_id"] = account_dict[k]["id"]
                args[k + "_password"] = account_dict[k]["password"]

        account = Account(**args)
        kintone = kintoneService(account)

        # load kintone apps
        apps = []
        for name in account_dict["apps"]:
            _a = account_dict["apps"][name]
            token = "" if "token" not in _a else _a["token"]
            kintone.app(int(_a["id"]), token, name)

        return kintone

    def __str__(self):
        infos = []
        infos.append("domain:\t {0}".format(self.domain))
        infos.append("login:\t {0} / {1}".format(self.login_id, self.login_password))
        infos.append("basic:\t {0} / {1}".format(self.basic_id, self.basic_password))

        return "\n".join(infos)


class kintoneService(object):
    ENCODE = "utf-8"
    SELECT_LIMIT = 500
    UPDATE_LIMIT = 100

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    from tzlocal import get_localzone
    __TIME_ZONE = get_localzone()

    def __init__(self, account):
        self.account = account
        self.__apps = []

    def __len__(self):
        return len(self.__apps)

    def app(self, app_id=-1, api_token="", app_name=""):
        from pykintone.application import Application
        if app_id < 0:
            return self.__apps[0]
        else:
            existed = [a for a in self.__apps if a.app_id == app_id]
            # register if not exist
            if len(existed) > 0:
                return existed[0]
            else:
                _a = Application(self.account, app_id, api_token, app_name)
                self.__apps.append(_a)
                return _a

    @classmethod
    def value_to_date(cls, value):
        return datetime.strptime(value, cls.DATE_FORMAT)

    @classmethod
    def value_to_time(cls, value):
        return datetime.strptime(value, cls.TIME_FORMAT)

    @classmethod
    def value_to_datetime(cls, value):
        d = datetime.strptime(value, cls.DATETIME_FORMAT)
        utc = d.replace(tzinfo=pytz.utc)  # configure timezone (on kintone, time is utc)
        local = utc.astimezone(cls.__TIME_ZONE).replace(tzinfo=None)  # to local, and to native
        return local

    @classmethod
    def date_to_value(cls, date):
        return date.strftime(cls.DATE_FORMAT)

    @classmethod
    def time_to_value(cls, time):
        return time.strftime(cls.TIME_FORMAT)

    @classmethod
    def datetime_to_value(cls, dt):
        local = dt.replace(tzinfo=cls.__TIME_ZONE)
        utc = local.astimezone(pytz.utc)
        value = utc.strftime(cls.DATETIME_FORMAT)
        return value
