// 引用 crypto-js 加密模块
// var CryptoJS = require('./crypto-js')
// const NodeRSA = require('./node-rsa');
// const axios = require('./axios');
// module.exports = { get_list_params, HMACEncrypt,getpack };
function get_timestamp() {
    var date = new Date(); //获取当前时间
    return Math.ceil(date.getTime() / 1000).toString();
}

function get_list_params(type_id, _class = '类型', area = "地区", year = "年份", page = "1", pagesize = "21") {

    var json_data = {
        "type_id": type_id,
        "sort": "by_default",
        "class": "类型",
        "area": "地区",
        "year": "年份",
        "page": page,
        "pageSize": "21",
        "timestamp": get_timestamp()
    }
    return JSON.stringify(json_data)
}

// console.log(get_list_params(1));

function HMACEncrypt(encrypt_str) {
    var text = encrypt_str;
    var secret_key = "635a580fcb5dc6e60caa39c31a7bde48";
    return CryptoJS.HmacMD5(text, secret_key).toString();
}

function getpack(encrypt_str) {
    const publicKeyPem = '-----BEGIN PUBLIC KEY-----'
        +'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA02F/kPg5A2NX4qZ5JSns+bjhVMCC6JbTiTKpbgNgiXU+Kkorg6Dj76gS68gB8llhbUKCXjIdygnHPrxVHWfzmzisq9P9awmXBkCk74Skglx2LKHa/mNz9ivg6YzQ5pQFUEWS0DfomGBXVtqvBlOXMCRxp69oWaMsnfjnBV+0J7vHbXzUIkqBLdXSNfM9Ag5qdRDrJC3CqB65EJ3ARWVzZTTcXSdMW9i3qzEZPawPNPe5yPYbMZIoXLcrqvEZnRK1oak67/ihf7iwPJqdc+68ZYEmmdqwunOvRdjq89fQMVelmqcRD9RYe08v+xDxG9Co9z7hcXGTsUquMxkh29uNawIDAQAB'
    +"-----END PUBLIC KEY-----";
    // 创建一个新的 NodeRSA 实例，并导入公钥
    const key = new NodeRSA(publicKeyPem);
    key.setOptions({ encryptionScheme: 'pkcs1' });
    const encrypted = key.encrypt(encrypt_str, 'base64');
    return encrypted;
}

function get_list(type_id, page = "1", _class = '类型', area = "地区", year = "年份", pagesize = "21") {
    var url = "https://app-v1.ecoliving168.com/api/v1/movie/screen/list"
    var par = get_list_params(type_id);
    var pack = getpack(par)
    var signature = HMACEncrypt(pack)
    console.log(pack,'\n',signature);
    // var data = JSON.stringify({pack: pack, signature: signature});
    axios.get(url, {
        params: {
            pack: pack,
            signature: signature
        }
    })
        .then(response => {
            console.log(JSON.stringify(response.data));
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

