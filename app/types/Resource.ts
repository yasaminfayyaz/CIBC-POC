/**
 * Defines a helper object that represents a single resource returned by the PEP.
 */
export interface Resource {
    resourceID: number;
    resourceName: string;
}

/**
 * Defines an object that represents data returned by the PEP.
 */
export interface GetResourceAPIReturn {
    resources: Array<Resource>;
}