import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
    scenarios: {
        upscale: {
            executor: 'constant-vus',
            vus: 5,
            exec: 'upscale',
            duration: '1m',
            tags: {test_type: 'upscale'}
        },
        downscale: {
            executor: 'constant-vus',
            vus: 5,
            exec: 'downscale',
            startTime: '1m',
            duration: '1m',
            tags: {test_type: 'downscale'}
        }
    },
    thresholds: {
        'http_req_duration{test_type:upscale}': ['p(90)<200'],
        'http_req_failed{test_type:upscale}': ['rate<0.01'],
        'http_req_duration{test_type:downscale}': ['p(90)<700'],
        'http_req_failed{test_type:downscale}': ['rate<0.01'],
    },
    summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'count']
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

function creteSize(from, to, step) {
    return Math.floor(Math.random() * Math.floor((to - from) / step)) * step + from
}

export function upscale(data) {
    let width = creteSize(800, 1500, 20);  // generate number [800, 820, ..., 1500]
    let height = creteSize(800, 1500, 20);  // generate number [800, 820, ..., 1500]
    http.get(baseUrl + '/api/v1/images/' + width + 'x' + height + '/' + data.image_id);
    sleep(1) ;
}

export function downscale(data) {
    let width = creteSize(20, 500, 20);  // generate number [20, 40, ..., 500]
    let height = creteSize(20, 500, 20);  // generate number [20, 40, ..., 500]
    http.get(baseUrl + '/api/v1/images/' + width + 'x' + height + '/' + data.image_id);
    sleep(1) ;
}
