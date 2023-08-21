export interface Resource {
    resourceID: number;
    resourceName: string;
}

export interface GetResourceAPIReturn {
    resources: Array<Resource>;
}