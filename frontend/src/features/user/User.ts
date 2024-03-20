export enum Role {
    USER = 'USER',
    ADMIN = 'ADMIN',
}

export type User = {
    id: number;
    name: string;
    role: Role;
};
