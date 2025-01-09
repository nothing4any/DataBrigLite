from fastapi import APIRouter, UploadFile, File, Form, Body

from business.service import dataservice
from schemas import schemas
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger("data")

server = dataservice.Service()


@router.post("/datareq")
async def data_request(item: schemas.DataReq):
    res = await server.data_request(item)
    return res


@router.post("/myreqlist")
async def data_request(item: schemas.DataReqInfos):
    res = await server.my_data_infos(item)
    return res


@router.post("/myreqcount")
async def data_request_count(item: schemas.DataReqInfos):
    res = await server.my_data_count(item)
    return res


@router.post("/handlereqlist")
async def handle_data_infos(item: schemas.DataReqInfos):
    res = await server.handle_data_infos(item)
    return res


@router.post("/handlereqcount")
async def handle_request_count(item: schemas.DataReqInfos):
    res = await server.handle_data_count(item)
    return res


@router.post("/acceptreq")
async def handle_request_accept(item: schemas.MyDataStatusEdit):
    res = await server.handle_request_accept(item)
    return res


@router.post("/handlefileupdate")
async def handle_file_update(file: UploadFile = File(...)
                             , note: str = Form(...)
                             , requestid: str = Form(...)
                             , usernumber: str = Form(...)
                             , status: str = Form(...)):
    item = schemas.FileAndUpdate(note=note, requestid=requestid
                                 , usernumber=usernumber
                                 , status=status)
    res = await server.handle_file_update(file, item)
    return res


@router.post("/mydataedit")
async def my_data_edit(item: schemas.MyDataEdit):
    res = await server.my_data_edit(item)
    return res


@router.post("/processrecords")
async def process_records(item: schemas.ProcessRecords):
    res = await server.process_records(item)
    return res


@router.post("/download")
async def download(item: schemas.download):
    res = await server.download(item)
    return res


@router.post("/taskoverview")
async def task_overview(item: schemas.TaskOverview):
    res = await server.task_overview(item)
    return res


@router.post("/taskoverviewinfo")
async def task_overview_info(item: schemas.TaskOverviewInfo):
    res = await server.task_overview_info(item)
    return res


@router.get("/getnewinformation")
async def get_new_information():
    res = await server.get_new_information()
    return res


@router.post("/addnewinformation")
async def add_new_information(item: schemas.AddNewInformation):
    res = await server.add_new_information(item)
    return res


@router.post("/editnewinformation")
async def edit_new_information(item: schemas.AddNewInformation):
    res = await server.edit_new_information(item)
    return res


@router.post("/delnewinformation")
async def del_new_information(item: schemas.NewInformation):
    res = await server.del_new_information(item)
    return res


@router.get("/getnewinformationview")
async def get_new_information_view():
    res = await server.get_new_information_view()
    return res