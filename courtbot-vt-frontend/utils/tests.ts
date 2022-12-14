import { randomInt } from 'node:crypto';
import { createMocks } from 'node-mocks-http';
import { Case } from '../types/case';

const {
    BASIC_AUTH_USERNAME,
    BASIC_AUTH_PASSWORD
} = process.env;

export function subscribe(phoneNumber: number, courtCase: Case, textMessage: string) {
    const { req, res } = createMocks({ method: 'POST' });

    const auth = Buffer.from(`${BASIC_AUTH_USERNAME}:${BASIC_AUTH_PASSWORD}`).toString('base64');

    req.headers = {
        authorization: `Basic ${auth}`
    };

    req.body = {
        Body: textMessage,
        From: phoneNumber
    };

    req.cookies = {
        state: 'case_found',
        cases: JSON.stringify([courtCase])
    }

    req.query = {
        instance: 'vt'
    };

    res.setHeader = jest.fn();

    res.end = jest.fn();

    return {
        req,
        res
    }
}

export function randomPhoneNumber() {
    const phoneNumber = Array(10)
        .fill(undefined)
        .map((_, _index) => {
            return randomInt(0, 9).toString();
        });
    return "+" + phoneNumber.join("");
}

export function eventAsCase(eventDocument) {
    return {
        uid: eventDocument._id,
        number: eventDocument.docket_number,
        date: eventDocument.date,
        address: `${eventDocument.court_room_code} ${eventDocument.county.name}, VT`
    }
}