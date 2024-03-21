export enum Role {
    ADMIN = 'ADMIN',
    USER_FLOOR_1 = 'USER_FLOOR_1',
    USER_FLOOR_2 = 'USER_FLOOR_2',
}

export type User = {
    id: number;
    name: string;
    role: Role;
    flat: number;
};
