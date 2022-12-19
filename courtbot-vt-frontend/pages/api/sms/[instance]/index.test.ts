import { subscribe } from '../../../../utils/tests';
import { randomPhoneNumber, eventAsCase } from '../../../../utils/tests';
import { EventDao, initialize as initializeInstanceDao } from '../../../../instances/vt/dao/mongoose';
import { ReminderDao, initialize as initializeDao } from '../../../../dao/mongoose';

describe('handler()', () => {
    describe('Given a user is subscribing to receiving a notification for the first time', () => {
        let caseUid: string | RegExp;
        let courtSession: { uid: any; number?: any; date?: any; address?: string | String; };
        let phoneNumber: string | number;

        beforeEach(async () => {
            const document = {
                _id: 'CountyName-Probate-114-178-120-litigant_entity-10',
                date: new Date("2023-03-09T13:00:00.000Z"),
                county: { code: 'CountyName', name: 'CountyName County' },
                division: 'Probate',
                judge: { code: 'TB9', name: 'Trudy Butaine' },
                court_room_code: 'Xptwjenx',
                hearing: {
                    date: '11/29/2022',
                    start_time: '09:00',
                    type_code: 'Ryxo',
                    type: 'Vemvfqlbssp'
                },
                doc_id: '114-178-120 Pemdpmogg',
                docket_number: '114-178-120',
                case: { name: 'Plantiff v. Defendant', status: 'Pending', type: 'Civil' },
                litigant: {
                    entity_id: 'litigant_entity',
                    last_name: 'Found',
                    first_name: 'Sarah',
                    full_name: 'Sarah Found',
                    role: { code: '10', rank: '1', description: 'Summary description.' },
                    number: '0'
                },
                attorney: {
                    entity_id: 'attorney_entity',
                    last_name: 'Passings',
                    first_name: 'Bill',
                    suffix: '',
                    full_name: 'Bill Passings'
                },
                calendar_id: '91',
                createdAt: new Date(Date.now()),
                updatedAt: new Date(Date.now()),
            };
            await initializeInstanceDao();
            await initializeDao();
            await EventDao.create(document);
            const eventDocument = await EventDao.findOne({ _id: { '$in': [caseUid] } }).exec();
            phoneNumber = randomPhoneNumber();
            courtSession = eventAsCase(eventDocument);
            caseUid = courtSession.uid;
        })

        afterEach(async () => {
            await ReminderDao.remove({ uid: caseUid, phone: phoneNumber }).exec();
        })

        test('When a user confirms \'yes\' to receive a notification, a single reminder document associated to the subscriber notification confirmation exists.', async () => {
            // Subscribe to receiving notifications with a phone number for a court session.
            let { req: firstRequest, res: firstResponse } = subscribe(phoneNumber, courtSession, 'yes');

            const handler = require('./index').default;

            await handler(firstRequest, firstResponse);

            // The SMS API should respond with 200, OK.
            expect(firstResponse._getStatusCode()).toBe(200);

            // There should be one reminder document with the associated case identifier and phone number.
            const count = await ReminderDao.countDocuments({ uid: caseUid, phone: phoneNumber }).exec();

            expect(count).toBe(1);
        })

        test('When a user confirms \'yes\' to receive a notification, multiple times, a single reminder document associated to the subscriber notification confirmation exists.', async () => {
            // Subscribe to receiving notifications with a phone number for a court session.
            let { req: firstRequest, res: firstResponse } = subscribe(phoneNumber, courtSession, 'yes');

            const handler = require('./index').default;

            await handler(firstRequest, firstResponse);

            // The SMS API should respond with 200, OK.
            expect(firstResponse._getStatusCode()).toBe(200);

            // There should be one reminder document with the associated case identifier and phone number.
            const firstCount = await ReminderDao.countDocuments({ uid: caseUid, phone: phoneNumber }).exec();

            expect(firstCount).toBe(1);

            // Subscribe, again, to receive notifications with a phone number for a court session.
            const { req: secondRequest, res: secondResponse } = subscribe(phoneNumber, courtSession, 'yes');

            await handler(secondRequest, secondResponse);

            // The SMS API should respond with 200, OK.
            expect(secondResponse._getStatusCode()).toBe(200);

            // There should be one reminder document with the associated case identifier and phone number.
            const secondCount = await ReminderDao.countDocuments({ uid: caseUid, phone: phoneNumber }).exec();

            expect(secondCount).toBe(1);
        })

        test('When a user declines with \'no\' to receive notifications, a reminder document is not be created', async () => {
            // Decline to receiving a notification.
            const { req, res } = subscribe(phoneNumber, courtSession, 'no');

            const handler = require('./index').default;

            await handler(req, res);

            expect(res._getStatusCode()).toBe(200);

            const count = await ReminderDao.countDocuments({ uid: caseUid, phone: phoneNumber }).exec();

            // The reminder collection should have no documents.
            expect(count).toBe(0);
        })
    });

    describe('Given a court session a user has subscribed to prior with an associated Reminder document having an active field value of false', () => {
        let caseUid: string | RegExp;
        let courtSession: { uid: any; number: any; date?: any; address?: string | String; };
        let phoneNumber: string | number;

        beforeEach(async () => {
            const eventDocument = {
                _id: 'CountyName-Probate-114-178-120-litigant_entity-10',
                date: new Date("2023-03-09T13:00:00.000Z"),
                county: { code: 'CountyName', name: 'CountyName County' },
                division: 'Probate',
                judge: { code: 'TB9', name: 'Trudy Butaine' },
                court_room_code: 'Xptwjenx',
                hearing: {
                    date: '11/29/2022',
                    start_time: '09:00',
                    type_code: 'Ryxo',
                    type: 'Vemvfqlbssp'
                },
                doc_id: '114-178-120 Pemdpmogg',
                docket_number: '114-178-120',
                case: { name: 'Plantiff v. Defendant', status: 'Pending', type: 'Civil' },
                litigant: {
                    entity_id: 'litigant_entity',
                    last_name: 'Found',
                    first_name: 'Sarah',
                    full_name: 'Sarah Found',
                    role: { code: '10', rank: '1', description: 'Summary description.' },
                    number: '0'
                },
                attorney: {
                    entity_id: 'attorney_entity',
                    last_name: 'Passings',
                    first_name: 'Bill',
                    suffix: '',
                    full_name: 'Bill Passings'
                },
                calendar_id: '91',
                createdAt: new Date(Date.now()),
                updatedAt: new Date(Date.now()),
            };

            await initializeInstanceDao();
            await initializeDao();
            await EventDao.create(eventDocument);

            const document = await EventDao.findOne({ _id: { '$in': [caseUid] } }).exec();
            phoneNumber = randomPhoneNumber();
            courtSession = eventAsCase(eventDocument);
            caseUid = courtSession.uid;

            const reminderDocument = {
                uid: 'CountyName-Probate-114-178-120-litigant_entity-10',
                number: '114-178-120',
                phone: phoneNumber,
                active: false,
            }
            await ReminderDao.create(reminderDocument);
        })

        afterEach(async () => {
            await ReminderDao.remove({ uid: caseUid, phone: phoneNumber }).exec();
        })

        test('When a user confirms \'yes\' to receive a notification, a reminder document associated to the subscriber notification is updated with an active state set to true.', async () => {
            // Subscribe to receiving notifications with a phone number for a court session.
            let { req: firstRequest, res: firstResponse } = subscribe(phoneNumber, courtSession, 'yes');

            const handler = require('./index').default;

            await handler(firstRequest, firstResponse);

            // The SMS API should respond with 200, OK.
            expect(firstResponse._getStatusCode()).toBe(200);

            const count = await ReminderDao.countDocuments({ uid: caseUid, phone: phoneNumber }).exec();

            // The reminder collection should have no documents.
            expect(count).toBe(1);

            const document = await ReminderDao.findOne({ uid: caseUid, phone: phoneNumber }).exec();
            const result = {
                uid: document?.uid,
                number: document?.number,
                phone: document?.phone,
                active: document?.active
            }
            const expected = {
                uid: courtSession.uid ,
                number: courtSession.number,
                phone: phoneNumber,
                active: true,
            }

            // There should be one reminder document with the associated case identifier and phone number.
            expect(result).toStrictEqual(expected);
        })
    });
    
});