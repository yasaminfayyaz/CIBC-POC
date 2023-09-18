/**
 * Defines an object that represents an available resource.
 */
export interface Document {
    fileName: string;
    createdAt: Date;
    createdBy: string;
    size: number;
    securityLevel: string;
}