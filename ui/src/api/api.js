import service from './request';

const login = (params = {}) => {
    return service({
        url: '/api/login',
        method: 'post',
        data: params
    })
};

const unlogin = (params = {}) => {
    return service({
        url: '/api/unlogin',
        method: 'post',
        data: params
    })
};

const userlist = (params = {}) => {
    return service({
        url: '/api/user/',
        method: 'post',
        data: params
    })
};

const usercreate = (params = {}) => {
    return service({
        url: '/api/user/create',
        method: 'post',
        data: params
    })
};

const userupdate = (params = {}) => {
    return service({
        url: '/api/user/update',
        method: 'post',
        data: params
    })
};

const userdelete = (params = {}) => {
    return service({
        url: '/api/user/delete',
        method: 'post',
        data: params
    })
};

const datareq = (params = {}) => {
    return service({
        url: '/api/data/datareq',
        method: 'post',
        data: params
    })
};

const myreqlist = (params = {}) => {
    return service({
        url: '/api/data/myreqlist',
        method: 'post',
        data: params
    })
};

const myreqcount = (params = {}) => {
    return service({
        url: '/api/data/myreqcount',
        method: 'post',
        data: params
    })
};

const handlereqlist = (params = {}) => {
    return service({
        url: '/api/data/handlereqlist',
        method: 'post',
        data: params
    })
};

const handlereqcount = (params = {}) => {
    return service({
        url: '/api/data/handlereqcount',
        method: 'post',
        data: params
    })
};

const acceptreq = (params = {}) => {
    return service({
        url: '/api/data/acceptreq',
        method: 'post',
        data: params
    })
};

const handlefileupdate = (params = {}) => {
    return service({
        url: '/api/data/handlefileupdate',
        method: 'post',
        data: params
    })
};

const mydataedit = (params = {}) => {
    return service({
        url: '/api/data/mydataedit',
        method: 'post',
        data: params
    })
};

const usermap = (params = {}) => {
    return service({
        url: '/api/user/getusermap',
        method: 'post',
        data: params
    })
};

const processrecords = (params = {}) => {
    return service({
        url: '/api/data/processrecords',
        method: 'post',
        data: params
    })
};

const download = (params = {}) => {
    return service({
        url: '/api/data/download',
        method: 'post',
        data: params
    })
};

const taskoverview = (params) => {
    return service({
        url: '/api/data/taskoverview',
        method: 'post',
        data: params
    });
};

const taskoverviewinfo = (params) => {
    return service({
        url: '/api/data/taskoverviewinfo',
        method: 'post',
        data: params
    });
};

const getnewinformation = () => {
    return service({
        url: '/api/data/getnewinformation',
        method: 'get'
    });
};

const addnewinformation = (params) => {
    return service({
        url: '/api/data/addnewinformation',
        method: 'post',
        data: params
    });
};

const editnewinformation = (params) => {
    return service({
        url: '/api/data/editnewinformation',
        method: 'post',
        data: params
    });
};

const delnewinformation = (params) => {
    return service({
        url: '/api/data/delnewinformation',
        method: 'post',
        data: params
    });
};

const getnewinformationview = () => {
    return service({
        url: '/api/data/getnewinformationview',
        method: 'get'
    });
};

const docs = () => {
    return service({
        url: '/api/docs',
        method: 'post',
    })
};

export {
    login,
    userlist,
    usercreate,
    unlogin,
    userupdate,
    docs,
    datareq,
    myreqlist,
    myreqcount,
    handlereqlist,
    handlereqcount,
    acceptreq,
    handlefileupdate,
    mydataedit,
    usermap,
    processrecords,
    download,
    taskoverview,
    taskoverviewinfo,
    getnewinformation,
    addnewinformation,
    editnewinformation,
    delnewinformation,
    getnewinformationview
}
