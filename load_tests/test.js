import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
    vus: 5,
    duration: '1m',
    thresholds: {
        'http_req_duration': ['p(95)<300'],
        'http_req_failed': ['rate<0.01']
    },
    throw: true
};

const baseUrl = 'http://0.0.0.0:8080'
const filePath = '../tests/data/test.jpg'
const file = open(filePath, 'b');

export function setup() {
    const data = {
        file: http.file(file, 'test.jpg', 'image/jpg'),
    };
    const res = http.post(baseUrl + '/api/v1/images', data);
    return {image_id: res.json()['image_id']};
}

export default function (data) {
    let width = Math.floor(Math.random()* 50) * 20 + 20;  // generate number [20, 40, ..., 1000]
    let height = Math.floor(Math.random()* 50) * 20 + 20;  // generate number [20, 40, ..., 1000]
    http.get(baseUrl + '/api/v1/images/' + width + 'x' + height + '/' + data.image_id);
    sleep(1) ;
}
