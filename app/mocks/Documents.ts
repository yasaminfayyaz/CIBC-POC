import { Document } from '../types/Document';

export const DocumentListMock = Array<Document>(
    {
        createdAt: new Date(1690981200000),
        createdBy: 'Felipe',
        fileName: 'File 1',
        securityLevel: 'TOP_SECRET',
        size: 4194304
    },
    {
        createdAt: new Date(1690894800000),
        createdBy: 'Yasamin',
        fileName: 'File 2',
        securityLevel: 'SECRET',
        size: 5242880
    },
    {
        createdAt: new Date(1690808400000),
        createdBy: 'Shahrbanoo',
        fileName: 'File 3',
        securityLevel: 'CLASSIFIED',
        size: 6291456
    },
    {
        createdAt: new Date(1690549200000),
        createdBy: 'Khalil',
        fileName: 'File 4',
        securityLevel: 'UNCLASSIFIED',
        size: 7340032
    },
    {
        createdAt: new Date(1690462800000),
        createdBy: 'Felipe',
        fileName: 'File 5',
        securityLevel: 'UNCLASSIFIED',
        size: 8388608
    },
    {
        createdAt: new Date(1690376400000),
        createdBy: 'Yasamin',
        fileName: 'File 6',
        securityLevel: 'CLASSIFIED',
        size: 9437184
    },
    {
        createdAt: new Date(1690290000000),
        createdBy: 'Shahrbanoo',
        fileName: 'File 7',
        securityLevel: 'SECRET',
        size: 10485760
    },
    {
        createdAt: new Date(1690203600000),
        createdBy: 'Khalil',
        fileName: 'File 8',
        securityLevel: 'TOP_SECRET',
        size: 11534336
    }
);