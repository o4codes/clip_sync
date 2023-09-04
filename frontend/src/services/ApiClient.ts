import axios from "axios";

axios.defaults.baseURL = "http://backend/api/v1"

export default class ApiClient {

    static setHeaders(header: { [key: string]: string }) {
        for (const key  of Object.keys(header)) {
            axios.defaults.headers.common[key] = header[key];
        }
    }

    static async setAuthorization(token: string) {
        axios.defaults.headers.common.Authorization = `Bearer ${token}`;
    }

    static removeAllHeaders(){
        axios.defaults.headers.common = {};
    }

    static async get(resource: string, params: object | null = null) {
        return await axios.get(resource, { params })
    }

    static async post(resource: string, data: object | null = null) {
        return await axios.post(resource, data)
    }

    static async put(resource: string, data: object) {
        return await axios.put(resource, data)
    }

    static async patch(resource: string, data: object) {
        return await axios.patch(resource, data)
    }

    static async delete(resource: string) {
        return await axios.delete(resource)
    }
}
