import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'http://127.0.0.1:8090/api/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: 'http://127.0.0.1:8090/api/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: 'http://127.0.0.1:8090/api/user/logout',
    method: 'post'
  })
}

export function postUser(data) {
  return request({
    url: 'http://127.0.0.1:8090/api/user',
    method: 'post',
    data
  })
}

export function getUserList() {
  return request({
    url: 'http://127.0.0.1:8090/api/userList',
    method: 'get'
  })
}

export function postDoctor(data) {
  return request({
    url: 'http://127.0.0.1:8090/api/doctor',
    method: 'post',
    data
  })
}

export function getDoctorList() {
  return request({
    url: 'http://127.0.0.1:8090/api/doctorList',
    method: 'get'
  })
}

