import { Store } from 'pullstate';

interface UIStore {
    userToken?: string;
}

export const applicationStore = new Store<UIStore>({ userToken: undefined });