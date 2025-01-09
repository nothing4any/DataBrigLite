from pydantic import BaseModel


class MyDataEdit(BaseModel):
    """
    请求数据变更
    """
    requestid: str
    requestno: str
    status: str
    remake: str


class MyDataStatusEdit(BaseModel):
    """
    申请状态变更
    """
    requestid: str
    requestno: str
    status: str


class DataReq(BaseModel):
    """
    申请
    """
    datatype: str
    purpose: str
    handler: str
    reqid: str
    expectedDate: str
    fields: list


class DataReqInfos(BaseModel):
    """
    我的申请查询
    """
    usernumber: str
    status: str
    stratdt: str
    enddt: str
    pagenumber: int
    pagesize: int


class User(BaseModel):
    """
    用户实体
    """
    usernumber: str
    username: str
    role: str


class UserSearch(BaseModel):
    """
    用户搜索实体
    """
    pagesize: int
    pagenumber: int


class UserCreate(BaseModel):
    """
    用户创建实体
    """
    usernumber: str
    username: str
    password: str
    department: str
    role: str


class UserUpdate(BaseModel):
    """
    用户更新实体
    """
    usernumber: str
    password: str


class UserDelete(BaseModel):
    """
    用户删除实体
    """
    usernumber: str


class UserStatus(BaseModel):
    """
    用户状态
    """
    usernumber: str
    status: str


class Login(BaseModel):
    """
    登录实体
    """
    usernumber: str
    password: str


class Token(BaseModel):
    """
    token实体
    """
    token: str


class Out(BaseModel):
    """
    返回实体
    """
    code: str
    data: dict
    msg: str


class FileAndUpdate(BaseModel):
    """
    文件上传与状态变更
    """
    note: str
    requestid: str
    usernumber: str
    status: str


class ProcessRecords(BaseModel):
    """
    获取处理记录
    """
    requestno: str


class download(BaseModel):
    """
    文件下载
    """
    requestno: str


class TaskOverview(BaseModel):
    """
    数据看板-任务概览
    """
    usernumber: str


class TaskOverviewInfo(BaseModel):
    """
    数据看板-任务概览
    """
    usernumber: str


class NewInformation(BaseModel):
    """
    通知
    """
    infono: str


class AddNewInformation(BaseModel):
    """
    添加通知
    """
    id: int
    title: str
    type: str
    category: str
    content: str
    create_dt: str
    diff_time: str
    info_no: str
